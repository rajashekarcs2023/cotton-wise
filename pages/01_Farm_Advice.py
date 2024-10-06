import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta
import requests

st.title("Farm Advice")

# Sidebar for input parameters
st.sidebar.header("Farm Information")
latitude = st.sidebar.number_input("Farm Latitude", value=19.7515)
longitude = st.sidebar.number_input("Farm Longitude", value=75.7139)
field_size = st.sidebar.number_input("Field Size (hectares)", value=5.0, min_value=0.1)
planting_date = st.sidebar.date_input("Planting Date", value=date.today() - timedelta(days=60))

if st.button("Get Advice"):
    # Call FastAPI backend
    response = requests.post("http://localhost:8000/irrigation-advice/", json={
        "latitude": latitude,
        "longitude": longitude,
        "field_size": field_size,
        "planting_date": planting_date.isoformat()
    })
    
    if response.status_code == 200:
        advice = response.json()
        
        # Display advice
        st.header("📊 Farm Overview")
        st.info(f"**Location**: {latitude:.4f}°N, {longitude:.4f}°E")
        st.info(f"**Field Size**: {field_size} hectares")
        st.info(f"**Days Since Planting**: {(date.today() - planting_date).days}")

        st.header("💧 Irrigation Advice")
        daily_advice = advice["daily_advice"]
        if daily_advice["irrigate"]:
            st.success(f"Irrigate today with {daily_advice['amount_liters']:.2f} liters of water.")
        else:
            st.info("No irrigation needed today.")
        
        # Water balance chart
        weekly_forecast = advice["weekly_forecast"]
        dates = [item["date"] for item in weekly_forecast]
        rainfall = [item["expected_rainfall_mm"] for item in weekly_forecast]
        irrigation_need = [item["irrigation_need_mm"] for item in weekly_forecast]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=dates, y=rainfall, name="Expected Rainfall (mm)", marker_color='blue'))
        fig.add_trace(go.Bar(x=dates, y=irrigation_need, name="Irrigation Need (mm)", marker_color='red'))
        fig.update_layout(title="7-Day Forecast: Rainfall vs Irrigation Need", barmode='group')
        st.plotly_chart(fig, use_container_width=True)

        st.header("💡 Water Saving Tip")
        st.success(advice["water_saving_tip"])

    else:
        st.error("Failed to fetch advice. Please try again later.")

else:
    st.info("👈 Please enter your farm details in the sidebar and click 'Get Advice' to receive personalized recommendations.")