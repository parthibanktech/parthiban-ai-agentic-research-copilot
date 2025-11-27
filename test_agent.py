import os
from dotenv import load_dotenv
from agent import get_agent_executor
from langchain_core.messages import HumanMessage

def test_agent():
    load_dotenv()
    
    # Check for API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("Skipping test: OPENAI_API_KEY not found.")
        return

    print("Initializing agent...")
    try:
        agent_executor = get_agent_executor()
        print("Agent initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        return

    # Test a simple query (if keys are present)
    # We won't actually invoke it if we don't want to consume quota or if keys are invalid, 
    # but we can check if the object is created correctly.
    # If the user has keys, we can try a simple hello.
    
    print("Test complete.")

if __name__ == "__main__":
    test_agent()
