"""
brain/ai.py

Purpose:
Central AI interface for JARVIS-X.

All Gemini requests come through this file.
"""

from google import genai

from config import GEMINI_API_KEY
from brain.personality import SYSTEM_PROMPT


MODEL_NAME = "gemini-2.5-flash"

client = genai.Client(api_key=GEMINI_API_KEY)


def _generate(prompt):

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response or not response.text:
        return None

    return response.text.strip()


def ask_ai(prompt):

    try:

        return _generate(
            f"""
{SYSTEM_PROMPT}

User:
{prompt}
"""
        )

    except Exception as e:

        return f"AI Error: {e}"


def ask_memory_ai(prompt):

    try:

        return _generate(prompt)

    except Exception:

        return None