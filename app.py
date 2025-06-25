# app.py

import streamlit as st
from mood_drink_map import get_drink_for_mood
from cafe_search import search_matcha_cafes

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

# On button click
if st.button("Find my matcha pairing"):
    with st.spinner("Brewing your matcha vibe..."):
        drink = get_drink_for_mood(mood)
        cafes = search_matcha_cafes(location)
        
        st.success(f"🧋 Recommended Drink: **{drink}**")

        if cafes:
            st.markdown("📍 **Nearby Cafés:**")
            for c in cafes[:5]:
                st.markdown(f"- **{c['name']}** — {c['address']} ({c.get('rating', '?')}⭐)\n[View on Maps]({c['map_link']})")
        else:
            st.warning("No matcha cafés found near that location.")