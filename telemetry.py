import os
from dotenv import load_dotenv
from langfuse import get_client, observe, Langfuse

load_dotenv()

public = os.getenv("LANGFUSE_PUBLIC_KEY")
secret = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")
if not (public and secret):
    print("[telemetry] Warning: Missing LANGFUSE_PUBLIC_KEY or LANGFUSE_SECRET_KEY in environment")

# Initialize Langfuse client (v3 recommended pattern)
langfuse = Langfuse(
    public_key=public,
    secret_key=secret,
    host=LANGFUSE_HOST
)



def trace_agent_call(name: str | None = None, as_type: str = "tool"):
    """
    Decorator that instruments a function using Langfuse SDK v3.

    Args:
        name: Optional explicit trace/span name. If None, uses "whiski_{func.__name__}".
        as_type: One of {"tool", "generation", "workflow"}. Defaults to "tool".
    """
    def _decorator(func):
        trace_name = name or (lambda *a, **k: f"whiski_{func.__name__}")
        observed_func = observe(name=trace_name, as_type=as_type)(func)
        return observed_func
    return _decorator

# Example usage:
# @trace_agent_call(as_type="tool")
# def fetch_cafes(location: str):
#     ...