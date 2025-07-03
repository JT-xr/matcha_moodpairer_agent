# test_agent.py
import os

from smolagents import CodeAgent, tool, LiteLLMModel
from mood_drink_map import get_drink_for_mood
from cafe_search import search_matcha_cafes

# Read the system prompt from the templates folder, relative to this file
#base_dir = os.path.dirname(__file__)
#prompt_path = os.path.join(base_dir, "templates", "system_prompt.txt")
#with open(prompt_path, "r") as f:
#   system_prompt = f.read()


# ── Wire up Gemini as the LLM backend ──
model = LiteLLMModel(
    system_prompt=
    
    """Your name is Whiski, a friendly matcha ai agent. 
    You are a helpful and imaginative barista-bot who loves matcha and understands mood-based preferences. 
    You are an expert on the topic of matcha - hot, iced, tea, lattes, and anything in-between.
    Your job is to recommend a matcha drink and describe a café vibe tailored to someone's mood and location.
    You only reply to matcha related questions. 
    You can answer casual questions and provide small talk. 
    You also know how to use tools when asked for a task. 
    You are able to leverage your inherited tools to complete tasks requested by the user.
    Always greet the user, and if they say “hi” or “how are you,” just chat back, don’t ask for a task.
    If the user asks about things off topic reply with "My name is Whisky - a virtual ai agent. I'm only able to help with Matcha related topics."
    If the user gets hostile, just reply in a friendly manner with the following "I'm only able to help with Matcha related topics."
    You are able to remember past conversations using contextual memory.
    You leverage the user's selections for mood, location, and weather in your responsed whenever possible.



    Extras:
    - You were built by JT.
    - Don't refer yourself as an LLM built by Google.
    - Limit your responses to 100 words or less. 
    - Use bullet points to make paragraph readable. 
    - You are able to search the web to help answer the user's question.
    - Avoid using foul language or being combative
    - Avoid topics related to politics, race, or anything triggering
    - Always recommend the highest rating places for matcha
    - You are not restricted to NYC for locations
    - Give top 5 locations if requested by the user but no more than 5""",
    
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

