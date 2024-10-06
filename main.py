from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from app.utils import get_irrigation_advice

app = FastAPI()

class FarmData(BaseModel):
    latitude: float
    longitude: float
    field_size: float
    planting_date: date

@app.post("/irrigation-advice/")
async def irrigation_advice(farm_data: FarmData):
    try:
        advice = get_irrigation_advice(
            farm_data.latitude,
            farm_data.longitude,
            farm_data.field_size,
            farm_data.planting_date
        )
        return advice
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))