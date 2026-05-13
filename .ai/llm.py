from google import genai
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_content(model: str, prompt: str) -> str:
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    return response.text
