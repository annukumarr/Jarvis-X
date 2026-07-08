"""
brain/memory_filter.py

Purpose:
Filter sentences that are likely
to contain personal memory.
"""

MEMORY_PATTERNS = [

    "my name",
    "my age",
    "my birthday",
    "my college",
    "my university",
    "my dream",
    "my goal",
    "my favourite",
    "my favorite",

    "i am",
    "i'm",

    "i study",

    "i want to become",
    "i want to work",

    "remember"
]


def should_extract_memory(command):

    command = command.lower().strip()

    return any(
        pattern in command
        for pattern in MEMORY_PATTERNS
    )