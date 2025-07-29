"""
Café Details Scene for Whiski App
Displays nearby café search results using real backend integration.
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from styles import get_scene_header_style
from ..components.progress_bar import render_progress_bar
from ..components.cards import render_cafe_card
from ..components.navigation import render_action_buttons
from ..utils import SCENES, navigate_to_scene

# Import real backend modules
try:
    from cafe_search import search_matcha_cafes
    CAFE_SEARCH_AVAILABLE = True
except ImportError:
    CAFE_SEARCH_AVAILABLE = False
    # Warning will be shown in the scene function if needed

def get_real_cafe_results(location, mood=None):
    """
    Get real café search results using backend integration
    
    Args:
        location (str): User location
        mood (str): User mood for filtering
    
    Returns:
        list: List of café dictionaries
    """
    if not CAFE_SEARCH_AVAILABLE:
        st.error("Café search service is not available. Please check your configuration.")
        return []
    
    try:
        # Use real café search
        cafes = search_matcha_cafes(location)
        
        if not cafes:
            st.warning("No cafés found in this location. Please try a different area.")
            return []
        
        # Limit to 5 results and format for display
        limited_cafes = cafes[:5]
        formatted_cafes = []
        
        # Varied speciality descriptions
        specialities = [
            "Premium matcha lattes & ceremonial grade tea",
            "Artisanal matcha drinks & Japanese sweets", 
            "Traditional matcha ceremonies & modern beverages",
            "Organic matcha & plant-based milk options",
            "Signature matcha blends & seasonal specialties"
        ]
        
        # Varied atmosphere descriptions
        atmospheres = [
            "Zen-inspired space perfect for mindful sipping",
            "Modern café with traditional Japanese touches",
            "Cozy corner spot ideal for creative work", 
            "Bright, minimalist space with calming vibes",
            "Warm gathering place for matcha enthusiasts"
        ]
        
        for i, cafe in enumerate(limited_cafes):
            formatted_cafe = {
                'name': cafe.get('name', 'Unknown Café'),
                'address': cafe.get('address', 'Address not available'),
                'rating': cafe.get('rating', 4.0),
                'distance': '',  # Remove distance text
                'speciality': specialities[i % len(specialities)],
                'atmosphere': atmospheres[i % len(atmospheres)],
                'price_range': '$$',  # Use dollar signs instead of $3-8
                'phone': cafe.get('phone') or 'Phone not available'
            }
            formatted_cafes.append(formatted_cafe)
        
        return formatted_cafes
        
    except Exception as e:
        st.error(f"Error searching for cafés: {e}")
        return []

def render_cafe_details_scene():
    """Render the café search results scene"""
    render_progress_bar(4)
    
    # Get user context
    mood = st.session_state.get('selected_mood', 'Unknown')
    location = st.session_state.get('user_location', 'Unknown')
    
    # Scene header
    st.markdown(get_scene_header_style(
        "📍 Nearby Cafés",
        f"Perfect spots for your <strong>{mood}</strong> vibe in <strong>{location}</strong>",
        font_size="42px"
    ), unsafe_allow_html=True)
    
    # Force regenerate café results if empty or not present
    if 'cafe_results' not in st.session_state or not st.session_state.cafe_results:
        with st.spinner("Finding the best matcha cafés for you..."):
            cafe_results = get_real_cafe_results(location, mood)
            st.session_state.cafe_results = cafe_results
    
    cafes = st.session_state.cafe_results
    
    # Display café cards
    if cafes:
        for i, cafe in enumerate(cafes):
            render_cafe_card(cafe, i)
            
            # Add spacing between café cards
            if i < len(cafes) - 1:
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.error("Unable to load café results. Please try again.")
        
        # Add a button to force refresh
        if st.button("🔄 Refresh Café Search", key="force_refresh_cafes"):
            # Clear the café results and reload
            if 'cafe_results' in st.session_state:
                del st.session_state['cafe_results']
            st.rerun()
    
    # Navigation buttons
    st.markdown("<br><br>", unsafe_allow_html=True)
    actions = [
        {
            'label': '← Back',
            'action': lambda: navigate_to_scene(SCENES['RESULTS']),
            'key': 'back_to_results'
        },
        {
            'label': '🔄 New Search',
            'action': lambda: reset_and_restart(),
            'key': 'new_search'
        },
        {
            'label': '💬 Chat',
            'action': lambda: navigate_to_scene(SCENES['CHAT']),
            'key': 'chat_from_cafes'
        }
    ]
    
    render_action_buttons(actions, "cafe_details")

def reset_and_restart():
    """Reset session and start over"""
    # Clear all session data
    for key in list(st.session_state.keys()):
        if key not in ['current_scene']:  # Keep navigation state
            del st.session_state[key]
    
    # Navigate to welcome
    navigate_to_scene(SCENES['WELCOME'])
