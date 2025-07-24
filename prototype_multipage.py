import streamlit as st
import time
import os

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'selected_mood' not in st.session_state:
    st.session_state.selected_mood = None
if 'selected_location' not in st.session_state:
    st.session_state.selected_location = None
if 'show_cafes' not in st.session_state:
    st.session_state.show_cafes = False

# Custom CSS for better styling
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

def show_progress_bar(step, total_steps=4):
    """Show progress bar at top of each scene"""
    progress = (step / total_steps) * 100
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress}%;"></div>
    </div>
    <p style="text-align: center; color: #666; font-size: 14px;">Step {step} of {total_steps}</p>
    """, unsafe_allow_html=True)

def show_welcome_scene():
    """Scene 1: Welcome/Landing"""
    st.markdown("""
    <div class="scene-container">
        <h1 style="font-size: 80px; margin-bottom: 20px;">🍵</h1>
        <h1 style="color: #4CAF50; font-size: 60px; margin-bottom: 20px;">Whiski</h1>
        <p style="font-size: 24px; color: #666; margin-bottom: 40px;">
            Your AI matcha mood pairer
        </p>
        <p style="font-size: 18px; color: #888; margin-bottom: 40px;">
            Discover the perfect matcha drink and café vibe<br>
            tailored to your mood and location
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 START YOUR JOURNEY", key="start_btn", type="primary", use_container_width=True):
            st.session_state.page = 'mood'
            st.rerun()

def show_mood_scene():
    """Scene 2: Mood Selection"""
    show_progress_bar(1)
    
    st.markdown("""
    <div style="text-align: center; padding: 20px 20px 30px 20px;">
        <h2 style="font-size: 48px; margin-bottom: 15px;">✨ What's your vibe?</h2>
        <p style="font-size: 20px; color: #666; margin-bottom: 30px;">
            Choose the mood that best describes how you're feeling right now
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    vibes = {
        "😌": "chill",
        "😰": "anxious", 
        "🎨": "creative",
        "🧘": "reflective",
        "⚡": "energized",
        "☕": "cozy"
    }
    
    # Create 2x3 grid with same styling as location buttons
    for row in range(2):
        cols = st.columns(3, gap="small")
        for col in range(3):
            index = row * 3 + col
            if index < len(list(vibes.items())):
                emoji, mood = list(vibes.items())[index]
                with cols[col]:
                    if st.button(f"{emoji} {mood.title()}", key=f"mood_{mood}", use_container_width=True):
                        st.session_state.selected_mood = mood
                        st.session_state.page = 'location'
                        st.rerun()

def show_location_scene():
    """Scene 3: Location Selection"""
    show_progress_bar(2)
    
    st.markdown(f"""
    <div class="scene-container">
        <h2 style="font-size: 48px; margin-bottom: 20px;">📍 Where are you?</h2>
        <p style="font-size: 20px; color: #666; margin-bottom: 20px;">
            You're feeling <strong>{st.session_state.selected_mood}</strong>
        </p>
        <p style="font-size: 18px; color: #888; margin-bottom: 40px;">
            Select your location to find nearby matcha cafés
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    locations = ["Brooklyn, NY", "Manhattan, NY", "Queens, NY", "Other Location"]
    
    for i, location in enumerate(locations):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"📍 {location}", key=f"loc_{i}", use_container_width=True):
                if location == "Other Location":
                    st.session_state.page = 'custom_location'
                else:
                    st.session_state.selected_location = location
                    st.session_state.page = 'loading'
                st.rerun()
    
    # Back button
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("← Back to Mood", key="back_location"):
            st.session_state.page = 'mood'
            st.rerun()

