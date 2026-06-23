from fastapi import APIRouter
import joblib

from src.models import CropRequest
from src.services import crop
from src.services.crop import get_soil_values, get_weather_values
from datasets.constants import CROP_INFO

router = APIRouter()
model = joblib.load("ml/crop_model.pkl")


@router.post("")
def get_crops(crop_request: CropRequest):

    n, p, k, ph = get_soil_values(crop_request.soil_type)

    weather = get_weather_values(crop_request.location)
    location = weather["location"]
    temperature = weather["metrics"]["temperature"]
    humidity = weather["metrics"]["humidity"]
    rainfall = weather["metrics"]["rainfall"]

    features = [[
        n,
        p,
        k,
        temperature,
        humidity,
        ph,
        rainfall,
    ]]
    probabilities = model.predict_proba(features)[0]
    top3_indices = probabilities.argsort()[-3:][::-1]

    recommendations = []

    for index in top3_indices:
        crop = model.classes_[index]
        
        confidence = round(probabilities[index] * 100, 2)
        info = CROP_INFO.get(crop, {})  # {} is the default value

        recommendations.append({
            "crop": crop.title(),
            "confidence": confidence,
            "season": info.get("season"),
            "water_requirement":
                info.get("water_requirement"),
            "description":
                info.get("description"),
            "ideal_temperature":
                info.get("ideal_temperature"),
            "ideal_rainfall":
                info.get("ideal_rainfall"),
        })

    return {
        "location": location,
        "soil_type": crop_request.soil_type,
        "weather": {
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall
        },
        "recommended_crops":
            recommendations
    }

