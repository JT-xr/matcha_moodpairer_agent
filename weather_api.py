import requests
import streamlit as st
from dotenv import load_dotenv
from telemetry import langfuse       
from langfuse import observe, get_client  

load_dotenv()

#🌤️ Weather in NYC
@observe(name="api.get_nyc_weather", as_type="generation")
def get_nyc_weather():
    try:
        weather_resp = requests.get(
            "https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&current_weather=true"
        ).json()
        temp = weather_resp["current_weather"]["temperature"]
        return f"{temp}°C"
    except Exception:
        return "Weather unavailable"

langfuse = get_client()
langfuse.flush()