def show_custom_location_scene():
    """Scene 3b: Custom Location Input"""
    show_progress_bar(2)
    
    st.markdown(f"""
    <div class="scene-container">
        <h2 style="font-size: 48px; margin-bottom: 20px;">📍 Enter your location</h2>
        <p style="font-size: 20px; color: #666; margin-bottom: 40px;">
            You're feeling <strong>{st.session_state.selected_mood}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    custom_loc = st.text_input(
        "Type your location:", 
        placeholder="e.g., San Francisco, CA",
        key="custom_location_input"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="back_custom", use_container_width=True):
            st.session_state.page = 'location'
            st.rerun()
    with col2:
        if st.button("Continue →", key="continue_custom", use_container_width=True, type="primary"):
            if custom_loc.strip():
                st.session_state.selected_location = custom_loc
                st.session_state.page = 'loading'
                st.rerun()
            else:
                st.error("Please enter a location")

def show_loading_scene():
    """Scene 4: Loading/Processing"""
    show_progress_bar(3)
    
    st.markdown("""
    <div class="scene-container">
        <h2 style="font-size: 48px; margin-bottom: 30px;">🧠 Whiski is thinking...</h2>
        <p style="font-size: 20px; color: #666; margin-bottom: 40px;">
            Brewing the perfect matcha recommendation for you
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Loading animation
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    messages = [
        "Analyzing your mood...",
        "Checking local weather...",
        "Finding nearby cafés...",
        "Crafting your perfect recommendation..."
    ]
    
    for i, message in enumerate(messages):
        status_text.text(message)
        progress_bar.progress((i + 1) * 25)
        time.sleep(0.8)
    
    st.session_state.page = 'results'
    st.rerun()

def show_results_scene():
    """Scene 5: Results/Recommendation"""
    show_progress_bar(4)
    
    st.markdown("""
    <div style="text-align: center; padding: 30px;">
        <h1 style="color: #4CAF50; font-size: 60px; margin-bottom: 20px;">🎉 Perfect Match!</h1>
        <p style="font-size: 20px; color: #666;">Here's your personalized matcha experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mock recommendation (replace with actual agent call)
    mood = st.session_state.selected_mood
    location = st.session_state.selected_location
    
    # Simulated recommendations based on mood
    mock_recommendations = {
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
    
    recommendation = mock_recommendations.get(mood, mock_recommendations["chill"])
    
    # Add separator line (matching main app)
    st.markdown("---")
    
    # Display results using same layout as main app
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(f"""
        <div style="
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #4CAF50;
            height: 100%;
        ">
            <h3 style="color: #2c3e50; margin-top: 0;">🧠 Whiski's Recommendation</h3>
            <div style="background: #e8f5e8; padding: 10px; border-radius: 8px; margin: 10px 0;">
                <strong>🍵 Drink:</strong> {recommendation['drink']}
            </div>
            <div style="background: #fff; padding: 15px; border-radius: 8px; margin: 10px 0;">
                <strong>✨ Vibe:</strong><br>
                {recommendation['vibe']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Use a placeholder image or your actual matcha_cafe.png
        try:
            st.image("matcha_cafe.png", caption="Matcha Vibe", width=400)
        except:
            # Fallback to online image if local file doesn't exist
            st.image("https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400", 
                    caption="Matcha Vibe", width=400)
    
    # Action buttons (updated to navigate to chat page)
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔄 Try Again", key="try_again", use_container_width=True):
            # Reset session state
            st.session_state.page = 'welcome'
            st.session_state.selected_mood = None
            st.session_state.selected_location = None
            st.rerun()
    
    with col2:
        if st.button("📍 Find Cafés", key="find_cafes", use_container_width=True, type="primary"):
            st.session_state.page = 'cafe_results'  # Navigate to new scene
            st.rerun()
    
    with col3:
        if st.button("💬 Chat with Whiski", key="chat", use_container_width=True):
            st.session_state.page = 'chat'  # Navigate to chat page
            st.rerun()
    
    # Remove the inline chat interface section since we now have a dedicated page

# Add a new function for the chat scene
def show_chat_scene():
    """Scene 7: Chat with Whiski"""
    show_progress_bar(4, total_steps=4)  # Keep at step 4 since this is an additional feature
    
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h2 style="color: #4CAF50; font-size: 42px; margin-bottom: 15px;">💬 Chat with Whiski</h2>
        <p style="font-size: 18px; color: #666;">Ask me anything about matcha, cafés, or your recommendations!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat interface (removed the current session context box)
    st.markdown("---")
    
    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant", 
                "content": f"Hi! I'm Whiski 🍵 I'm here to help you with all things matcha! {'Since you selected ' + st.session_state.selected_mood + ' mood in ' + st.session_state.selected_location + ', feel free to ask me about your recommendation or anything else!' if st.session_state.selected_mood else 'What would you like to know about matcha?'}"
            }
        ]
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").markdown(f'<span style="color: black;">**Whiski 🧠:**</span> {message["content"]}', unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask me about matcha, cafés, or your recommendations!"):
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Mock AI response (replace with actual agent.run(prompt) in real app)
        mock_responses = [
            "That's a great question about matcha! Based on your preferences, I'd recommend...",
            "I love talking about matcha! Here's what I think about that...",
            "Interesting! Let me share some insights about that...",
            "Based on your current mood and location, here's my take...",
            "Great question! Matcha is such a fascinating topic..."
        ]
        
        import random
        response = random.choice(mock_responses) + f" (This is a mock response - in the real app, this would use agent.run('{prompt}'))"
        
        # Add assistant response to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.chat_message("assistant").markdown(f'<span style="color: black;">**Whiski 🧠:**</span> {response}', unsafe_allow_html=True)
        st.rerun()
    
    # Navigation buttons only
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Back to Results", key="back_to_results_chat", use_container_width=True):
            st.session_state.page = 'results'
            st.rerun()
    
    with col2:
        if st.button("📍 View Cafés", key="view_cafes_chat", use_container_width=True):
            st.session_state.page = 'cafe_results'
            st.rerun()
    
    with col3:
        if st.button("🔄 New Search", key="new_search_chat", use_container_width=True):
            st.session_state.page = 'welcome'
            st.session_state.selected_mood = None
            st.session_state.selected_location = None
            st.session_state.chat_history = []
            st.rerun()

