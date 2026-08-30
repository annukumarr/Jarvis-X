"""
brain/extractor.py

Purpose:
Extract structured memory from user sentences.

This module DOES NOT save anything.
It only extracts information using rule-based patterns.
"""

from settings.memory_patterns import SAVE_PATTERNS


def extract_memory(command: str):
    """
    Extract structured memory using rule-based patterns.

    Supports natural prefixes such as:

    remember my target company is Microsoft
    remember that my target company is Microsoft
    my target company is Microsoft

    The matching is case-insensitive while the extracted
    value keeps the user's original capitalization.
    """

    if not command:
        return None

    # ======================================================
    # CLEAN INPUT
    # ======================================================

    original_command = command.strip()

    normalized_command = (
        original_command
        .lower()
        .strip()
    )


    # ======================================================
    # REMOVE MEMORY PREFIX
    # ======================================================

    prefixes = (
        "remember that ",
        "remember ",
    )

    for prefix in prefixes:

        if normalized_command.startswith(prefix):

            original_command = (
                original_command[
                    len(prefix):
                ].strip()
            )

            normalized_command = (
                normalized_command[
                    len(prefix):
                ].strip()
            )

            break


    # ======================================================
    # RULE-BASED EXTRACTION
    # ======================================================

    for pattern, (category, key) in SAVE_PATTERNS.items():

        pattern_normalized = (
            pattern
            .lower()
            .strip()
        )


        if normalized_command.startswith(
            pattern_normalized
        ):

            value = (
                original_command[
                    len(pattern_normalized):
                ].strip()
            )


            # ==================================================
            # IGNORE EMPTY VALUES
            # ==================================================

            if not value:
                return None


            return {
                "category": category,
                "key": key,
                "value": value,
            }


    # ======================================================
    # NO LOCAL MATCH
    # ======================================================

    return None