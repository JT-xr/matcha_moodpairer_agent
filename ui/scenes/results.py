"""
Results Scene for Whiski App
Displays AI-generated matcha recommendations using real backend integration.
"""

import streamlit as st
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from styles import get_scene_header_style
from ..components.progress_bar import render_progress_bar
from ..components.cards import render_recommendation_card, render_loading_card
from ..components.navigation import render_action_buttons
from ..utils import SCENES, navigate_to_scene

# Import real backend modules
try:
    from whiski_agent import agent  # Import the actual agent instance
    from weather_api import get_nyc_weather
    # from mood_drink_map import get_drink_for_mood  # No longer needed since agent provides drink
    BACKEND_AVAILABLE = True
except ImportError as e:
    BACKEND_AVAILABLE = False
    # Backend modules not available - will use fallback mode

def get_ai_recommendation(mood, location, weather_data=None):
    """
    Get AI recommendation using real Whiski agent and the proper template
    
    Args:
        mood (str): Selected mood
        location (str): User location
        weather_data (dict): Weather information
    
    Returns:
        dict: Recommendation with 'drink' and 'vibe' keys
    """
    
    # Try to get AI-generated recommendation using template
    if BACKEND_AVAILABLE:
        try:
            # Get weather context
            weather_context = get_nyc_weather() if weather_data is None else weather_data
            
            # Load and fill the prompt template
            import os
            template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates", "prompt_template_gemini.txt")
            with open(template_path, "r") as tf:
                template = tf.read()
                
            # Fill template with actual values
            filled_task = template.format(
                mood=mood,
                location=location,
                weather=weather_context
            )
            
            # Get response from agent
            response = agent.run(filled_task)
            
            # Parse the agent response to extract drink and vibe
            import re
            drink_match = re.search(r'Drink:\s*([^.]*\.?[^V]*?)(?=\s*Vibe:|$)', response)
            vibe_match = re.search(r'Vibe:\s*(.*?)(?=$)', response, re.DOTALL)
            
            if drink_match and vibe_match:
                ai_drink = drink_match.group(1).strip()
                ai_vibe = vibe_match.group(1).strip()
                return {"drink": ai_drink, "vibe": ai_vibe}
            else:
                # If parsing fails, use fallback
                return get_fallback_recommendation(mood)
            
        except Exception as e:
            # Use fallback if agent fails
            return get_fallback_recommendation(mood)
    else:
        # Backend not available, use full fallback
        return get_fallback_recommendation(mood)

def get_fallback_recommendation(mood):
    """Fallback recommendations when backend is unavailable"""
    fallback_recommendations = {
        "chill": {
            "drink": "Iced Lavender Matcha Latte 💜 - creamy, refreshing, and calming",
            "vibe": "Imagine yourself in a sleek, minimalist café in a quiet corner. Soft jazz plays while sunlight streams through large windows, creating the perfect peaceful atmosphere to unwind. 🌿✨"
        },
        "anxious": {
            "drink": "Warm Ceremonial Matcha 🍵 - pure, grounding, and meditative",
            "vibe": "Picture a serene tea house with bamboo accents and gentle instrumental music. The ritual of preparing matcha helps center your mind and ease your worries. 🧘‍♀️🌱"
        },
        "creative": {
            "drink": "Matcha Rose Latte 🌹 - inspiring, floral, and artistic",
            "vibe": "Envision a vibrant café filled with local art, colorful cushions, and the gentle hum of creative energy. Natural light pours in, perfect for sketching or writing. 🎨✨"
        },
        "reflective": {
            "drink": "Traditional Matcha Tea 🍃 - pure, contemplative, and authentic",
            "vibe": "Find yourself in a quiet corner of a traditional tea room, surrounded by books and soft lighting. The perfect space for deep thoughts and peaceful contemplation. 📚🕯️"
        },
        "energized": {
            "drink": "Matcha Lemonade ⚡ - zesty, refreshing, and invigorating",
            "vibe": "Picture a bright, modern café with upbeat music and bustling energy. Large communal tables and standing desks create the perfect environment for productivity. 💪🌟"
        },
        "cozy": {
            "drink": "Warm Matcha with Oat Milk ☕ - comforting, rich, and nurturing",
            "vibe": "Imagine a snug café with plush armchairs, warm lighting, and the gentle sound of rain outside. Soft blankets and the aroma of fresh pastries complete the cozy atmosphere. 🛋️🕯️"
        }
    }
    return fallback_recommendations.get(mood, fallback_recommendations["chill"])

