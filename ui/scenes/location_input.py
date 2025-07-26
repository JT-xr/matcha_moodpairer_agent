"""
Location Input Scene for Whiski App
Allows users to select or enter their location.
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from styles import get_scene_header_style
from ..components.progress_bar import render_progress_bar
from ..components.buttons import render_location_button_list
from ..components.navigation import render_navigation_buttons
from ..utils import SCENES, navigate_to_scene

def render_location_input_scene():
    """Render the location input scene"""
    # Don't render if we're transitioning to another scene
    if st.session_state.get('transitioning', False):
        return
        
    render_progress_bar(2)
    
    # Scene header
    st.markdown(get_scene_header_style(
        "📍 Where are you?",
        "Select your location to find nearby matcha cafés"
    ), unsafe_allow_html=True)
    
    # Location options
    locations = ["Brooklyn, NY", "Manhattan, NY", "Queens, NY", "Other Location"]
    
    # Render location button list
    render_location_button_list(
        locations, 
        target_scene=SCENES['LOADING'],
        custom_scene='custom_location'
    )
    
    # Back button
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("← Back to Mood", key="back_location"):
            navigate_to_scene(SCENES['MOOD_SELECTION'])

def render_custom_location_scene():
    """Render the custom location input scene"""
    # Don't render if we're transitioning to another scene
    if st.session_state.get('transitioning', False):
        return
        
    render_progress_bar(2)
    
    # Scene header with current mood context
    current_mood = st.session_state.get('selected_mood', 'your current')
    st.markdown(f"""
    <div class="scene-container">
        <h2 style="font-size: 48px; margin-bottom: 20px;">📍 Enter your location</h2>
        <p style="font-size: 20px; color: #666; margin-bottom: 40px;">
            You're feeling <strong>{current_mood}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom location input
    custom_loc = st.text_input(
        "Type your location:", 
        placeholder="e.g., San Francisco, CA",
        key="custom_location_input"
    )
    
    # Navigation buttons
    st.markdown("<br>", unsafe_allow_html=True)
    render_navigation_buttons(
        back_scene=SCENES['LOCATION_INPUT'],
        back_label="← Back",
        continue_scene=SCENES['LOADING'],
        continue_label="Continue →",
        continue_condition=bool(custom_loc.strip()),
        error_message="Please enter a location",
        key_suffix="custom_location"
    )
    
    # Store custom location if provided
    if custom_loc.strip():
        st.session_state.user_location = custom_loc
        # Also set legacy key for compatibility
        st.session_state.selected_location = custom_loc
