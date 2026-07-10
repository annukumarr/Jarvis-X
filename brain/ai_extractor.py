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

Extract ONLY important personal information.

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

    if not response:
        return None

    # Remove markdown if AI returns ```json ... ```
    response = response.strip()

    if response.startswith("```"):
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

    try:

        data = json.loads(response)

        if data is None:
            return None

        required = {"category", "key", "value"}

        if not required.issubset(data.keys()):
            return None

        if (
            not data["category"]
            or not data["key"]
            or not data["value"]
        ):
            return None

        return data

    except json.JSONDecodeError:
        return None