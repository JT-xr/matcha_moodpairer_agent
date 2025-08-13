"""
Card Components for Whiski App
Provides reusable card layouts for recommendations and café details.
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from styles import get_recommendation_card_style, get_cafe_card_style

def render_recommendation_card(drink, vibe, title="Whiski's Choice"):
    """
    Render a recommendation card with drink and vibe information
    
    Args:
        drink (str): The recommended drink description
        vibe (str): The vibe/atmosphere description  
        title (str): Card title
    """
    st.markdown(f"""
    <div style="{get_recommendation_card_style()}">
        <h3 style="color: #2c3e50; margin-top: 0; text-align: center;">{title}</h3>
        <div style="background: #e8f5e8; padding: 10px; border-radius: 8px; margin: 10px 0;">
            <strong>🍵 Drink:</strong> {drink}
        </div>
        <div style="background: #fff; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <strong>✨ Vibe:</strong><br>
            {vibe}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_cafe_card(cafe_data, card_index=0):
    """
    Render a café information card
    
    Args:
        cafe_data (dict): Dictionary containing café information
        card_index (int): Index for unique button keys
    """
    st.markdown(f"""
    <div style="{get_cafe_card_style()}">
        <h4 style="color: #2c3e50; margin: 0 0 10px 0; font-size: 20px;">
            {cafe_data['name']} 
            <span style="color: #4CAF50;">⭐ {cafe_data['rating']}</span>
        </h4>
        <p style="color: #666; margin: 5px 0; font-size: 14px;">
            📍 {cafe_data['address']}{' • <strong>' + cafe_data['distance'] + '</strong>' if cafe_data['distance'] else ''}
        </p>
        <p style="color: #4CAF50; margin: 5px 0; font-weight: bold; font-size: 15px;">
            🍵 {cafe_data['speciality']}
        </p>
        <p style="color: #888; margin: 5px 0; font-style: italic; font-size: 14px;">
            "{cafe_data['atmosphere']}"
        </p>
        <p style="color: #333; margin: 5px 0; font-size: 14px;">
            💰 {cafe_data['price_range']} • 📞 {cafe_data['phone']}
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_loading_card(title, subtitle, progress_value=None):
    """
    Render a loading/processing card
    
    Args:
        title (str): Main loading message
        subtitle (str): Additional context
        progress_value (int): Optional progress bar value (0-100)
    """
    st.markdown(f"""
    <div class="scene-container">
        <h2 style="font-size: 48px; margin-bottom: 30px;">{title}</h2>
        <p style="font-size: 20px; color: #666; margin-bottom: 40px;">
            {subtitle}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if progress_value is not None:
        st.progress(progress_value)
