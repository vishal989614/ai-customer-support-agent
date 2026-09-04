from google import genai

from config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def generate_answer(prompt: str) -> str:

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text