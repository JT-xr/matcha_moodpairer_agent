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
from telemetry import langfuse
from langfuse import observe, get_client

# Import real backend modules
try:
    from whiski_agent import agent  # Import the agent instance directly like in original
    AGENT_AVAILABLE = True
except ImportError:
    AGENT_AVAILABLE = False
    st.warning("Whiski agent not available - using fallback mode")

@observe(name="chat.get_ai_response", as_type="generation")
def get_ai_response(prompt, context=None):
    """
    Get AI response using real Whiski agent
    
    Args:
        prompt (str): User's message
        context (dict): Current session context
    
    Returns:
        str: AI response
    """
    if not AGENT_AVAILABLE:
        st.error("Whiski agent is not available. Please check your configuration.")
        return "Sorry, I'm not available right now. Please try again later."
    
    try:
        # Use agent directly
        response = agent.run(prompt)
        return response
        
    except Exception as e:
        st.error(f"Error getting AI response: {e}")
        return "I'm having trouble responding right now. Please try again."
langfuse = get_client()
langfuse.flush()



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
            st.error("Bot image (bot.png) not found. Please check your assets.")
    
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
