"""
Scenes Module Initialization
Imports all scene modules for the Whiski app.
"""

# Import scene render functions
from .welcome import render_welcome_scene
from .mood_selection import render_mood_selection_scene
from .location_input import render_location_input_scene, render_custom_location_scene
from .results import render_results_scene
from .cafe_details import render_cafe_details_scene
from .chat import render_chat_scene

__all__ = [
    'render_welcome_scene',
    'render_mood_selection_scene',
    'render_location_input_scene',
    'render_custom_location_scene',
    'render_results_scene',
    'render_cafe_details_scene',
    'render_chat_scene'
]
