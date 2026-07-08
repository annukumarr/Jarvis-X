"""
commands/memory.py

Purpose:
Handle all memory-related voice commands.
"""

from settings.memory_patterns import SAVE_PATTERNS, RECALL_PATTERNS
from database.memory_db import save_memory, get_memory


def handle_memory(command):

    command = command.lower().strip()

    # ==========================
    # SAVE MEMORY
    # ==========================

    if command.startswith("remember "):

        sentence = command.replace("remember ", "", 1).strip()

        for pattern, (category, key) in SAVE_PATTERNS.items():

            if sentence.startswith(pattern):

                value = sentence.replace(pattern, "", 1).strip()

                save_memory(category, key, value)

                return (
                    f"I'll remember that, Boss. "
                    f"Your {key.replace('_', ' ')} is {value}."
                )

    # ==========================
    # RECALL MEMORY
    # ==========================

    for pattern, (category, key) in RECALL_PATTERNS.items():

        if pattern in command:

            value = get_memory(category, key)

            if value:

                return (
                    f"Your {key.replace('_', ' ')} "
                    f"is {value}, Boss."
                )

            return (
                f"I don't know your "
                f"{key.replace('_', ' ')} yet."
            )

    return None