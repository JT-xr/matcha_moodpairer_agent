"""
Results Scene for Whiski App
Displays AI-generated matcha recommendations using real backend integration.
"""

import streamlit as st
import time
import sys
import os
from langfuse import observe
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

@observe(name="pairing_workflow", as_type="workflow")
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
        
        # Parse the agent response - handle the actual format the agent uses
        import re
        
        # Check if this is a conversational response rather than a recommendation
        conversational_patterns = [
            r"glad i could help",
            r"is there another",
            r"would you like",
            r"anything else",
            r"other mood",
            r"follow.?up"
        ]
        
        is_conversational = any(re.search(pattern, response, re.IGNORECASE) for pattern in conversational_patterns)
        
        if is_conversational:
            # This is a conversational response, not a recommendation
            # Try to re-prompt with a more direct approach
            direct_prompt = f"Recommend a specific matcha drink and café vibe for someone feeling {mood} in {location} with {weather_context} weather. Format: **The Drink:** [recommendation] **The Vibe:** [description]"
            response = agent.run(direct_prompt)
        
        # Method 1: Extract drink and vibe from the structured format
        drink_match = re.search(r'\*\*(?:The )?Drink:\*\*\s*(.*?)(?=\*\*(?:The )?Vibe:|\n\n|$)', response, re.DOTALL | re.IGNORECASE)
        vibe_match = re.search(r'\*\*(?:The )?Vibe:\*\*\s*(.*?)(?=$)', response, re.DOTALL | re.IGNORECASE)
        
        if drink_match and vibe_match:
            drink_text = drink_match.group(1).strip()
            vibe_text = vibe_match.group(1).strip()
            
            # Clean up the text (remove extra asterisks and formatting)
            drink_clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', drink_text)
            vibe_clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', vibe_text)
            
            # Validate that we got actual recommendations, not questions
            if (len(drink_clean.strip()) > 10 and 
                "matcha" in drink_clean.lower() and 
                len(vibe_clean.strip()) > 10 and
                not any(pattern in drink_clean.lower() for pattern in ["another", "other", "would you", "anything else"])):
                
                return {
                    "drink": drink_clean.strip(),
                    "vibe": vibe_clean.strip()
                }
        
        # Method 2: Try alternative patterns (fallback)
        drink_alt = re.search(r'drink:\s*(.*?)(?=vibe:|$)', response, re.DOTALL | re.IGNORECASE)
        vibe_alt = re.search(r'vibe:\s*(.*?)(?=$)', response, re.DOTALL | re.IGNORECASE)
        
        if drink_alt and vibe_alt:
            drink_text = drink_alt.group(1).strip()
            vibe_text = vibe_alt.group(1).strip()
            
            if (len(drink_text) > 10 and "matcha" in drink_text.lower() and len(vibe_text) > 10):
                return {
                    "drink": drink_text,
                    "vibe": vibe_text
                }
        
        # Method 3: If response contains matcha content but no clear structure
        if "matcha" in response.lower():
            # Extract any matcha-related content but provide a generic structure
            matcha_content = re.findall(r'[^.]*matcha[^.]*\.?', response, re.IGNORECASE)
            if matcha_content:
                return {
                    "drink": matcha_content[0][:80] + ("..." if len(matcha_content[0]) > 80 else ""),
                    "vibe": f"A perfect {mood} atmosphere in {location} to enjoy your matcha! 🍵"
                }
        
        # If all parsing fails, show what the agent actually returned
        st.error(f"Agent did not provide structured recommendation. Raw response: {response[:200]}...")
        return {"drink": "Agent parsing failed", "vibe": "Agent did not provide proper format"}
        
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
                # Validate we got actual recommendations, not error messages
                drink = recommendation['drink']
                vibe = recommendation['vibe']
                
                # Check if we got valid recommendations (but don't auto-retry)
                if (drink and vibe and 
                    len(drink.strip()) > 5 and len(vibe.strip()) > 5 and
                    drink != "Parsing error" and vibe != "Please try again" and
                    drink != "Agent parsing failed"):
                    
                    st.session_state.drink_recommendation = drink
                    st.session_state.vibe_description = vibe
                else:
                    # Show the actual agent failure instead of retrying
                    st.error(f"Agent failed to provide valid recommendation. Drink: {drink}, Vibe: {vibe}")
                    st.session_state.drink_recommendation = drink
                    st.session_state.vibe_description = vibe
            else:
                st.error("Agent did not return proper recommendation format")
                st.session_state.drink_recommendation = "Agent format error"
                st.session_state.vibe_description = "Agent did not respond correctly"
        except Exception as e:
            st.error(f"Agent error: {e}")
            st.session_state.drink_recommendation = f"Agent exception: {str(e)[:50]}"
            st.session_state.vibe_description = "Agent failed to respond"
    
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
            st.error("Matcha image (matcha_cafe.png) not found. Please check your assets.")
    
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
