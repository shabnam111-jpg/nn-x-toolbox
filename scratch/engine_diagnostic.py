import os
import sys
from dotenv import load_dotenv

def diagnostic():
    print("--- Aura AI Engine Diagnostic ---")
    print(f"Python Executable: {sys.executable}")
    
    # Check .env loading
    loaded = load_dotenv(override=True)
    print(f".env loaded: {loaded}")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    nvidia_key = os.getenv("NVIDIA_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    print(f"OpenAI Key Found: {bool(openai_key)}")
    print(f"NVIDIA Key Found: {bool(nvidia_key)}")
    print(f"Gemini Key Found: {bool(gemini_key)}")
    
    # Check Imports
    try:
        from openai import OpenAI
        print("OpenAI Library: OK")
    except Exception as e:
        print(f"OpenAI Library Error: {e}")
        
    try:
        import google.generativeai as genai
        print("Gemini Library: OK")
    except Exception as e:
        print(f"Gemini Library Error: {e}")
        
    # Test Initialization Logic
    if nvidia_key:
        try:
            from openai import OpenAI
            client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=nvidia_key)
            print("NVIDIA Init check: OK")
        except Exception as e:
            print(f"NVIDIA Init check ERROR: {e}")

    if openai_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            print("OpenAI Init check: OK")
        except Exception as e:
            print(f"OpenAI Init check ERROR: {e}")

if __name__ == "__main__":
    diagnostic()
