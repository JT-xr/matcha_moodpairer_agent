# test_langfuse.py — Option B: use shared telemetry client
from dotenv import load_dotenv
from telemetry import langfuse          # centralized Langfuse client (uses LANGFUSE_HOST, keys from env)
from langfuse import observe, get_client             # decorator for quick spans

# Load env vars from .env so keys/host are available when running locally
load_dotenv()


@observe(name="cli_test_decorator", as_type="workflow")
def run_test():
    """Very small decorator-based test; should create a trace in Langfuse."""
    return "ok"

langfuse = get_client()
langfuse.flush()

if __name__ == "__main__":
    # 1) Decorator-based smoke test
    print("Decorator test result:", run_test())

