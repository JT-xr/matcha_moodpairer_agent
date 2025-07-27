"""
UI Module Structure for Whiski Matcha Mood Pairer
==================================================

This file documents the modular UI structure for organizing the Streamlit app components.

DIRECTORY STRUCTURE:
```
ui/
├── __init__.py              # UI module initialization
├── scenes/                  # Scene/page modules
│   ├── __init__.py         
│   ├── welcome.py          # Welcome/splash page
│   ├── mood_selection.py   # Mood selection scene
│   ├── location_input.py   # Location input scene
│   ├── results.py          # Results display scene
│   ├── cafe_details.py     # Individual café details
│   └── chat.py             # Chat interface scene
├── components/             # Reusable UI components
│   ├── __init__.py
│   ├── progress_bar.py     # Progress indicator
│   ├── navigation.py       # Navigation utilities
│   ├── cards.py           # Various card components
│   └── buttons.py         # Button components
└── utils.py               # UI utility functions
```

ROOT LEVEL:
- styles.py                 # All CSS styling (already created)
- app.py                   # Main application entry point

DESIGN PRINCIPLES:
1. Each scene is self-contained with its own render function
2. Components are reusable across scenes
3. All styling is centralized in styles.py
4. Real backend integration (no mock data)
5. Clean separation of concerns
6. Session state management centralized in app.py

INTEGRATION PATTERN:
- app.py imports scenes and orchestrates navigation
- Each scene imports needed backend modules (whiski_agent, cafe_search, etc.)
- Components are imported by scenes as needed
- Styles are applied globally and per-scene as needed

BACKEND INTEGRATIONS:
- whiski_agent.py: AI recommendations and chat
- cafe_search.py: Café discovery and details
- weather_api.py: Weather-based recommendations
"""
