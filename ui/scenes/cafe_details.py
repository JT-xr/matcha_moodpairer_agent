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
        return get_fallback_cafes(location)
    
    try:
        # Use real café search
        cafes = search_matcha_cafes(location)
        
        if not cafes:
            return get_fallback_cafes(location)
        
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
                'price_range': '$3-8',  # Default price range
                'phone': cafe.get('phone') or 'Phone not available'
            }
            formatted_cafes.append(formatted_cafe)
        
        return formatted_cafes
        
    except Exception as e:
        st.error(f"Error searching for cafés: {e}")
        return get_fallback_cafes(location)

def get_fallback_cafes(location):
    """Fallback café data when backend is unavailable - limited to 5 results"""
    location_lower = location.lower() if location else "brooklyn, ny"
    
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
    
    if "culver city" in location_lower or "california" in location_lower:
        cafes = [
            {
                "name": "Matcha & Co Culver City",
                "address": "9600 Culver Blvd, Culver City, CA",
                "rating": 4.7,
                "phone": "(424) 555-0156"
            },
            {
                "name": "Venice Beach Matcha House",
                "address": "1234 Washington Blvd, Culver City, CA", 
                "rating": 4.5,
                "phone": "(424) 555-0287"
            },
            {
                "name": "Green Garden Tea",
                "address": "4567 Sepulveda Blvd, Culver City, CA",
                "rating": 4.8,
                "phone": "(424) 555-0398"
            },
            {
                "name": "Westside Matcha Co",
                "address": "7890 West Blvd, Culver City, CA",
                "rating": 4.6,
                "phone": "(424) 555-0409"
            },
            {
                "name": "Pacific Matcha Studio",
                "address": "1111 Jefferson Blvd, Culver City, CA",
                "rating": 4.4,
                "phone": "(424) 555-0510"
            }
        ]
    elif "manhattan" in location_lower or "new york" in location_lower:
        cafes = [
            {
                "name": "Soho Matcha House",
                "address": "456 Broadway, New York, NY",
                "rating": 4.8,
                "phone": "(212) 555-0234"
            },
            {
                "name": "West Village Tea Co",
                "address": "123 Bleecker St, New York, NY", 
                "rating": 4.6,
                "phone": "(212) 555-0345"
            },
            {
                "name": "Central Park Matcha",
                "address": "321 Central Park West, New York, NY",
                "rating": 4.9,
                "phone": "(212) 555-0456"
            },
            {
                "name": "East Village Zen Tea",
                "address": "789 St Marks Pl, New York, NY",
                "rating": 4.5,
                "phone": "(212) 555-0567"
            },
            {
                "name": "Chelsea Market Matcha",
                "address": "75 9th Ave, New York, NY",
                "rating": 4.7,
                "phone": "(212) 555-0678"
            }
        ]
    elif "queens" in location_lower:
        cafes = [
            {
                "name": "Astoria Matcha Corner",
                "address": "123 30th Ave, Astoria, NY",
                "rating": 4.5,
                "phone": "(718) 555-0567"
            },
            {
                "name": "Flushing Tea Garden",
                "address": "456 Northern Blvd, Flushing, NY", 
                "rating": 4.7,
                "phone": "(718) 555-0678"
            },
            {
                "name": "Long Island City Brew",
                "address": "789 Queens Plaza, LIC, NY",
                "rating": 4.4,
                "phone": "(718) 555-0789"
            },
            {
                "name": "Forest Hills Matcha",
                "address": "321 Austin St, Forest Hills, NY",
                "rating": 4.6,
                "phone": "(718) 555-0890"
            },
            {
                "name": "Jackson Heights Tea",
                "address": "654 Roosevelt Ave, Jackson Heights, NY",
                "rating": 4.3,
                "phone": "(718) 555-0901"
            }
        ]
    else:  # Default to Brooklyn
        cafes = [
            {
                "name": "Park Slope Matcha",
                "address": "789 7th Ave, Brooklyn, NY",
                "rating": 4.6,
                "phone": "(718) 555-0123"
            },
            {
                "name": "Williamsburg Green Tea",
                "address": "234 Bedford Ave, Brooklyn, NY",
                "rating": 4.8,
                "phone": "(718) 555-0234"
            },
            {
                "name": "DUMBO Matcha House",
                "address": "567 Water St, Brooklyn, NY",
                "rating": 4.7,
                "phone": "(718) 555-0345"
            },
            {
                "name": "Red Hook Tea Co",
                "address": "890 Van Brunt St, Brooklyn, NY",
                "rating": 4.5,
                "phone": "(718) 555-0456"
            },
            {
                "name": "Crown Heights Zen",
                "address": "432 Franklin Ave, Brooklyn, NY",
                "rating": 4.4,
                "phone": "(718) 555-0567"
            }
        ]
    
    # Add varied descriptions and remove distance
    for i, cafe in enumerate(cafes):
        cafe.update({
            'distance': '',  # Remove distance text
            'speciality': specialities[i % len(specialities)],
            'atmosphere': atmospheres[i % len(atmospheres)],
            'price_range': '$3-8'
        })
    
    return cafes

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
    
    # Show warning only if backend is not available
    if not CAFE_SEARCH_AVAILABLE:
        st.info("🔄 Using sample café data - real search temporarily unavailable")
    
    # Force regenerate café results if empty or not present
    if 'cafe_results' not in st.session_state or not st.session_state.cafe_results:
        with st.spinner("Finding the best matcha cafés for you..."):
            cafe_results = get_real_cafe_results(location, mood)
            st.session_state.cafe_results = cafe_results
    
    cafes = st.session_state.cafe_results
    
    # TEMPORARY FIX: Always show Brooklyn cafés for testing
    if not cafes or len(cafes) == 0:
        cafes = [
            {
                "name": "Matcha Zen Brooklyn",
                "address": "245 Court St, Brooklyn, NY",
                "rating": 4.8,
                "distance": "0.3 miles",
                "speciality": "Traditional ceremonial matcha",
                "atmosphere": "Quiet, minimalist, perfect for reflection",
                "price_range": "$$",
                "phone": "(718) 555-0123"
            },
            {
                "name": "Green Tea House",
                "address": "156 Atlantic Ave, Brooklyn, NY", 
                "rating": 4.6,
                "distance": "0.7 miles",
                "speciality": "Artisanal matcha lattes",
                "atmosphere": "Cozy corner nooks, ambient lighting",
                "price_range": "$$$",
                "phone": "(718) 555-0456"
            },
            {
                "name": "Brooklyn Matcha Co",
                "address": "89 Smith St, Brooklyn, NY",
                "rating": 4.7,
                "distance": "1.0 miles",
                "speciality": "Creative matcha cocktails",
                "atmosphere": "Vibrant, artistic, Instagram-worthy",
                "price_range": "$$",
                "phone": "(718) 555-0789"
            },
            {
                "name": "Tea & Tranquility",
                "address": "312 Flatbush Ave, Brooklyn, NY",
                "rating": 4.5,
                "distance": "1.2 miles",
                "speciality": "Matcha bubble tea",
                "atmosphere": "Modern, spacious, perfect for groups",
                "price_range": "$",
                "phone": "(718) 555-0234"
            }
        ]
        st.session_state.cafe_results = cafes
    
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
