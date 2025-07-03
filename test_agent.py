# test_agent.py
import os
from smolagents import CodeAgent, tool, LiteLLMModel


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

agent = CodeAgent(
    tools=[add],
    model=model,
    max_steps=20,
    verbosity_level=2
)

# ── Ask the agent to use our add tool ──
prompt = "Please compute add(2, 3) and return only the number."
result = agent.run(prompt)

print("Agent said:", result)