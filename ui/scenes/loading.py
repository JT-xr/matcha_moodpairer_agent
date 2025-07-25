"""
Loading Scene for Whiski App
Displays the "Whiski is thinking..." animation while processing recommendations.
"""

import streamlit as st
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from styles import get_scene_header_style
from ..components.progress_bar import render_progress_bar
from ..utils import SCENES, navigate_to_scene

def render_loading_scene():
    """Render the loading/processing scene"""
    # Force a clean UI state
    if 'loading_started' not in st.session_state:
        st.session_state.loading_started = True
        st.rerun()
    
    render_progress_bar(3)
    
    # Use a container to ensure full control over the display
    with st.container():
        st.markdown("""
        <div style="text-align: center; padding: 50px 20px; min-height: 60vh; display: flex; flex-direction: column; justify-content: center;">
            <h2 style="font-size: 48px; margin-bottom: 30px; color: #557937ff;">🧠 Whiski is thinking...</h2>
            <p style="font-size: 20px; color: #666; margin-bottom: 40px;">
                Brewing the perfect matcha recommendation for you
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Loading animation
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        messages = [
            "Analyzing your mood...",
            "Checking local weather...",
            "Finding nearby cafés...",
            "Crafting your perfect recommendation..."
        ]
        
        # Animate through the loading messages
        for i, message in enumerate(messages):
            status_text.text(message)
            progress_bar.progress((i + 1) * 25)
            time.sleep(0.8)
        
        # Clear the loading elements
        progress_bar.empty()
        status_text.empty()
        
        # Clear the loading flag
        if 'loading_started' in st.session_state:
            del st.session_state.loading_started
        
        # Navigate to results
        navigate_to_scene(SCENES['RESULTS'])
        st.rerun()
    st.rerun()
