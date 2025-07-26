"""
Chat Scene for Whiski App
Provides interactive chat with the AI agent using real backend integration.
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from styles import get_scene_header_style
from ..components.progress_bar import render_progress_bar
from ..components.navigation import render_action_buttons
from ..utils import SCENES, navigate_to_scene

# Import real backend modules
try:
    from whiski_agent import agent  # Import the agent instance directly like in original
    AGENT_AVAILABLE = True
except ImportError:
    AGENT_AVAILABLE = False
    st.warning("Whiski agent not available - using fallback mode")

def get_ai_response(prompt, context=None):
    """
    Get AI response using real Whiski agent (same as original backup)
    
    Args:
        prompt (str): User's message
        context (dict): Current session context
    
    Returns:
        str: AI response
    """
    if not AGENT_AVAILABLE:
        return get_fallback_response(prompt)
    
    try:
        # Use agent directly like in the original backup
        response = agent.run(prompt)
        return response
        
    except Exception as e:
        st.error(f"Error getting AI response: {e}")
        return get_fallback_response(prompt)

def get_fallback_response(prompt):
    """Fallback responses when agent is unavailable"""
    import random
    
    # Simple keyword-based responses
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ['hello', 'hi', 'hey']):
        return "Hi there! I'm Whiski 🍵 I'm here to help you with all things matcha! What would you like to know?"
    
    elif any(word in prompt_lower for word in ['recommend', 'suggestion', 'advice']):
        return "Based on your preferences, I'd suggest trying different matcha preparations to find what suits your mood best! Would you like specific recommendations?"
    
    elif any(word in prompt_lower for word in ['café', 'cafe', 'location', 'where']):
        return "I can help you find great matcha cafés! The ones I found for you should have the perfect atmosphere for your current vibe. Have you checked them out?"
    
    elif any(word in prompt_lower for word in ['weather', 'temperature', 'hot', 'cold']):
        return "Weather definitely affects the perfect matcha choice! Hot drinks for cozy weather, iced options for warm days. What's the weather like where you are?"
    
    elif any(word in prompt_lower for word in ['matcha', 'tea', 'green']):
        return "Matcha is amazing! It's rich in antioxidants, provides sustained energy, and has this wonderful earthy flavor. Each preparation brings out different aspects of the tea. What aspect interests you most?"
    
    else:
        responses = [
            "That's a great question about matcha! Let me share some insights...",
            "Interesting! Matcha culture has so many fascinating aspects to explore.",
            "I love talking about this! Based on your current preferences...",
            "Great point! Here's what I think about that...",
            "That's something many matcha enthusiasts wonder about!"
        ]
        return random.choice(responses)


def render_chat_scene():
    """Render the chat interface scene matching the original backup implementation"""
    render_progress_bar(4, total_steps=4)
    
    # Clean, centered header design matching mockup
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h2 style="color: #557937ff; font-size: 42px; margin-bottom: 15px;">💬 Chat with Whiski</h2>
        <p style="font-size: 18px; color: #666;">Ask me anything about matcha, cafés, or your recommendations!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the bot image like in the mockup and original backup
    # Use the same sizing as the original backup (120px width)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        try:
            st.image("bot.png", width=700, output_format="PNG")
        except:
            # Fallback if bot.png not found
            st.markdown("""
            <div style="text-align: center; padding: 40px;">
                <div style="font-size: 150px;">🤖</div>
                <p style="color: #557937ff; font-weight: bold;">Whiski</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chat input at the bottom (matching original backup style)
    if prompt := st.chat_input("Ask me about Matcha!"):
        # Display user message using Streamlit's chat components (like original)
        st.chat_message("user").write(prompt)
        
        # Get AI response
        with st.spinner("Whiski is thinking..."):
            response = get_ai_response(prompt)
        
        # Display assistant response using Streamlit's chat components (like original)  
        st.chat_message("assistant").markdown(f'<span style="color: black;">**Whiski 🧠:**</span> {response}', unsafe_allow_html=True)
    
    # Navigation buttons matching mockup style (3 buttons in a row)
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("← Back", key="back_chat", use_container_width=True):
            navigate_to_scene(SCENES['RESULTS'])
    
    with col2:
        if st.button("📍 View Cafés", key="view_cafes_chat", use_container_width=True):
            navigate_to_scene(SCENES['CAFE_DETAILS'])
    
    with col3:
        if st.button("🔄 New Search", key="new_search_chat", use_container_width=True):
            reset_chat_and_restart()

def reset_chat_and_restart():
    """Reset session including chat history and start over"""
    # Clear all session data
    for key in list(st.session_state.keys()):
        if key not in ['current_scene']:  # Keep navigation state
            del st.session_state[key]
    
    # Navigate to welcome
    navigate_to_scene(SCENES['WELCOME'])
