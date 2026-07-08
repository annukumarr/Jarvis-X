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

    except Exception as e:

        return f"AI Error: {e}"


def ask_memory_ai(prompt):

    try:

        return _generate(prompt)

    except Exception:

        return None