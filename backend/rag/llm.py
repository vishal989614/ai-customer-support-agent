from google import genai

from config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


import re
import time


def generate_answer(prompt: str, max_retries: int = 4) -> str:

    candidate_models = ["gemini-2.5-flash", "gemini-3.5-flash-lite", "gemini-3.6-flash"]

    for model_name in candidate_models:
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                error_str = str(e)
                is_transient = any(
                    code in error_str
                    for code in ["429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE"]
                )
                if is_transient and attempt < max_retries - 1:
                    delay = 1.5 * (attempt + 1)
                    time.sleep(delay)
                    continue
                break  # try next candidate model

    # If all models failed, raise last exception
    raise RuntimeError("All Gemini model candidates failed.")