from __future__ import annotations

import os

from src.config import SETTINGS


class AnswerGenerator:
    def __init__(self) -> None:
        if SETTINGS.generation_provider != "gemini":
            raise RuntimeError(
                f"Unsupported generation provider: {SETTINGS.generation_provider}"
            )

        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "Missing Gemini API key. Set GEMINI_API_KEY in your .env file."
            )

    def generate(self, prompt: str) -> str:
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError(
                "Missing dependency: google-genai. Run `pip install -r requirements.txt`."
            ) from exc

        client = genai.Client(api_key=self.api_key)
        response = client.models.generate_content(
            model=SETTINGS.generation_model,
            contents=prompt,
        )
        return response.text or ""
