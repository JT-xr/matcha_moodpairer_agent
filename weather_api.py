import requests
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

#🌤️ Weather in NYC
def get_nyc_weather():
    try:
        weather_resp = requests.get(
            "https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&current_weather=true"
        ).json()
        temp = weather_resp["current_weather"]["temperature"]
        return f"{temp}°C"
    except Exception:
        return "Weather unavailable"

st.markdown(f"**🌤️ Weather:** {get_nyc_weather()}")