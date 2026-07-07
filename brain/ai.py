from google import genai
from config import GEMINI_API_KEY
from brain.personality import SYSTEM_PROMPT

client = genai.Client(api_key=GEMINI_API_KEY)


def ask_ai(prompt):

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
{SYSTEM_PROMPT}

User:
{prompt}
"""
        )

        return response.text.strip()

    except Exception as e:

        return f"AI Error: {e}"