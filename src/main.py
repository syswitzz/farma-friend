from fastapi import FastAPI
from src.routers.crop import router as crop_router

app = FastAPI(title="Farma Friend API", version="0.1.0")

# Include routers
app.include_router(crop_router, prefix="/api/crops", tags=["crops"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Farma Friend API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}