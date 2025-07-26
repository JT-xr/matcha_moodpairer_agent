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
    
    # Render the green step progress bar (Step 3 of 4)
    render_progress_bar(3)
    
    # Use a container to ensure full control over the display
    with st.container():
        st.markdown("""
        <style>
        .loading-spinner {
            width: 60px;
            height: 60px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #557937ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
        
        <div style="text-align: center; padding: 50px 20px; min-height: 60vh; display: flex; flex-direction: column; justify-content: center;">
            <h2 style="font-size: 48px; margin-bottom: 30px; color: #557937ff;">🧠 Whiski is thinking...</h2>
            <p style="font-size: 20px; color: #666; margin-bottom: 40px;">
                Brewing the perfect matcha recommendation for you
            </p>
            <div class="loading-spinner"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Wait for a few seconds to simulate processing
        time.sleep(3)
        
        # Clear the loading flag
        if 'loading_started' in st.session_state:
            del st.session_state.loading_started
        
        # Navigate to results
        navigate_to_scene(SCENES['RESULTS'])
        st.rerun()
    st.rerun()
