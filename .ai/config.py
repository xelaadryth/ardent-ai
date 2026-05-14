import os

MODEL = "gemini-3.1-flash-lite"
MODELS = [
    "gemini-3.1-flash",
    "gemini-2.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash-lite",
]
VAULT_ROOT = "."
PROMPT = os.environ.get("PROMPT", "")
