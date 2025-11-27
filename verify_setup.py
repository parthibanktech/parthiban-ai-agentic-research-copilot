import sys
import os
from dotenv import load_dotenv

def verify_setup():
    print("Verifying setup...")
    
    # Check imports
    try:
        import chainlit
        import langchain
        import langchain_openai
        import langchain_community
        import wikipedia
        import tavily
        import alpha_vantage
        print("✅ All libraries installed successfully.")
        print(f"LangChain version: {langchain.__version__}")
    except ImportError as e:
        print(f"❌ Missing library: {e}")
        sys.exit(1)

    # Check API Keys
    load_dotenv()
    missing_keys = []
    if not os.getenv("OPENAI_API_KEY"):
        missing_keys.append("OPENAI_API_KEY")
    if not os.getenv("TAVILY_API_KEY"):
        missing_keys.append("TAVILY_API_KEY")
    if not os.getenv("ALPHAVANTAGE_API_KEY"):
        missing_keys.append("ALPHAVANTAGE_API_KEY")

    if missing_keys:
        print(f"⚠️  Missing API Keys: {', '.join(missing_keys)}")
        print("Please create a .env file with these keys.")
    else:
        print("✅ All API keys found.")

if __name__ == "__main__":
    verify_setup()
