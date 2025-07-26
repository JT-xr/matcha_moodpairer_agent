# Whiski - Matcha Mood Pairer Agent

A Streamlit-based application that pairs your mood with the perfect matcha drink and recommends local cafés.

## Features

- **Mood-based Recommendations**: Select your mood and get personalized matcha drink suggestions
- **Location-aware Café Search**: Find cafés near you with real-time recommendations
- **Weather Integration**: Weather-aware suggestions for the perfect drink
- **Interactive Chat**: Engage with the Whiski AI agent for personalized advice
- **Beautiful UI**: Modern, polished interface with smooth navigation

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment Variables**:
   Create a `.env` file with your API keys:
   ```
   GOOGLE_API_KEY=your_gemini_api_key
   OPENWEATHER_API_KEY=your_weather_api_key
   ```

3. **Run the App**:
   ```bash
   streamlit run app.py
   ```

## Project Structure

- `app.py` - Main application entry point
- `ui/` - Modular UI system
  - `scenes/` - Individual app screens
  - `components/` - Reusable UI components
  - `utils.py` - UI utilities
- `styles.py` - Global CSS styling
- `whiski_agent.py` - AI agent logic
- `cafe_search.py` - Café search functionality
- `weather_api.py` - Weather integration
- `templates/` - AI prompt templates
- `backup_files/` - Previous versions and test files

## Development

The app uses a modular architecture with clean separation between UI components and backend logic. All styling is centralized in `styles.py`, and the UI is built using reusable components from the `ui/` directory.

## Migration Notes

This app has been fully migrated from a prototype to a production-ready application with:
- Modular UI architecture
- Real backend integration
- Clean, polished UX
- Production-ready code structure