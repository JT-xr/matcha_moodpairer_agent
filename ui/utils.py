"""
UI Utilities for Whiski Matcha Mood Pairer
Contains shared utility functions for navigation, session state, and UI helpers.
"""

import streamlit as st

# Scene constants
SCENES = {
    'WELCOME': 'welcome',
    'MOOD_SELECTION': 'mood_selection',
    'LOCATION_INPUT': 'location_input',
    'LOADING': 'loading',
    'RESULTS': 'results',
    'CAFE_DETAILS': 'cafe_details',
    'CHAT': 'chat'
}

def init_session_state():
    """Initialize all session state variables"""
    if 'current_scene' not in st.session_state:
        st.session_state.current_scene = SCENES['WELCOME']
    
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    
    if 'selected_mood' not in st.session_state:
        st.session_state.selected_mood = None
    
    if 'user_location' not in st.session_state:
        st.session_state.user_location = None
    
    # Legacy compatibility - keep both keys for now
    if 'selected_location' not in st.session_state:
        st.session_state.selected_location = None
    
    if 'weather_data' not in st.session_state:
        st.session_state.weather_data = None
    
    if 'drink_recommendation' not in st.session_state:
        st.session_state.drink_recommendation = None
    
    if 'vibe_description' not in st.session_state:
        st.session_state.vibe_description = None
    
    if 'cafe_results' not in st.session_state:
        st.session_state.cafe_results = []
    
    if 'selected_cafe' not in st.session_state:
        st.session_state.selected_cafe = None
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def navigate_to_scene(scene_name):
    """Navigate to a specific scene"""
    if scene_name in SCENES.values():
        st.session_state.current_scene = scene_name
        st.rerun()

def get_current_scene():
    """Get the current scene"""
    return st.session_state.get('current_scene', SCENES['WELCOME'])

def update_progress(percentage):
    """Update the progress bar percentage"""
    st.session_state.progress = min(100, max(0, percentage))

def get_progress_by_scene(scene_name):
    """Get progress percentage based on current scene"""
    progress_map = {
        SCENES['WELCOME']: 0,
        SCENES['MOOD_SELECTION']: 20,
        SCENES['LOCATION_INPUT']: 40,
        SCENES['RESULTS']: 60,
        SCENES['CAFE_DETAILS']: 80,
        SCENES['CHAT']: 100
    }
    return progress_map.get(scene_name, 0)

def reset_session():
    """Reset all session state to start over"""
    keys_to_keep = ['current_scene']  # Keep navigation state
    keys_to_clear = [key for key in st.session_state.keys() if key not in keys_to_keep]
    
    for key in keys_to_clear:
        del st.session_state[key]
    
    init_session_state()
    navigate_to_scene(SCENES['WELCOME'])

def format_location_display(location):
    """Format location string for display"""
    if not location:
        return "Location not set"
    return f"📍 {location}"

def format_mood_display(mood):
    """Format mood string for display"""
    if not mood:
        return "Mood not selected"
    return f"😊 {mood.title()}"
