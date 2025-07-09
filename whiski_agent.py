# whiski_agent.py
import os

from smolagents import CodeAgent, tool, LiteLLMModel, DuckDuckGoSearchTool, PlanningPromptTemplate, ManagedAgentPromptTemplate, FinalAnswerPromptTemplate
from mood_drink_map import get_drink_for_mood
from cafe_search import search_matcha_cafes
from templates.main_system_prompt import WHISKI_SYSTEM_PROMPT


# ── Wire up Gemini as the LLM backend ──
model = LiteLLMModel(
    system_prompt= WHISKI_SYSTEM_PROMPT,
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



my_templates = {
    "system_prompt": WHISKI_SYSTEM_PROMPT,

    # planning template: controls how the agent initially thinks
    "planning": PlanningPromptTemplate(
        initial_plan="",
        update_plan_pre_messages="",
        update_plan_post_messages="",
    ),


# managed_agent: how it wraps up each step if using a managed agent
    "managed_agent": ManagedAgentPromptTemplate(
        task="{task}",  # insert your task string here
        report="{report}",  # how to show tool results
    ),
    # final_answer: how the final response is formatted
    "final_answer": FinalAnswerPromptTemplate(
                pre_messages="",
                post_messages=""
    ),
}




agent = CodeAgent(
    tools=[get_drink_for_mood_tool,search_matcha_cafes_tool, duck_tool],
    model=model,
    max_steps=1,
    verbosity_level=1, #controls how much "thinking" info the agent logs 0-3, 3 is most verbose
    max_print_outputs_length = 10,  # maximum length of the output before truncating,
    prompt_templates=my_templates,  
)


# smoke-test below
if __name__ == "__main__":
    resp = agent.run("What is your name?")
    print("Agent response:", resp)