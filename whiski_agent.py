# whiski_agent.py
import os

from smolagents import CodeAgent, tool, LiteLLMModel, DuckDuckGoSearchTool, PlanningPromptTemplate, ManagedAgentPromptTemplate, FinalAnswerPromptTemplate
from mood_drink_map import get_drink_for_mood
from cafe_search import search_matcha_cafes
from templates.main_system_prompt import WHISKI_SYSTEM_PROMPT


# ── Wire up Gemini 2.5 as the LLM backend (better instruction following than 1.5) ──
model = LiteLLMModel(
    system_prompt=WHISKI_SYSTEM_PROMPT,
    model_id="gemini/gemini-2.5-flash",  # Upgraded for better prompt adherence
    api_key=os.getenv("GOOGLE_GEMINI_API_KEY"),
    timeout=30,  # 30 second timeout
    max_retries=3,  # Retry up to 3 times on failure
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

@tool
def web_search_tool(query: str) -> str:
    """
    Search the web for information using DuckDuckGo.
    
    Args:
        query: The search query string
        
    Returns:
        str: Search results as a formatted string
    """
    try:
        duck_tool = DuckDuckGoSearchTool()
        results = duck_tool.forward(query)
        return str(results)
    except Exception as e:
        return f"Search failed: {str(e)}"



my_templates = {
    "system_prompt": WHISKI_SYSTEM_PROMPT,

    # planning template: controls how the agent initially thinks
    "planning": PlanningPromptTemplate(
        initial_plan="🍵 Let me think about your matcha needs...",
        update_plan_pre_messages="📝 Updating my approach: ",
        update_plan_post_messages="✅ Plan updated!",
    ),

    # managed_agent: how it wraps up each step if using a managed agent
    "managed_agent": ManagedAgentPromptTemplate(
        task="🎯 Task: {task}",
        report="📊 Results: {report}",
    ),
    
    # final_answer: how the final response is formatted
    "final_answer": FinalAnswerPromptTemplate(
        pre_messages="",
        post_messages=""
    ),
}




agent = CodeAgent(
    tools=[get_drink_for_mood_tool, search_matcha_cafes_tool, web_search_tool],
    model=model,
    max_steps=2,
    verbosity_level=1, #controls how much "thinking" info the agent logs 0-3, 3 is most verbose
    max_print_outputs_length = 300,  # maximum length of the output before truncating,
    prompt_templates=my_templates,  
)


# Enhanced test to see formatting in action
if __name__ == "__main__":
    print("=== Testing Whiski Agent Formatting ===\n")
    
    # Test 1: Simple greeting
    print("Test 1: Simple greeting")
    resp1 = agent.run("code?")
    print(f"Response: {resp1}\n")
