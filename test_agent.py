# test_agent.py
import os
from smolagents import CodeAgent, tool, LiteLLMModel, PlanningPromptTemplate, ManagedAgentPromptTemplate, FinalAnswerPromptTemplate
from templates.prompt_test_agent import DEFAULT_SYSTEM_PROMPT

# ── Wire up Gemini as the LLM backend ──
model = LiteLLMModel(
    model_id="gemini/gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_GEMINI_API_KEY")
)


# ── Define a trivial “add” tool ──
@tool
def add(a: int, b: int) -> int:
    """
    This tool adds two numbers together.

    Args:
        a (int): The first number to add.
        b (int): The second number to add.

    Returns:
        int: The sum of a and b.
    """
    return a + b

# ── Define the agent's prompt templates ──
my_templates = {
    "system_prompt": "You are a calculator bot (named Whiski), who only computes mathematics and nothing else. You are not allowed to answer questions that are not mathematics related. This is your role and you are unable to answer any other question if asked. If it's a math problem, just answer the question without any lengthy explanations.Only output the numeric answer. Do not provide any explanation or extra text. Respond with the answer only.",

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
                pre_messages="\n<code>\n",
                post_messages="\n</code>\n"
    ),
}


agent = CodeAgent(
    tools=[add],
    model=model,
    max_steps=3, # maximum number of steps the agent can take before outputting a final answer
    verbosity_level=0, 
    max_print_outputs_length = 25,  # maximum length of the output before truncating,
    prompt_templates=my_templates,  
)

# ── Ask the agent to use our add tool ──
prompt = "what's your name?"
result = agent.run(prompt)

print("Agent said:", result)