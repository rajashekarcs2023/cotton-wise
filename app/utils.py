import requests
from datetime import date, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")

def get_nasa_power_data(lat, lon, start_date, end_date):
    base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "start": start_date,
        "end": end_date,
        "latitude": lat,
        "longitude": lon,
        "community": "ag",
        "parameters": "T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN",
        "format": "JSON"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch NASA data: {response.status_code} {response.text}")

def process_nasa_data(nasa_data):
    processed_data = {}
    for param in ["T2M", "PRECTOTCORR", "ALLSKY_SFC_SW_DWN"]:
        data = nasa_data['properties']['parameter'][param]
        processed_data[param] = {date: value for date, value in data.items() if value != -999}
    return processed_data

def calculate_et0(temp, solar_radiation):
    return 0.0023 * (temp + 17.8) * (solar_radiation * 0.408) ** 0.5

def get_crop_coefficient(days_since_planting):
    if days_since_planting < 30:
        return 0.35
    elif days_since_planting < 70:
        return 0.75
    elif days_since_planting < 120:
        return 1.15
    else:
        return 0.7

def get_irrigation_advice(latitude, longitude, field_size, planting_date):
    today = date(2024, 8, 22)
    end_date = today + timedelta(days=7)
    days_since_planting = (today - planting_date).days
    
    nasa_data = get_nasa_power_data(
        latitude, 
        longitude, 
        today.strftime("%Y%m%d"),
        end_date.strftime("%Y%m%d")
    )
    
    processed_data = process_nasa_data(nasa_data)
    
    daily_advice = []
    weekly_forecast = []
    
    for i in range(8):  # Today + 7 days
        day = today + timedelta(days=i)
        date_str = day.strftime("%Y%m%d")
        
        if date_str in processed_data["T2M"]:
            temp = processed_data["T2M"][date_str]
            solar_rad = processed_data["ALLSKY_SFC_SW_DWN"][date_str]
            precip = processed_data["PRECTOTCORR"][date_str]
            
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
    
    water_saving_tips = [
        "Consider mulching your field to reduce water evaporation.",
        "Implement drip irrigation for more efficient water use.",
        "Monitor soil moisture levels regularly to avoid over-irrigation.",
        "Adjust irrigation schedules based on growth stage and weather conditions.",
        "Maintain your irrigation system to prevent leaks and ensure even distribution."
    ]
    
    return {
        "daily_advice": daily_advice[0],
        "weekly_forecast": weekly_forecast,
        "water_saving_tip": water_saving_tips[today.day % len(water_saving_tips)]  # Rotate tips daily
    }