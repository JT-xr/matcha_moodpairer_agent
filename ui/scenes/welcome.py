"""
Welcome Scene for Whiski App
Displays the splash page and start button.
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from styles import apply_welcome_styles
from ..components.buttons import render_start_button
from ..utils import SCENES

def render_welcome_scene():
    """Render the welcome/splash scene"""
    # Apply welcome-specific styles
    apply_welcome_styles()
    
    # Full-screen splash image
    try:
        st.image("Welcome_Image2.PNG", use_container_width=True)
    except:
        st.error("Welcome image (Welcome_Image2.PNG) not found. Please check your assets.")

    # Custom styled start button positioned at bottom
    st.markdown(
        """
        <div style="position: fixed; bottom: 2rem; left: 50%; transform: translateX(-50%); z-index: 1000;">
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Render start button
    render_start_button(SCENES['MOOD_SELECTION'])
