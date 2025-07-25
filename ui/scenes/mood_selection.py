"""
Mood Selection Scene for Whiski App
Allows users to select their current mood/vibe.
"""

import streamlit as st
from styles import get_scene_header_style
from ..components.progress_bar import render_progress_bar
from ..components.buttons import render_mood_button_grid
from ..utils import SCENES

def render_mood_selection_scene():
    """Render the mood selection scene"""
    render_progress_bar(1)
    
    # Scene header
    st.markdown(get_scene_header_style(
        "✨ What's your vibe?",
        "Choose the mood that best describes how you're feeling right now"
    ), unsafe_allow_html=True)
    
    # Mood options
    vibes = {
        "😌": "chill",
        "😰": "anxious", 
        "🎨": "creative",
        "🧘": "reflective",
        "⚡": "energized",
        "☕": "cozy"
    }
    
    # Render mood button grid
    render_mood_button_grid(vibes, SCENES['LOCATION_INPUT'])
