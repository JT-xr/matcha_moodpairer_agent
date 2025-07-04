# test_agent.py
import os

from pathlib import Path
from smolagents import CodeAgent, tool, LiteLLMModel, DuckDuckGoSearchTool
from mood_drink_map import get_drink_for_mood
from cafe_search import search_matcha_cafes

# Read the system prompt from the templates folder, relative to this file
BASE = Path(__file__).resolve().parent
SYSTEM_PROMPT_PATH = BASE / "templates" / "system_prompt.txt"
SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")


# ── Wire up Gemini as the LLM backend ──
model = LiteLLMModel(
    system_prompt= SYSTEM_PROMPT,
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

duck_tool = DuckDuckGoSearchTool ()


agent = CodeAgent(
    tools=[get_drink_for_mood_tool,search_matcha_cafes_tool, duck_tool],
    model=model,
    max_steps=3,
    verbosity_level=0, #controls how much "thinking" info the agent logs 0-3, 3 is most verbose
)


# smoke-test below
if __name__ == "__main__":
    resp = agent.run("What is your name?")
    print("Agent response:", resp)