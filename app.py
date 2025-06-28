# app.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

import streamlit as st
from mood_drink_map import get_drink_for_mood
from cafe_search import search_matcha_cafes
from string import Template

import datetime
import requests


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

# Streamlit UI
st.set_page_config(page_title="Matcha Mood Mix 🍵", page_icon="🍵")

st.title("Matcha Mood Mix")
st.subheader("Find the perfect matcha + cafe based on your mood!")

# 📅 Current date and time
now = datetime.datetime.now()
st.markdown(f"**🗓️ Today:** {now.strftime('%A, %B %d, %Y – %I:%M %p')}")

# ♈ Zodiac Sign
def get_zodiac_sign(month, day):
    zodiac = [
        (120, "♑ Capricorn"), (219, "♒ Aquarius"), (320, "♓ Pisces"),
        (420, "♈ Aries"), (521, "♉ Taurus"), (621, "♊ Gemini"),
        (722, "♋ Cancer"), (823, "♌ Leo"), (923, "♍ Virgo"),
        (1023, "♎ Libra"), (1122, "♏ Scorpio"), (1222, "♐ Sagittarius"),
        (1231, "♑ Capricorn")
    ]
    date_num = month * 100 + day
    for z in zodiac:
        if date_num <= z[0]:
            return z[1]
    return "♑ Capricorn"

st.markdown(f"**🔮 Zodiac Sign:** {get_zodiac_sign(now.month, now.day)}")

def get_current_weather(location_name):
    try:
        geocode_resp = requests.get(f"https://geocode.maps.co/search?q={location_name}&format=json").json()
        if not geocode_resp:
            return "Location not found"
        lat = geocode_resp[0]["lat"]
        lon = geocode_resp[0]["lon"]
        weather_resp = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()
        temp = weather_resp["current_weather"]["temperature"]
        return f"{temp}°C"
    except Exception:
        return "Weather unavailable"


# Inputs
mood = st.selectbox(
    "How are you feeling today?",
    ["chill", "anxious", "creative", "reflective", "energized", "cozy"]
)

st.markdown("### 📍 Choose a location")

boroughs = ["Brooklyn, NY", "Manhattan, NY", "Queens, NY", "Other"]
selected_borough = st.selectbox("Pick a borough", boroughs)

custom_location = ""
if selected_borough == "Other":
    custom_location = st.text_input("Enter a location")
    location = custom_location
else:
    location = selected_borough

if not location.strip():
    st.warning("Please enter a valid location.")
    st.stop()

# On button click
if st.button("Find my matcha pairing"):
    with st.spinner("Brewing your matcha vibe..."):
        st.markdown(f"**🌤️ Weather:** {get_current_weather(location)}")
        drink = get_drink_for_mood(mood)
        cafes = search_matcha_cafes(location)
        
        st.success(f"🧋 Recommended Drink: **{drink}**")

        if cafes:
            st.markdown(f"📍 **Nearby Cafés ({len(cafes)} found):**")
            for c in cafes[:5]:
                st.markdown(f"- **{c['name']}** — {c['address']} ({c.get('rating', '?')}⭐)\n[View on Maps]({c['map_link']})")
        else:
            st.warning("No matcha cafés found near that location.")

        # Generate a message with Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        with open("templates/prompt_template_gemini.txt") as f:
            template = Template(f.read())
            prompt = template.substitute(mood=mood, location=location)
            print(prompt)

        try:
            response = model.generate_content(prompt)
            st.markdown("🧠 **Gemini Recommendation:**")
            st.write(response.text)
        except Exception as e:
            st.error(f"Gemini error: {e}")

        st.markdown("**🖼️ Your Matcha Mood Image:** _(placeholder)_")
        st.image("https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=800&q=60", caption="Matcha Vibe")


# Chat interface
st.markdown("---")
st.markdown("### 💬 Chat with Whiski")

st.image("bot.png", width=64)

def get_matcha_response(prompt):
    try:
        chat_model = genai.GenerativeModel("gemini-1.5-flash")
        response = chat_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini error: {e}"

if prompt := st.chat_input("Ask me about Matcha!"):
    st.chat_message("user").write(prompt)
    response = get_matcha_response(prompt)
    st.chat_message("assistant").markdown(f"**Whiski 🧠:** {response}")