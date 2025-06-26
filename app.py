# app.py

import streamlit as st
from mood_drink_map import get_drink_for_mood
from cafe_search import search_matcha_cafes

from smolagents import ToolCallingAgent
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Streamlit UI
st.set_page_config(page_title="Matcha Mood Pairer 🍵", page_icon="🍵")

st.title("Matcha Mood Pairer")
st.subheader("Find the perfect matcha + café based on your mood.")

# Inputs
mood = st.selectbox(
    "How are you feeling today?",
    ["chill", "anxious", "creative", "reflective", "energized", "cozy"]
)

location = st.text_input("Where are you located?", "Brooklyn, NY")

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

        if cafes:
            st.markdown("---")

            # Format cafes for the agent
            cafe_text = "\n".join([f"- {c['name']} ({c.get('rating', '?')}⭐) - {c['address']}" for c in cafes[:5]])

            # Load prompt
            with open("templates/prompt_template.txt") as f:
                template = f.read()

            prompt = template.replace("{{ mood }}", mood)\
                            .replace("{{ location }}", location)\
                            .replace("{{ drink }}", drink)\
                            .replace("{{ cafes }}", cafe_text)

            openai_key = os.getenv("OPENAI_API_KEY")
            if not openai_key:
                st.error("Missing OpenAI API key. Please check your .env file.")
                st.stop()

            # Run SmolAgent
            client = OpenAI(api_key=openai_key)
            agent = ToolCallingAgent(
                tools=[],  # you can define tools here later if needed
                model=client.chat
            )
            response = agent.run(prompt)

            st.markdown("🧠 **Your Matcha Concierge Says:**")
            st.write(response)