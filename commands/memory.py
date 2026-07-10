"""
commands/memory.py

Purpose:
Handle all memory-related commands.
"""

from brain.memory_engine import process_memory
from settings.memory_patterns import RECALL_PATTERNS
from database.memory_db import (
    save_memory,
    get_memory,
    get_all_memories
)


def handle_memory(command):

    command = command.lower().strip()

    # ==========================
    # USER PROFILE SUMMARY
    # ==========================

    if (
        "what do you know about me" in command
        or "tell me about myself" in command
        or "summarize my profile" in command
    ):

        memories = get_all_memories()

        if not memories:
            return (
                "I don't know much about you yet, Boss."
            )

        response = [
            "Here's what I know about you, Boss:\n"
        ]

        for category, values in memories.items():

            response.append(
                f"{category.title()}:"
            )

            for key, value in values.items():

                response.append(
                    f"- {key.replace('_', ' ').title()}: {value}"
                )

            response.append("")

        return "\n".join(response)

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