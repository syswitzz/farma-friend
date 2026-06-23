from fastapi import APIRouter
import joblib

from models import CropRequest
from utils.crop import get_soil_values, get_weather_values

router = APIRouter()
model = joblib.load("ml/crop_model.pkl")

@router.post("")
def get_crops(crop_request: CropRequest):

    n, p, k, ph = get_soil_values(crop_request.soil_type)
    weather = get_weather_values(crop_request.location)["metrics"]
    location, temperature, humidity, rainfall = weather["location"], weather["temperature"], weather["humidity"], weather["rainfall"]

    prediction = model.predict([[n, p, k, ph, rainfall, temperature, humidity]])

    return {"location": location, "recommended_crop": prediction[0]}

