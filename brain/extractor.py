"""
brain/extractor.py

Purpose:
Extract memory information from user sentences.

This module DOES NOT save anything.
It only returns extracted information.
"""

from settings.memory_patterns import SAVE_PATTERNS


def extract_memory(command: str):

    command = command.lower().strip()

    # Remove "remember" if user says it
    if command.startswith("remember "):
        command = command.replace("remember ", "", 1).strip()

    for pattern, (category, key) in SAVE_PATTERNS.items():

        if command.startswith(pattern):

            value = command.replace(pattern, "", 1).strip()

            return {
                "category": category,
                "key": key,
                "value": value
            }

    return None