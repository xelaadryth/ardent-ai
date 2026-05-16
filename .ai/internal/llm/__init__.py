from pkg.config import MODELS
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import os
import time

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

RETRYABLE_ERRORS = (
    ServiceUnavailable,   # 503
    ResourceExhausted,    # rate limits (often 429)
)

# =====================================================================
# DEFINING THE ENFORCED JSON SCHEMA
# =====================================================================
class FileOperation(BaseModel):
    action: Literal["create", "update", "delete"] = Field(
        description="The type of file operation to perform."
    )
    name: str = Field(
        description="The exact page title/name of the file."
    )
    content: Optional[str] = Field(
        default=None,
        description="The full file contents including the mandatory YAML frontmatter. Required for 'create' and 'update', omit for 'delete'."
    )

class VaultOperationsResponse(BaseModel):
    operations: List[FileOperation] = Field(
        description="A list of deterministic file operations to apply to the vault. If no changes are needed, return an empty list."
    )


# Automatic implicit caching probably lasts around 5 minutes
def generate_content(prompt: str, models=None, max_retries=2) -> str:
    models = models or MODELS

    last_error = None

    # Configure the generation parameters to enforce Structured Outputs
    generation_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=VaultOperationsResponse,
    )

    for model in models:
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=generation_config  # Enforces the JSON schema structurally
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
