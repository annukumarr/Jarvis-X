"""
commands/memory.py

Purpose:
Handle all memory-related voice commands.

No database logic.
Uses memory patterns from config.
"""

from settings.memory_patterns import MEMORY_PATTERNS
from database.memory_db import save_memory, get_memory


def handle_memory(command):

    command = command.lower().strip()

    # -----------------------------
    # SAVE MEMORY
    # -----------------------------
    if command.startswith("remember "):

        sentence = command.replace("remember ", "", 1).strip()

        for pattern, (category, key) in MEMORY_PATTERNS.items():

            if sentence.startswith(pattern):

                value = sentence.replace(pattern, "", 1).strip()

                save_memory(category, key, value)

                return f"I'll remember that, Boss. Your {key.replace('_',' ')} is {value}."

    # -----------------------------
    # RECALL MEMORY
    # -----------------------------

    if "what is my dream company" in command:

        company = get_memory("goal", "dream_company")

        if company:
            return f"Your dream company is {company}, Boss."

        return "I don't know your dream company yet."

    if "what is my name" in command:

        name = get_memory("profile", "name")

        if name:
            return f"Your name is {name}, Boss."

        return "I don't know your name yet."

    if "where do i study" in command:

        college = get_memory("profile", "college")

        if college:
            return f"You study at {college}, Boss."

        return "I don't know your college yet."

    return None