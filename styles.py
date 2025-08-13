"""
Styles Module for Whiski Matcha Mood Pairer
Contains all CSS styling and UI configuration for the Streamlit app.
"""

import streamlit as st

def apply_global_styles():
    """Apply global CSS styles to the Streamlit app"""
    st.markdown("""
    <style>
        .scene-container {
            text-align: center;
            padding: 50px 20px;
            min-height: 60vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .mood-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 15px;
            padding: 20px;
            margin: 10px;
            font-size: 18px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .location-button {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 15px 30px;
            margin: 8px;
            font-size: 16px;
            width: 100%;
        }
        
        .start-button {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 15px 40px;
            font-size: 20px;
            font-weight: bold;
        }
        
        .progress-bar {
            height: 4px;
            background: #e0e0e0;
            border-radius: 2px;
            margin: 20px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #66BB6A);
            border-radius: 2px;
            transition: width 0.3s ease;
        }
    </style>
    """, unsafe_allow_html=True)

def apply_welcome_styles():
    """Apply styles specific to the welcome/splash scene"""
    st.markdown(
        """
        <style>
          .stApp {
            background-color: #bdcb9aff;
          }
          .splash-img {
            display: flex;
            justify-content: center;
            align-items: top;
            height: 100vh;
          }
          .splash-img > img {
            width: 75vw;
            height: 75vh;
            object-fit: cover;
          }
          .start-splash-button {
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            padding: 0.75rem 3rem;
            font-size: 1.5rem;
            background-color: white;
            color: black;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 1000;
          }
          .start-splash-button:hover {
            transform: translateX(-50%) translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

def hide_streamlit_ui():
    """Hide default Streamlit UI elements"""
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def get_scene_header_style(title, subtitle="", font_size="48px"):
    """Generate consistent header styling for scenes"""
    return f"""
    <div style="text-align: center; padding: 20px 20px 30px 20px;">
        <h2 style="font-size: {font_size}; margin-bottom: 15px;">{title}</h2>
        {f'<p style="font-size: 20px; color: #666; margin-bottom: 30px;">{subtitle}</p>' if subtitle else ''}
    </div>
    """

def get_recommendation_card_style():
    """Styling for recommendation display cards"""
    return """
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 10px solid #557937ff;
        height: 100%;
        margin-bottom: 40px;  /* Add significant bottom spacing for mobile */
    """

def get_cafe_card_style():
    """Styling for café result cards"""
    return """
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    """

def get_drink_recommendation_style():
    """Styling for drink recommendation sections"""
    return """
        background: #e8f5e8;
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
    """

def get_vibe_description_style():
    """Styling for vibe description sections"""
    return """
        background: #fff;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    """

# Color palette constants
class Colors:
    PRIMARY_GREEN = "#4CAF50"
    SECONDARY_GREEN = "#66BB6A"
    BACKGROUND_GREEN = "#bdcb9aff"
    ACCENT_GREEN = "#557937ff"
    TEXT_GRAY = "#666"
    DARK_TEXT = "#2c3e50"
    LIGHT_BACKGROUND = "#f8f9fa"
    SUCCESS_GREEN = "#e8f5e8"
    CARD_SHADOW = "rgba(0,0,0,0.1)"
    BUTTON_SHADOW = "rgba(0,0,0,0.2)"

# Font size constants
class FontSizes:
    HERO_TITLE = "60px"
    SCENE_TITLE = "48px"
    SECTION_TITLE = "42px"
    SUBTITLE = "20px"
    BODY_TEXT = "18px"
    SMALL_TEXT = "14px"
    BUTTON_TEXT = "16px"
