"""
brain/extractor.py

Purpose:
Extract structured memory from user sentences.

This module DOES NOT save anything.
It only extracts information using rule-based patterns.
"""

from settings.memory_patterns import SAVE_PATTERNS


def extract_memory(command: str):

    command = command.lower().strip()

    # Remove optional prefix
    if command.startswith("remember "):
        command = command[len("remember "):].strip()

    # Rule-based extraction
    for pattern, (category, key) in SAVE_PATTERNS.items():

        if command.startswith(pattern):

            value = command[len(pattern):].strip()

            # Ignore empty values
            if not value:
                return None

            return {
                "category": category,
                "key": key,
                "value": value
            }

    return None