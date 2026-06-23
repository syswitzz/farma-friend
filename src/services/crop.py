import requests as r
from datasets.constants import SOIL_DATABASE
from geopy.geocoders import Nominatim
from fastapi import HTTPException, status


geolocator = Nominatim(user_agent="crop_recommendation_app")


def get_weather_values(location: str):
    loc = geolocator.geocode(location)

    if not loc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"status": "error", "message": "Location could not be found."})
    
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": loc.latitude,
        "longitude": loc.longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "rain"],
        "timezone": "auto"
    }

    try:
        response = r.get(weather_url, params=params, timeout=10)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail={"status": "error", "message": f"Weather API request failed with status code {response.status_code}"})
            
        data = response.json().get("current", {})
        
        return {
            "location": loc.address,
            "metrics": {
                "temperature": data.get("temperature_2m"),
                "humidity": data.get("relative_humidity_2m"),
                "rainfall": data.get("rain")
            }
        }
        
    except r.exceptions.RequestException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"status": "error", "message": f"Network request failed: {str(e)}"})




def get_soil_values(soil_type: str):
    soil_type = soil_type.strip().lower()

    if soil_type in SOIL_DATABASE:
        soil = SOIL_DATABASE[soil_type]
        return soil["N"], soil["P"], soil["K"], soil["ph"]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"status": "error", "message": f"Soil type '{soil_type}' not found in the database."})
