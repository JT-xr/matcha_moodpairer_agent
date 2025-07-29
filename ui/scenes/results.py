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
    
    if not BACKEND_AVAILABLE:
        st.error("Whiski agent is not available. Please check your configuration.")
        return {"drink": "Agent unavailable", "vibe": "Please try again later"}
    
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
        
        # Parse the agent response - handle both code-wrapped and direct formats
        import re
        
        # First, try to extract content from code blocks if present
        code_match = re.search(r'<code>(.*?)</code>', response, re.DOTALL)
        if code_match:
            # Extract the content inside code tags
            code_content = code_match.group(1)
            # Look for print statements
            print_matches = re.findall(r'print\(["\']([^"\']*)["\'][^)]*\)', code_content)
            if print_matches:
                # Join all print statements
                response = ' '.join(print_matches)
        
        # Now parse for drink and vibe from the cleaned response
        drink_match = re.search(r'Drink:\s*([^.]*\.?[^V]*?)(?=\s*Vibe:|$)', response, re.IGNORECASE)
        vibe_match = re.search(r'Vibe:\s*(.*?)(?=$)', response, re.DOTALL | re.IGNORECASE)
        
        if drink_match and vibe_match:
            ai_drink = drink_match.group(1).strip()
            ai_vibe = vibe_match.group(1).strip()
            return {"drink": ai_drink, "vibe": ai_vibe}
        else:
            # If structured parsing fails, try to extract any meaningful content
            if "matcha" in response.lower():
                # If response contains matcha content, use it as-is
                return {"drink": response[:50] + "..." if len(response) > 50 else response, 
                       "vibe": "Perfect matcha experience awaits! 🍵"}
            else:
                st.error(f"Unable to parse recommendation. Agent response: {response[:100]}...")
                return {"drink": "Parsing error", "vibe": "Please try again"}
        
    except Exception as e:
        st.error(f"Error getting AI recommendation: {e}")
        return {"drink": "Error occurred", "vibe": "Please try again"}

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
        
        # Get AI recommendation
        try:
            recommendation = get_ai_recommendation(mood, location, weather_data)
            if recommendation and 'drink' in recommendation and 'vibe' in recommendation:
                st.session_state.drink_recommendation = recommendation['drink']
                st.session_state.vibe_description = recommendation['vibe']
            else:
                st.error("Invalid recommendation format received")
                st.session_state.drink_recommendation = "Recommendation error"
                st.session_state.vibe_description = "Please try again"
        except Exception as e:
            st.error(f"Error generating recommendation: {e}")
            st.session_state.drink_recommendation = "Error occurred"
            st.session_state.vibe_description = "Please try again"
    
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
