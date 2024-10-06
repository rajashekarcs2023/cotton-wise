# This file contains the utility functions for farm advice
# In a real application, these would likely make API calls or database queries

def get_maharashtra_cotton_irrigation_advice(latitude, longitude, field_size, planting_date, soil_type):
    return {
        "irrigation_advice": f"Irrigate with 25mm of water in the next 2-3 days.",
        "water_requirement": 30,
        "recent_rainfall": 5,
        "water_saving_tip": "Consider mulching to reduce water evaporation from the soil."
    }

def get_pest_disease_warning():
    return ["High temperature and humidity. Monitor for bollworm activity."]

def get_cotton_prices():
    return {"current_price": 6000, "forecast_next_month": 6200}

def get_weather_alerts():
    return ["Extreme heat expected. Ensure adequate irrigation to prevent heat stress."]

def get_soil_health_advice(soil_type, days_since_planting):
    return "Maintain soil moisture to support root development. Avoid waterlogging."