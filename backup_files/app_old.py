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
    
    # Debug info in sidebar (remove in production)
    render_debug_sidebar()

def render_debug_sidebar():
    """Render debug information in sidebar"""
    with st.sidebar:
        st.write("**🔧 Debug Info:**")
        st.write(f"**Current Scene:** {get_current_scene()}")
        st.write(f"**Selected Mood:** {st.session_state.get('selected_mood', 'None')}")
        st.write(f"**User Location:** {st.session_state.get('user_location', 'None')}")
        st.write(f"**Weather Data:** {'Available' if st.session_state.get('weather_data') else 'None'}")
        st.write(f"**Recommendation:** {'Generated' if st.session_state.get('drink_recommendation') else 'None'}")
        st.write(f"**Café Results:** {len(st.session_state.get('cafe_results', []))} found")
        st.write(f"**Chat History:** {len(st.session_state.get('chat_history', []))} messages")
        
        # Reset button for debugging
        if st.button("🔄 Reset App State"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        # Scene navigation for debugging
        st.write("**Quick Navigation:**")
        scenes = [
            ("Welcome", SCENES['WELCOME']),
            ("Mood", SCENES['MOOD_SELECTION']),
            ("Location", SCENES['LOCATION_INPUT']),
            ("Results", SCENES['RESULTS']),
            ("Cafés", SCENES['CAFE_DETAILS']),
            ("Chat", SCENES['CHAT'])
        ]
        
        for scene_name, scene_key in scenes:
            if st.button(f"→ {scene_name}", key=f"nav_{scene_key}"):
                navigate_to_scene(scene_key)

if __name__ == "__main__":
    main()
