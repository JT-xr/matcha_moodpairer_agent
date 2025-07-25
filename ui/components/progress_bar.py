"""
Progress Bar Component for Whiski App
Displays progress through the matcha recommendation flow.
"""

import streamlit as st

def render_progress_bar(step, total_steps=4):
    """
    Render a progress bar showing current step in the flow
    
    Args:
        step (int): Current step number (1-based)
        total_steps (int): Total number of steps in the flow
    """
    progress = (step / total_steps) * 100
    
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress}%;"></div>
    </div>
    <p style="text-align: center; color: #666; font-size: 14px;">Step {step} of {total_steps}</p>
    """, unsafe_allow_html=True)
