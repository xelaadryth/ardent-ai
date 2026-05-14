from config import MODELS
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable
from google import genai
import os
import time

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

RETRYABLE_ERRORS = (
    ServiceUnavailable,   # 503
    ResourceExhausted,    # rate limits (often 429)
)

def generate_content(prompt: str, models=None, max_retries=2) -> str:
    models = models or MODELS

    last_error = None

    for model in models:
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                print(f"[MODEL SUCCESS] {model} (attempt {attempt + 1})")
                return response.text

            except RETRYABLE_ERRORS as e:
                last_error = e
                wait = 2 ** attempt  # exponential backoff
                time.sleep(wait)

            except Exception as e:
                # non-retryable → try next model immediately
                last_error = e
                break

    raise RuntimeError(f"All models failed. Last error: {last_error}")