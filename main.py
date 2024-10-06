import requests
from datetime import date, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")

def get_nasa_power_data(lat, lon, start_date, end_date):
    base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "T2M,PRECTOT,ALLSKY_SFC_SW_DWN",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start_date,
        "end": end_date,
        "format": "JSON"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch NASA data")

def calculate_et0(temp, solar_radiation):
    # Simplified ETo calculation (Hargreaves method)
    return 0.0023 * (temp + 17.8) * (solar_radiation * 0.408) ** 0.5

def get_crop_coefficient(days_since_planting):
    # Simplified crop coefficient for cotton
    if days_since_planting < 30:
        return 0.35
    elif days_since_planting < 70:
        return 0.75
    elif days_since_planting < 120:
        return 1.15
    else:
        return 0.7

def get_irrigation_advice(latitude, longitude, field_size, planting_date):
    today = date.today()
    days_since_planting = (today - planting_date).days
    
    nasa_data = get_nasa_power_data(
        latitude, 
        longitude, 
        today.strftime("%Y%m%d"), 
        (today + timedelta(days=7)).strftime("%Y%m%d")
    )
    
    daily_advice = []
    weekly_forecast = []
    
    for i in range(8):  # Today + 7 days
        day = today + timedelta(days=i)
        temp = nasa_data['properties']['parameter']['T2M'][day.strftime("%Y%m%d")]
        precip = nasa_data['properties']['parameter']['PRECTOT'][day.strftime("%Y%m%d")]
        solar_rad = nasa_data['properties']['parameter']['ALLSKY_SFC_SW_DWN'][day.strftime("%Y%m%d")]
        
        et0 = calculate_et0(temp, solar_rad)
        kc = get_crop_coefficient(days_since_planting + i)
        crop_water_need = et0 * kc
        
        irrigation_need = max(0, crop_water_need - precip)
        irrigation_amount = irrigation_need * field_size * 10  # Convert mm to liters
        
        if i == 0:
            daily_advice.append({
                "date": day.isoformat(),
                "irrigate": irrigation_need > 0,
                "amount_liters": round(irrigation_amount, 2)
            })
        
        weekly_forecast.append({
            "date": day.isoformat(),
            "expected_rainfall_mm": round(precip, 2),
            "irrigation_need_mm": round(irrigation_need, 2)
        })
    
    return {
        "daily_advice": daily_advice[0],
        "weekly_forecast": weekly_forecast,
        "water_saving_tip": "Consider mulching your field to reduce water evaporation."
    }