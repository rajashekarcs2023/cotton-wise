import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta
import random
from openai_chat import get_ai_response  # Import the OpenAI chat function

# Simulated function calls - replace these with actual API calls in production
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

# Set page config
st.set_page_config(page_title="CottonDrip: Smart Advisor for Maharashtra Cotton Farmers", page_icon="🌱", layout="wide")

# Title and introduction
st.title("🌱 CottonDrip: Smart Advisor for Maharashtra Cotton Farmers")
st.markdown("""
This tool provides personalized advice for cotton farmers in Maharashtra, 
helping you make informed decisions about irrigation, pest control, and more.
""")

# Sidebar for input parameters
st.sidebar.header("Farm Information")
latitude = st.sidebar.number_input("Farm Latitude", value=19.7515)
longitude = st.sidebar.number_input("Farm Longitude", value=75.7139)
field_size = st.sidebar.number_input("Field Size (hectares)", value=5.0, min_value=0.1)
planting_date = st.sidebar.date_input("Planting Date", value=date.today() - timedelta(days=60))
soil_type = st.sidebar.selectbox("Soil Type", ["sandy", "loamy", "clay"])

# Main content
col1, col2 = st.columns(2)

with col1:
    if st.button("Get Advice"):
        # Fetch advice (simulated)
        advice = get_maharashtra_cotton_irrigation_advice(latitude, longitude, field_size, planting_date, soil_type)
        pest_warnings = get_pest_disease_warning()
        market_info = get_cotton_prices()
        weather_alerts = get_weather_alerts()
        
        # Calculate days since planting
        days_since_planting = (date.today() - planting_date).days
        soil_health_tip = get_soil_health_advice(soil_type, days_since_planting)

        # Display advice in main area
        st.header("📊 Farm Overview")
        st.info(f"**Location**: {latitude:.4f}°N, {longitude:.4f}°E")
        st.info(f"**Field Size**: {field_size} hectares")
        st.info(f"**Soil Type**: {soil_type.capitalize()}")
        st.info(f"**Days Since Planting**: {days_since_planting}")

        st.header("💧 Irrigation Advice")
        st.success(advice["irrigation_advice"])
        
        # Water balance chart
        fig = go.Figure(go.Bar(x=['Requirement', 'Rainfall', 'Irrigation Need'],
                               y=[advice['water_requirement'], advice['recent_rainfall'], 
                                  max(0, advice['water_requirement'] - advice['recent_rainfall'])],
                               marker_color=['#1976D2', '#43A047', '#C62828']))
        fig.update_layout(title="Water Balance (mm)", height=300)
        st.plotly_chart(fig, use_container_width=True)

        st.header("🌡️ Weather Alerts")
        for alert in weather_alerts:
            st.warning(alert)

        st.header("🐛 Pest and Disease Warnings")
        for warning in pest_warnings:
            st.error(warning)

        st.header("💰 Market Information")
        st.metric("Current Cotton Price", f"₹{market_info['current_price']} per quintal")
        st.metric("Forecasted Price (Next Month)", f"₹{market_info['forecast_next_month']} per quintal",
                  delta=f"₹{market_info['forecast_next_month'] - market_info['current_price']}")

        st.header("🌱 Soil Health")
        st.info(soil_health_tip)

        st.header("💡 Water Saving Tip")
        st.success(advice['water_saving_tip'])

        # Historical data visualization
        st.header("📈 Historical Data")
        # Simulated historical data - replace with actual data in production
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        dates = pd.date_range(start=start_date, end=end_date).tolist()
        rainfall = [random.uniform(0, 10) for _ in range(len(dates))]
        temperature = [random.uniform(25, 40) for _ in range(len(dates))]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=rainfall, name="Rainfall (mm)", yaxis="y1"))
        fig.add_trace(go.Scatter(x=dates, y=temperature, name="Temperature (°C)", yaxis="y2"))
        fig.update_layout(
            title="30-Day Weather History",
            yaxis=dict(title="Rainfall (mm)"),
            yaxis2=dict(title="Temperature (°C)", overlaying="y", side="right")
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    if st.button("Talk with Agri AI ADVISOR"):
        st.header("💬 AI Advisor Chat")
        st.markdown("Ask our AI advisor any questions about cotton farming!")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "system", "content": "You are an AI advisor for cotton farmers in Maharashtra, India. Provide helpful, concise advice on cotton farming practices, pest control, irrigation, and market trends."}
            ]

        # Display chat messages from history on rerun
        for message in st.session_state.messages[1:]:  # Skip the system message
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("What's your question about cotton farming?"):
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Get AI response
            response = get_ai_response(st.session_state.messages)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

if not st.button("Get Advice") and not st.button("Talk with Agri AI ADVISOR"):
    st.info("👈 Please enter your farm details and click 'Get Advice' to receive personalized recommendations or 'Talk with Agri AI ADVISOR' to chat with our AI.")

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ for Maharashtra's cotton farmers. For support, contact support@cottondrip.com")