"""
Main Whiski App - Integrated with Modular UI System
===================================================
This file integrates the modular UI components from the ui/ directory
with the existing backend functionality from the original app.py.

Migration from prototype_multipage.py completed with real backend integration.
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modular UI system
from ui import init_session_state, navigate_to_scene, get_current_scene, SCENES
from ui.scenes import (
    render_welcome_scene,
    render_mood_selection_scene, 
    render_location_input_scene,
    render_custom_location_scene,
    render_loading_scene,
    render_results_scene,
    render_cafe_details_scene,
    render_chat_scene
)
from styles import apply_global_styles, hide_streamlit_ui

def main():
    """Main application entry point"""
    # Configure Streamlit
    st.set_page_config(
        page_title="Whiski - AI Matcha Mood Pairer", 
        page_icon="🍵",
        layout="centered"
    )
    
    # Initialize session state
    init_session_state()
    
    # Apply global styles
    apply_global_styles()
    hide_streamlit_ui()
    
    # Get current scene
    current_scene = get_current_scene()
    
    # Route to appropriate scene
    if current_scene == SCENES['WELCOME']:
        render_welcome_scene()
    elif current_scene == SCENES['MOOD_SELECTION']:
        render_mood_selection_scene()
    elif current_scene == SCENES['LOCATION_INPUT']:
        render_location_input_scene()
    elif current_scene == 'custom_location':  # Special case for custom location
        render_custom_location_scene()
    elif current_scene == SCENES['LOADING']:
        render_loading_scene()
    elif current_scene == SCENES['RESULTS']:
        render_results_scene()
    elif current_scene == SCENES['CAFE_DETAILS']:
        render_cafe_details_scene()
    elif current_scene == SCENES['CHAT']:
        render_chat_scene()
    else:
        # Fallback to welcome scene
        st.error(f"Unknown scene: {current_scene}")
        navigate_to_scene(SCENES['WELCOME'])

if __name__ == "__main__":
    main()
