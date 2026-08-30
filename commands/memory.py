"""
commands/memory.py

Purpose:
Handle all memory-related commands.

This module:
- Saves memories
- Recalls specific memories
- Searches memories using natural queries
- Returns owner memory information

No AI is required for deterministic memory recall.
"""

import re

from brain.memory_engine import process_memory

from settings.memory_patterns import RECALL_PATTERNS

from database.memory_db import (
    save_memory,
    get_memory,
    get_all_memories,
    search_memories,
)


# ==========================================================
# GENERIC MEMORY SEARCH
# ==========================================================

def _extract_memory_search_query(
    command: str,
):
    """
    Extract the subject from natural memory questions.

    Example:

        what do you remember about Microsoft?

    Returns:

        Microsoft
    """

    patterns = [
        r"what do you remember about (.+)",
        r"what do you know about (.+)",
        r"do you remember (.+)",
        r"tell me what you remember about (.+)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            command,
            re.IGNORECASE,
        )

        if match:

            query = match.group(1).strip()

            query = query.rstrip(
                "?.!"
            )

            return query.strip()

    return None


# ==========================================================
# FORMAT SEARCH RESULTS
# ==========================================================

def _format_memory_results(
    query: str,
    results: list,
):

    if not results:

        return (
            f"I don't have any memory related to "
            f"{query}, Boss."
        )

    response = [
        f"Here's what I remember about {query}, Boss:"
    ]

    for memory in results:

        category = (
            memory["category"]
            .replace("_", " ")
            .title()
        )

        key = (
            memory["key"]
            .replace("_", " ")
            .title()
        )

        value = memory["value"]

        response.append(
            f"- {key}: {value}"
        )

    return "\n".join(response)


# ==========================================================
# MAIN MEMORY HANDLER
# ==========================================================

def handle_memory(command):

    command = command.lower().strip()


    # ======================================================
    # USER PROFILE SUMMARY
    # ======================================================

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
                    f"- "
                    f"{key.replace('_', ' ').title()}: "
                    f"{value}"
                )

            response.append("")

        return "\n".join(response)


    # ======================================================
    # GENERIC MEMORY SEARCH
    # ======================================================

    search_query = (
        _extract_memory_search_query(
            command
        )
    )

    if search_query:

        results = search_memories(
            search_query
        )

        if results:

            return _format_memory_results(
                search_query,
                results,
            )


    # ======================================================
    # SAVE MEMORY
    # ======================================================

    memory = process_memory(command)

    if memory:

        save_memory(
            memory["category"],
            memory["key"],
            memory["value"],
        )

        return (
            f"I'll remember that, Boss. "
            f"Your "
            f"{memory['key'].replace('_', ' ')} "
            f"is "
            f"{memory['value']}."
        )


    # ======================================================
    # SPECIFIC RECALL
    # ======================================================

    for pattern, (
        category,
        key,
    ) in RECALL_PATTERNS.items():

        if pattern in command:

            value = get_memory(
                category,
                key,
            )

            if value:

                return (
                    f"Your "
                    f"{key.replace('_', ' ')} "
                    f"is {value}, Boss."
                )

            return (
                f"I don't know your "
                f"{key.replace('_', ' ')} yet."
            )


    # ======================================================
    # NO MEMORY ACTION
    # ======================================================

    return None