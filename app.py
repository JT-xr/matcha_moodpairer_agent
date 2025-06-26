# app.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

import streamlit as st
from mood_drink_map import get_drink_for_mood
from cafe_search import search_matcha_cafes
from string import Template


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

# Streamlit UI
st.set_page_config(page_title="Matcha Mood Pairer 🍵", page_icon="🍵")

st.title("Matcha Mood Pairer")
st.subheader("Find the perfect matcha + café based on your mood.")

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