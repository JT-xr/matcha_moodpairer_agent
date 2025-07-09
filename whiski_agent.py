# whiski_agent.py
import os

from smolagents import CodeAgent, tool, LiteLLMModel, DuckDuckGoSearchTool, PlanningPromptTemplate, ManagedAgentPromptTemplate, FinalAnswerPromptTemplate
from mood_drink_map import get_drink_for_mood
from cafe_search import search_matcha_cafes
from templates.main_system_prompt import WHISKI_SYSTEM_PROMPT


# ── Wire up Gemini as the LLM backend ──
model = LiteLLMModel(
    system_prompt= WHISKI_SYSTEM_PROMPT,
    model_id="gemini/gemini-2.5-flash",
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

duck_tool = DuckDuckGoSearchTool()



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
        pre_messages="🧠 **Hi, I'm happy to help!**\n",
        post_messages="\n\n🍵 *Enjoy your matcha journey!*"
    ),
}




agent = CodeAgent(
    tools=[get_drink_for_mood_tool,search_matcha_cafes_tool, duck_tool],
    model=model,
    max_steps=3,
    verbosity_level=3, #controls how much "thinking" info the agent logs 0-3, 3 is most verbose
    max_print_outputs_length = 10,  # maximum length of the output before truncating,
    prompt_templates=my_templates,  
)


# Enhanced test to see formatting in action
if __name__ == "__main__":
    print("=== Testing Whiski Agent Formatting ===\n")
    
    # Test 1: Simple greeting
    print("Test 1: Simple greeting")
    resp1 = agent.run("What is your name?")
    print(f"Response: {resp1}\n")
    
    # Test 2: Mood-based recommendation (uses tools)
    print("Test 2: Mood-based recommendation")
    resp2 = agent.run("I'm feeling anxious, can you recommend a matcha drink?")
    print(f"Response: {resp2}\n")
    
    # Test 3: Location-based search (uses tools)
    print("Test 3: Location-based search")
    resp3 = agent.run("Find me matcha cafes in Brooklyn")
    print(f"Response: {resp3}\n")