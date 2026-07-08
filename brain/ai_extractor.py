"""
brain/ai_extractor.py

Purpose:
Use Gemini AI to extract memory information
from natural conversations.
"""

import json

from brain.ai import ask_memory_ai


def ai_extract_memory(command):

    prompt = f"""
You are a memory extraction engine.

Your job is to extract only important personal information
from the user's sentence.

Return ONLY valid JSON.

Format:

{{
    "category": "",
    "key": "",
    "value": ""
}}

Examples

Input:
My name is Annu

Output:
{{
    "category":"profile",
    "key":"name",
    "value":"Annu"
}}

Input:
I study at Chandigarh University

Output:
{{
    "category":"profile",
    "key":"college",
    "value":"Chandigarh University"
}}

Input:
My dream company is Microsoft

Output:
{{
    "category":"goal",
    "key":"dream_company",
    "value":"Microsoft"
}}

If nothing should be remembered return:

null

User Sentence:

{command}
"""

    response = ask_memory_ai(prompt)

    if response is None:
        return None

    try:

        data = json.loads(response)

        return data

    except Exception:

        return None