# Add this new function for the café results scene
def show_cafe_results_scene():
    """Scene 6: Café Search Results"""
    show_progress_bar(4)  # Or make it step 5 if you prefer
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <h2 style="color: #4CAF50; font-size: 42px; margin-bottom: 15px;">📍 Nearby Cafés</h2>
        <p style="font-size: 18px; color: #666;">Perfect spots for your <strong>{st.session_state.selected_mood}</strong> vibe in <strong>{st.session_state.selected_location}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mock café data (would come from your cafe_search.py)
    mock_cafes = [
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
            "name": "Whiski's Favorite",
            "address": "89 Smith St, Brooklyn, NY",
            "rating": 4.9,
            "distance": "1.2 miles", 
            "speciality": "Creative matcha cocktails",
            "atmosphere": "Vibrant, artistic, Instagram-worthy",
            "price_range": "$$",
            "phone": "(718) 555-0789"
        }
    ]
    
    # Display café cards (removed images)
    for i, cafe in enumerate(mock_cafes):
        with st.container():
            st.markdown(f"""
            <div style="
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #4CAF50;
                margin: 10px 0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            ">
                <h4 style="color: #2c3e50; margin: 0 0 10px 0; font-size: 20px;">
                    {cafe['name']} 
                    <span style="color: #ff9800;">⭐ {cafe['rating']}</span>
                </h4>
                <p style="color: #666; margin: 5px 0; font-size: 14px;">
                    📍 {cafe['address']} • <strong>{cafe['distance']}</strong>
                </p>
                <p style="color: #4CAF50; margin: 5px 0; font-weight: bold; font-size: 15px;">
                    🍵 {cafe['speciality']}
                </p>
                <p style="color: #888; margin: 5px 0; font-style: italic; font-size: 14px;">
                    "{cafe['atmosphere']}"
                </p>
                <p style="color: #333; margin: 5px 0; font-size: 14px;">
                    💰 {cafe['price_range']} • 📞 {cafe['phone']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons for each café
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("🗺️ Directions", key=f"directions_{i}", use_container_width=True):
                    st.success(f"Opening directions to {cafe['name']}...")
            with col_b:
                if st.button("📞 Call", key=f"call_{i}", use_container_width=True):
                    st.info(f"Calling {cafe['phone']}...")
            with col_c:
                if st.button("💾 Save", key=f"save_{i}", use_container_width=True):
                    st.success(f"Saved {cafe['name']} to favorites!")
        
        # Add spacing between café cards
        if i < len(mock_cafes) - 1:
            st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation buttons (removed the additional search options)
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Back to Results", key="back_to_results", use_container_width=True):
            st.session_state.page = 'results'
            st.rerun()
    
    with col2:
        if st.button("🔄 New Search", key="new_search", use_container_width=True):
            st.session_state.page = 'welcome'
            st.session_state.selected_mood = None
            st.session_state.selected_location = None
            st.rerun()
    
    with col3:
        if st.button("💬 Chat with Whiski", key="chat_from_cafes", use_container_width=True):
            st.session_state.page = 'chat'  # Navigate to chat page
            st.rerun()

def main():
    """Main app routing"""
    st.set_page_config(
        page_title="Whiski - Prototype", 
        page_icon="🍵",
        layout="centered"
    )
    
    # Hide streamlit style
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Route to appropriate scene
    if st.session_state.page == 'welcome':
        show_welcome_scene()
    elif st.session_state.page == 'mood':
        show_mood_scene()
    elif st.session_state.page == 'location':
        show_location_scene()
    elif st.session_state.page == 'custom_location':
        show_custom_location_scene()
    elif st.session_state.page == 'loading':
        show_loading_scene()
    elif st.session_state.page == 'results':
        show_results_scene()
    elif st.session_state.page == 'cafe_results':
        show_cafe_results_scene()
    elif st.session_state.page == 'chat':  # Add new chat route
        show_chat_scene()
    
    # Debug info (remove in production)
    with st.sidebar:
        st.write("**Debug Info:**")
        st.write(f"Current page: {st.session_state.page}")
        st.write(f"Selected mood: {st.session_state.selected_mood}")
        st.write(f"Selected location: {st.session_state.selected_location}")
        
        if st.button("Reset App"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()