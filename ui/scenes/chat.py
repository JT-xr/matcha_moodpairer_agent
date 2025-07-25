"""
Chat Scene for Whiski App
Provides interactive chat with the AI agent using real backend integration.
"""

import streamlit as st
from styles import get_scene_header_style
from ..components.progress_bar import render_progress_bar
from ..components.navigation import render_action_buttons
from ..utils import SCENES, navigate_to_scene

# Import real backend modules
try:
    from whiski_agent import WhiskiAgent
    AGENT_AVAILABLE = True
except ImportError:
    AGENT_AVAILABLE = False
    st.warning("Whiski agent not available - using fallback mode")

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
        return get_fallback_response(prompt)
    
    try:
        agent = WhiskiAgent()
        
        # Add context to prompt if available
        if context:
            contextual_prompt = f"""
            Context: User is feeling {context.get('mood', 'unknown')} and is in {context.get('location', 'unknown location')}.
            {f"Recommended drink: {context.get('drink_recommendation', '')}" if context.get('drink_recommendation') else ""}
            {f"Weather: {context.get('weather_data', '')}" if context.get('weather_data') else ""}
            
            User message: {prompt}
            
            Respond as Whiski, the friendly matcha expert AI assistant.
            """
        else:
            contextual_prompt = f"User message: {prompt}\n\nRespond as Whiski, the friendly matcha expert AI assistant."
        
        response = agent.run(contextual_prompt)
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

def initialize_chat_history():
    """Initialize chat history with welcome message"""
    if 'chat_history' not in st.session_state:
        # Get current context
        mood = st.session_state.get('selected_mood')
        location = st.session_state.get('user_location')
        
        welcome_message = "Hi! I'm Whiski 🍵 I'm here to help you with all things matcha!"
        
        if mood and location:
            welcome_message += f" Since you selected {mood} mood in {location}, feel free to ask me about your recommendation or anything else!"
        else:
            welcome_message += " What would you like to know about matcha?"
        
        st.session_state.chat_history = [
            {
                "role": "assistant", 
                "content": welcome_message
            }
        ]

def render_chat_scene():
    """Render the chat interface scene"""
    render_progress_bar(4, total_steps=4)  # Keep at step 4 since this is an additional feature
    
    # Scene header
    st.markdown(get_scene_header_style(
        "💬 Chat with Whiski",
        "Ask me anything about matcha, cafés, or your recommendations!",
        font_size="42px"
    ), unsafe_allow_html=True)
    
    # Initialize chat history
    initialize_chat_history()
    
    # Chat interface
    st.markdown("---")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").markdown(
                f'<span style="color: black;">**Whiski 🧠:**</span> {message["content"]}', 
                unsafe_allow_html=True
            )
    
    # Chat input
    if prompt := st.chat_input("Type Here!"):
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Get context for AI
        context = {
            'mood': st.session_state.get('selected_mood'),
            'location': st.session_state.get('user_location'),
            'drink_recommendation': st.session_state.get('drink_recommendation'),
            'weather_data': st.session_state.get('weather_data')
        }
        
        # Get AI response
        with st.spinner("Whiski is thinking..."):
            response = get_ai_response(prompt, context)
        
        # Add assistant response to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.chat_message("assistant").markdown(
            f'<span style="color: black;">**Whiski 🧠:**</span> {response}', 
            unsafe_allow_html=True
        )
        st.rerun()
    
    # Navigation buttons
    st.markdown("<br><br>", unsafe_allow_html=True)
    actions = [
        {
            'label': '← Back',
            'action': lambda: navigate_to_scene(SCENES['RESULTS']),
            'key': 'back_to_results_chat'
        },
        {
            'label': '📍 View Cafés',
            'action': lambda: navigate_to_scene(SCENES['CAFE_DETAILS']),
            'key': 'view_cafes_chat'
        },
        {
            'label': '🔄 New Search',
            'action': lambda: reset_chat_and_restart(),
            'key': 'new_search_chat'
        }
    ]
    
    render_action_buttons(actions, "chat")

def reset_chat_and_restart():
    """Reset session including chat history and start over"""
    # Clear all session data
    for key in list(st.session_state.keys()):
        if key not in ['current_scene']:  # Keep navigation state
            del st.session_state[key]
    
    # Navigate to welcome
    navigate_to_scene(SCENES['WELCOME'])