def show_loading_process():
    """Show loading animation while processing recommendation"""
    render_loading_card(
        "🧠 Whiski is thinking...",
        "Brewing the perfect matcha recommendation for you"
    )
    
    # Loading animation
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    messages = [
        "Analyzing your mood...",
        "Checking local weather...",
        "Consulting matcha expertise...",
        "Crafting your perfect recommendation..."
    ]
    
    for i, message in enumerate(messages):
        status_text.text(message)
        progress_bar.progress((i + 1) * 25)
        time.sleep(0.8)
    
    return True

def render_results_scene():
    """Render the results/recommendation scene"""
    # Check if we need to generate recommendation
    if 'drink_recommendation' not in st.session_state or st.session_state.drink_recommendation is None:
        # Get user data first
        mood = st.session_state.get('selected_mood', 'chill')
        location = st.session_state.get('user_location', 'Unknown')
        
        # Get weather data
        weather_data = None
        if BACKEND_AVAILABLE:
            try:
                weather_data = get_nyc_weather()  # Get current NYC weather
                st.session_state.weather_data = weather_data
            except Exception as e:
                # Weather API failed - continue without weather data
                pass
        
        # Get AI recommendation (with fallback)
        try:
            recommendation = get_ai_recommendation(mood, location, weather_data)
            if recommendation and 'drink' in recommendation and 'vibe' in recommendation:
                st.session_state.drink_recommendation = recommendation['drink']
                st.session_state.vibe_description = recommendation['vibe']
            else:
                raise Exception("Invalid recommendation format")
        except Exception as e:
            # Force fallback
            fallback = get_fallback_recommendation(mood)
            st.session_state.drink_recommendation = fallback['drink'] 
            st.session_state.vibe_description = fallback['vibe']
    
    # Show progress bar
    render_progress_bar(4)
    
    # Scene header
    st.markdown("""
    <div style="text-align: center; padding: 30px;">
        <h1 style="color: #557937ff; font-size: 60px; margin-bottom: 20px;">🎉 Perfect Match(a)!</h1>
        <p style="font-size: 20px; color: #666;">Here's your personalized matcha experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add separator line
    st.markdown("---")
    
    # Display results layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Render recommendation card
        drink = st.session_state.get('drink_recommendation') or "Matcha recommendation loading..."
        vibe = st.session_state.get('vibe_description') or "Perfect vibe coming right up!"
        

        
        render_recommendation_card(drink, vibe)
    
    with col2:
        # Display matcha image
        try:
            st.image("matcha_cafe.png", caption="Matcha Vibe", width=400)
        except:
            # Fallback to online image if local file doesn't exist
            st.image("https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400", 
                    caption="Matcha Vibe", width=400)
    
    # Action buttons
    st.markdown("<br><br>", unsafe_allow_html=True)
    actions = [
        {
            'label': '🔄 Try Again',
            'action': lambda: reset_and_restart(),
            'key': 'try_again'
        },
        {
            'label': '📍 Find Cafés',
            'action': lambda: navigate_to_scene(SCENES['CAFE_DETAILS']),
            'type': 'primary',
            'key': 'find_cafes'
        },
        {
            'label': '💬 Chat',
            'action': lambda: navigate_to_scene(SCENES['CHAT']),
            'key': 'chat'
        }
    ]
    
    render_action_buttons(actions, "results")

def reset_and_restart():
    """Reset session and start over"""
    # Clear recommendation data
    for key in ['drink_recommendation', 'vibe_description', 'weather_data']:
        if key in st.session_state:
            del st.session_state[key]
    
    # Navigate to welcome
    navigate_to_scene(SCENES['WELCOME'])
