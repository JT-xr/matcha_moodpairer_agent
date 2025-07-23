# app.py
# Core Streamlit framework for web app
import os
import streamlit as st

# Custom modules for app functionality
from mood_drink_map import get_drink_for_mood  # Maps user moods to recommended drinks
from cafe_search import search_matcha_cafes  # Searches for matcha cafes by location
from dotenv import load_dotenv  # Loads environment variables from .env file
from whiski_agent import agent  # AI agent for matcha recommendations and chat
from splashpage import show_welcomepage  # Displays welcome/landing page
from weather_api import get_nyc_weather  # Fetches current NYC weather data
from location_cards import display_expandable_cafe_cards  # UI component for cafe display

load_dotenv()

# Streamlit UI
st.set_page_config(page_title="Whiski", page_icon="🍵")

# Show welcome page before main content
show_welcomepage()

st.markdown('<h1 style="font-size: 75px;">Whiski</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="color: black;">The matcha AI Agent helps you find the perfect drink and cafe based on your mood!</h3>', unsafe_allow_html=True)


# Mood selection with emojis
st.markdown("### ✨ Pick your Vibe")

#
vibes = {
    "😌": "chill",
    "😰": "anxious",
    "🎨": "creative",
    "🧘": "reflective",
    "⚡": "energized",
    "☕": "cozy"
}

# General styling for all buttons
st.markdown(
    """
    <style>
    .stButton>button {
        font-size: 10px;
        padding: 0.01rem .001rem;
        margin: 0.01rem;
        border-radius: 100px;
        width: 55%;
        color: black; 
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# UI - Grid of buttons for each mood
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



# Mood options mapping
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
selected_borough = st.radio("", boroughs)

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
            display_expandable_cafe_cards(cafes)
        else:
            st.warning("No matcha cafés found near that location.")

        # ── Use our SmolAgent/Whiski agent for matcha pairing ──
        # Load and fill our prompt template
        template_path = os.path.join(os.path.dirname(__file__), "templates", "prompt_template_gemini.txt")
        with open(template_path, "r") as tf:
            template = tf.read()
        # Assume the template uses {mood}, {location}, and {weather} placeholders
        filled_task = template.format(
            mood=mood,
            location=location,
            weather=get_nyc_weather()
        )
        response = agent.run(filled_task)
        
        # Option 3: Split Layout (Text + Image Side by Side)
        col1, col2 = st.columns([3, 2])

        with col1:
            st.markdown(f"""
            <div style="
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 5px solid #4CAF50;
                height: 100%;
            ">
                <h3 style="color: #2c3e50; margin-top: 0;">🧠 Whiski's Recommendation</h3>
                <div style="background: #e8f5e8; padding: 10px; border-radius: 8px; margin: 10px 0;">
                    <strong>🍵 Drink:</strong> {drink}
                </div>
                <div style="background: #fff; padding: 15px; border-radius: 8px; margin: 10px 0;">
                    <strong>✨ Vibe:</strong><br>
                    {response}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.image("matcha_cafe.png", caption="Matcha Vibe", width=400)


# Chat interface
st.markdown("")
st.markdown('<hr style="margin: 100px;">', unsafe_allow_html=True)
st.markdown("### 💬 Chat with Whiski")

st.image("bot.png", width=120,output_format="PNG")
if prompt := st.chat_input("Ask me about Matcha!"):
    st.chat_message("user").write(prompt)
    response = agent.run(prompt)
    st.chat_message("assistant").markdown(f'<span style="color: black;">**Whiski 🧠:**</span> {response}', unsafe_allow_html=True)


