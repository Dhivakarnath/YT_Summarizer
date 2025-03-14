# Used to check the models in the API and Expiry of the API

# import requests
# import os

# GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Load API key from environment variables

# headers = {
#     "Authorization": f"Bearer {GROQ_API_KEY}",
#     "Content-Type": "application/json"
# }

# data = {
#     "model": "llama3-70b-8192",  # Choose model (or use mixtral-8x7b-32768)
#     "messages": [
#         {"role": "system", "content": "You are an expert summarizer."},
#         {"role": "user", "content": "Summarize this transcript: <your_text_here>"}
#     ],
#     "temperature": 0.7
# }

# response = requests.post(GROQ_API_URL, headers=headers, json=data)

# if response.status_code == 200:
#     print(response.json())  # Output AI-generated summary
# else:
#     print(f"❌ Error: {response.json()}")


import os
import google.generativeai as genai

# Set API Key
api_key = os.getenv("GOOGLE_API_KEY")  # Load from .env (if set)
if not api_key:
    api_key = input("Enter your Google Gemini API Key: ").strip()

# Configure API
genai.configure(api_key=api_key)

try:
    # Fetch available models
    available_models = genai.list_models()
    
    # Print model names
    model_names = [model.name for model in available_models]
    print("\n✅ Available Models:", model_names)

except Exception as e:
    print(f"\n❌ Error fetching models: {str(e)}")
