"""
commands/memory.py

Purpose:
Handle all memory-related commands.
"""

from brain.memory_engine import process_memory
from settings.memory_patterns import RECALL_PATTERNS
from database.memory_db import save_memory, get_memory


def handle_memory(command):

    command = command.lower().strip()

    # ==========================
    # SAVE MEMORY
    # ==========================

    memory = process_memory(command)

    if memory:

        save_memory(
            memory["category"],
            memory["key"],
            memory["value"]
        )

        return (
            f"I'll remember that, Boss. "
            f"Your {memory['key'].replace('_', ' ')} "
            f"is {memory['value']}."
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