from pydantic import BaseModel

class CropRequest(BaseModel):
    location: str
    soil_type: str
