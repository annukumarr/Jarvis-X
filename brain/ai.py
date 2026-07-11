"""
brain/ai.py

Purpose:
Handle AI communication safely.
"""

from google import genai

from config import GEMINI_API_KEY
from brain.personality import SYSTEM_PROMPT


client = genai.Client(api_key=GEMINI_API_KEY)


def _generate(prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

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

    except Exception as error:

        error_message = str(error).lower()

        if (
            "503" in error_message
            or "unavailable" in error_message
            or "high demand" in error_message
        ):
            return (
                "My AI service is temporarily busy, Boss. "
                "Please try again in a moment."
            )

        if (
            "429" in error_message
            or "resource_exhausted" in error_message
            or "quota" in error_message
        ):
            return (
                "My AI request limit is temporarily unavailable, Boss. "
                "Please try again later."
            )

        print(f"AI Error: {error}")

        return (
            "I encountered an AI service problem, Boss. "
            "My local commands are still available."
        )


def ask_memory_ai(prompt):

    try:
        return _generate(prompt)

    except Exception as error:

        print(f"Memory AI Error: {error}")

        return None