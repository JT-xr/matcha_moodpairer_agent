# app.py

import os
import google.generativeai as genai
import streamlit as st
import datetime
import requests
from mood_drink_map import get_drink_for_mood
from cafe_search import search_matcha_cafes
from string import Template
from dotenv import load_dotenv


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

# Streamlit UI
st.set_page_config(page_title="Matcha Mood Mix 🍵", page_icon="🍵")


st.title("Whiski")
st.subheader("The matcha AI Agent here to help you find the perfect drink and cafe based on your mood!")



# 📅 Current date and time
now = datetime.datetime.now()
st.markdown(f"**🗓️ Today:** {now.strftime('%B %d')}")

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



# Mood selection with emojis
st.markdown("### ✨ Pick your Vibe")

vibes = {
    "😌": "chill",
    "😰": "anxious",
    "🎨": "creative",
    "🧘": "reflective",
    "⚡": "energized",
    "☕": "cozy"
}

st.markdown(
    """
    <style>
    .stButton>button {
        font-size: 10px;
        padding: 0.01rem .001rem;
        margin: 0.01rem;
        border-radius: 100px;
        width: 55%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Use two rows of three columns for better grid layout
emoji_grid = list(vibes.items())
for row in range(2):
    cols = st.columns(3)
    for col in range(3):
        index = row * 3 + col
        if index < len(emoji_grid):
            emoji, label = emoji_grid[index]
            button_label = f"{emoji} {label}"
            with cols[col]:
                container = st.container()
                if container.button(button_label, key=f"mood_{label}"):
                    st.session_state.selected_mood = label

if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = list(vibes.values())[0]  # Default

mood = st.session_state.selected_mood



# Inputs
mood_options = {
    "😌 chill": "chill",
    "😰 anxious": "anxious",
    "🎨 creative": "creative",
    "🧘 reflective": "reflective",
    "⚡ energized": "energized",
    "☕ cozy": "cozy"
}





# Location handling
st.markdown("### 📍 Choose a location")
st.markdown("<style>div[data-testid='stMarkdownContainer'] h3 { margin-bottom: 0.00rem !important; }</style>", unsafe_allow_html=True)
boroughs = ["Brooklyn, NY", "Manhattan, NY", "Queens, NY", "Other"]
selected_borough = st.selectbox("", boroughs)

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
        
        st.markdown("---")
        st.success(f"Success!")

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
        st.markdown("---")
        try:
            response = model.generate_content(prompt)
            st.markdown("🧠 **Whiski's Advice:**")
            st.write(response.text)
        except Exception as e:
            st.error(f"Gemini error: {e}")

        st.markdown("Mood Image:")
        st.image("matcha_cafe.jpeg", caption="Matcha Vibe")


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
