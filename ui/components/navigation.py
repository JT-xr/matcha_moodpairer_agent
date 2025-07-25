"""
Navigation Component for Whiski App
Provides consistent navigation buttons across scenes.
"""

import streamlit as st
from ..utils import navigate_to_scene, SCENES, reset_session

def render_back_button(target_scene, label="← Back", key_suffix=""):
    """Render a back navigation button"""
    if st.button(label, key=f"back_{key_suffix}", use_container_width=True):
        navigate_to_scene(target_scene)

def render_continue_button(target_scene, label="Continue →", key_suffix="", button_type="primary", condition=True, error_message=""):
    """Render a continue navigation button with optional validation"""
    if st.button(label, key=f"continue_{key_suffix}", use_container_width=True, type=button_type):
        if condition:
            navigate_to_scene(target_scene)
        elif error_message:
            st.error(error_message)

def render_navigation_buttons(back_scene=None, back_label="← Back", 
                            continue_scene=None, continue_label="Continue →",
                            continue_condition=True, error_message="",
                            key_suffix="nav"):
    """Render standard back/continue navigation buttons"""
    col1, col2 = st.columns(2)
    
    if back_scene:
        with col1:
            render_back_button(back_scene, back_label, f"{key_suffix}_back")
    
    if continue_scene:
        with col2:
            render_continue_button(continue_scene, continue_label, f"{key_suffix}_continue", 
                                 condition=continue_condition, error_message=error_message)

def render_action_buttons(actions, key_suffix="action"):
    """
    Render multiple action buttons in columns
    
    Args:
        actions: List of dicts with keys: 'label', 'action', 'type' (optional), 'key' (optional)
        key_suffix: Suffix for button keys
    """
    if not actions:
        return
    
    cols = st.columns(len(actions))
    
    for i, action in enumerate(actions):
        with cols[i]:
            button_type = action.get('type', 'secondary')
            button_key = action.get('key', f"{key_suffix}_{i}")
            
            if st.button(action['label'], key=button_key, use_container_width=True, type=button_type):
                action['action']()

def render_reset_button(label="🔄 Start Over", key="reset_session"):
    """Render a button to reset the entire session"""
    if st.button(label, key=key, use_container_width=True):
        reset_session()
