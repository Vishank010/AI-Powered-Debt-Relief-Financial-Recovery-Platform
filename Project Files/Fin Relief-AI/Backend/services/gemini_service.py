"""
Google Gemini API Integration
------------------------------
Thin wrapper around the Gemini generateContent REST endpoint.
If no API key is configured, or the API call fails for any reason,
callers should catch the exception and fall back to rule-based logic
(see services/negotiation_engine.py).
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-flash:generateContent"
)


class GeminiUnavailableError(Exception):
    pass


def generate_content(prompt: str, max_output_tokens: int = 800) -> str:
    """Call Gemini API with a prompt and return generated text.

    Raises GeminiUnavailableError if no API key is set or the request fails,
    so the caller can fall back to rule-based generation.
    """
    if not GEMINI_API_KEY:
        raise GeminiUnavailableError("GEMINI_API_KEY not configured")

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": max_output_tokens,
        },
    }

    try:
        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json=payload,
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as exc:
        raise GeminiUnavailableError(str(exc))
