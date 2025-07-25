"""
Welcome Scene for Whiski App
Displays the splash page and start button.
"""

import streamlit as st
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
        # Fallback if image not found
        st.markdown("""
        <div class="scene-container">
            <h1 style="color: #4CAF50; font-size: 60px; margin-bottom: 20px;">Whiski</h1>
            <p style="font-size: 24px; color: #666; margin-bottom: 20px;">
                Your AI matcha mood pairer
            </p>
            <h1 style="font-size: 80px; text-align: center; margin: 20px 0;">🍵</h1>
        </div>
        """, unsafe_allow_html=True)

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
