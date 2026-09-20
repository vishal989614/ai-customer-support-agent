from google import genai

from config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


import re
import time


def generate_answer(prompt: str, max_retries: int = 4) -> str:

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )
            return response.text

        except Exception as e:
            error_str = str(e)
            is_transient = any(
                code in error_str
                for code in ["429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE"]
            )

            if is_transient and attempt < max_retries - 1:
                # Extract suggested retry delay from error message if available
                match = re.search(
                    r"retry in (\d+(?:\.\d+)?)s",
                    error_str,
                    re.IGNORECASE
                )
                if match:
                    delay = float(match.group(1)) + 1.0
                else:
                    delay = 5.0 * (attempt + 1)

                print(
                    f"\n[Gemini API Rate Limit / Demand Spike] "
                    f"Waiting {delay:.1f}s before retry ({attempt + 1}/{max_retries})..."
                )
                time.sleep(delay)
                continue

            raise e