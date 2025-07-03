# test_agent.py
import os

from smolagents import CodeAgent, tool, LiteLLMModel
from mood_drink_map import get_drink_for_mood
from cafe_search import search_matcha_cafes


# ── Wire up Gemini as the LLM backend ──
model = LiteLLMModel(
    system_prompt="""
    You are Whiski, a friendly matcha assistant. 
    You can answer casual questions and small talk,
    and you also know how to use tools when asked for a task.
    Always greet the user, and if they say “hi” or “how are you,”
    just chat back, don’t ask for a task.""",
    model_id="gemini/gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_GEMINI_API_KEY")
)


@tool
def get_drink_for_mood_tool(mood: str) -> str:
    """
    Returns a recommended a unique matcha drink for a given mood the user inputs.

    Args:
        mood: The mood that user selects from the list.
    
    """
    return get_drink_for_mood(mood)

@tool
def search_matcha_cafes_tool(location: str) -> list[dict]:
    """
    Returns a list of matcha cafés in a given location.

    Args:
        location: The location where the user wants to search for matcha cafés.
    
    """
    return search_matcha_cafes(location)


agent = CodeAgent(
    tools=[get_drink_for_mood_tool,search_matcha_cafes_tool],
    model=model,
    max_steps=20,
    verbosity_level=2
)

