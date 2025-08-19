# 🍵 Whiski - Matcha AI Agent

An intelligent AI application that pairs your current mood with the perfect matcha drink and vibes, plus recommends local cafés. Powered by advanced LLM agentic features, it leverages context-aware reasoning and dynamic tool usage for a tailored personalized experience. The app also has a separate chat feature for users to engage with Whiski to learn about Matcha. Learn more below:


## 🌟 Features
- **Mood-Based Recommendations**: Get personalized matcha drink suggestions based on your current mood
- **Local Café Search**: Find matcha cafés near you with real-time location-based recommendations
- **AI-Powered Agent**: Uses Gemini 2.5 for intelligent, context-aware suggestions
- **LLM Chat Bot**: Chat with the LLM to learn about matcha, get personalized tips, and explore matcha culture
- **Performance Monitoring**: Integrated with Langfuse for AI observability and performance tracking

_________________________________________________________________________


## 🚀 Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/JT-xr/matcha_moodpairer_agent.git
   cd matcha_moodpairer_agent
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   Create a `.env` file with your API keys:
   ```env
   GOOGLE_GEMINI_API_KEY=your_gemini_api_key
   GOOGLE_PLACES_API_KEY=your_places_api_key
   LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
   LANGFUSE_SECRET_KEY=your_langfuse_secret_key
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

_________________________________________________________________________

## 🏗️ Project Structure

```
matcha_moodpairer_agent/
├── app.py                 # Main application entry point
├── whiski_agent.py        # AI agent implementation
├── cafe_search.py         # Café search functionality
├── mood_drink_map.py      # Mood to drink mapping logic
├── telemetry.py          # Langfuse integration for monitoring
├── weather_api.py        # Weather integration
├── styles.py             # Global CSS styling
├── requirements.txt      # Project dependencies
│
├── ui/                   # Modular UI system
│   ├── components/       # Reusable UI components
│   │   ├── buttons.py
│   │   ├── cards.py
│   │   ├── navigation.py
│   │   └── progress_bar.py
│   │
│   └── scenes/          # Individual app screens
│       ├── welcome.py
│       ├── mood_selection.py
│       ├── location_input.py
│       ├── results.py
│       └── chat.py
│
└── templates/           # AI prompt templates
    └── main_system_prompt.py
```

## 🔄 Scene Flow (User Journey)

1. **Welcome**: Introduction and app overview
2. **Mood Selection**: User selects their current mood
3. **Location Input**: User provides their location
4. **Loading**: Processing user input
5. **Results**: Shows drink recommendation and vibe
6. **Chat**: Separate AI-powered chat for more details
6. **Cafes**: Separate cafe section for LLM interaction


## 🔧 Core Components

### UI System
- **Scene-based Architecture**: Each screen is a self-contained scene with its own logic and UI
- **Component Library**: Reusable UI components for consistent design
- **Global Styling**: Centralized styling in `styles.py`

### AI Agent
- **Gemini 2.5 Integration**: Advanced language model for understanding and recommendations
- **Tool System**: Modular tools for drink recommendations and café searches
- **Prompt Templates**: Structured templates for consistent AI interactions

### Telemetry
- **Langfuse Integration**: Monitor AI performance and user interactions
- **Tracing**: Track function calls and agent decisions
- **Error Handling**: Comprehensive error tracking and reporting

## 🎨 Styling

The app uses a consistent color palette defined in `styles.py`:
- Primary Green: `#4CAF50`
- Background: `#fbf3e2ff`
- Accent Green: `#557937ff`

Custom styling is applied through:
- Global CSS in `styles.py`
- Scene-specific styles in individual scene components
- Streamlit theme configuration in `.streamlit/config.toml`


_________________________________________________________________________
## 📈 Future Enhancements
- [ ] Add user profiles and preference saving
- [ ] Integrate more café data sources
- [ ] Expand mood recognition capabilities
- [ ] Add multi-language support
- [ ] Implement café ratings and reviews


## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details