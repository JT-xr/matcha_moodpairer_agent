"""
Button Components for Whiski App
Provides styled buttons for mood selection, locations, and actions.
"""

import streamlit as st
from ..utils import navigate_to_scene

def render_mood_button_grid(moods, target_scene, session_key="selected_mood"):
    """
    Render a grid of mood selection buttons
    
    Args:
        moods (dict): Dictionary of emoji -> mood mappings
        target_scene (str): Scene to navigate to when mood is selected
        session_key (str): Session state key to store selected mood
    """
    # Create 2x3 grid
    for row in range(2):
        cols = st.columns(3, gap="small")
        for col in range(3):
            index = row * 3 + col
            if index < len(list(moods.items())):
                emoji, mood = list(moods.items())[index]
                with cols[col]:
                    if st.button(f"{emoji} {mood.title()}", key=f"mood_{mood}", use_container_width=True):
                        st.session_state[session_key] = mood
                        navigate_to_scene(target_scene)

def render_location_button_list(locations, target_scene, custom_scene=None, session_key="user_location"):
    """
    Render a list of location selection buttons
    
    Args:
        locations (list): List of location strings
        target_scene (str): Scene to navigate to when location is selected
        custom_scene (str): Optional scene for "Other Location" option
        session_key (str): Session state key to store selected location
    """
    for i, location in enumerate(locations):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"📍 {location}", key=f"loc_{i}", use_container_width=True):
                if location == "Other Location" and custom_scene:
                    # Set transitioning flag to prevent dual rendering
                    st.session_state.transitioning = True
                    navigate_to_scene(custom_scene)
                else:
                    # Set transitioning flag to prevent dual rendering
                    st.session_state.transitioning = True
                    st.session_state[session_key] = location
                    # Also set legacy key for compatibility
                    st.session_state.selected_location = location
                    navigate_to_scene(target_scene)
                # Immediately stop further rendering
                st.stop()

def render_action_button(label, action, button_type="secondary", key_suffix="", full_width=False):
    """
    Render a single action button
    
    Args:
        label (str): Button text
        action (callable): Function to call when clicked
        button_type (str): Streamlit button type
        key_suffix (str): Suffix for button key
        full_width (bool): Whether to use full container width
    """
    if st.button(label, key=f"action_{key_suffix}", type=button_type, use_container_width=full_width):
        action()

def render_start_button(target_scene, label="🚀 Start"):
    """Render the main start button for welcome page"""
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button(label, key="start_btn", use_container_width=True):
            navigate_to_scene(target_scene)
