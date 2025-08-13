from langfuse import Langfuse
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY")
)

def trace_agent_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        trace = langfuse.trace(
            name="whiski_recommendation",
            metadata={
                "function": func.__name__,
                "args": str(args),
                "kwargs": str(kwargs)
            }
        )
        
        try:
            with trace.span(name=f"agent_{func.__name__}") as span:
                result = func(*args, **kwargs)
                span.set_attribute("success", True)
                return result
        except Exception as e:
            trace.error(
                message=str(e),
                level="error",
                stack_trace=str(e)
            )
            raise
        finally:
            trace.end()
    
    return wrapper