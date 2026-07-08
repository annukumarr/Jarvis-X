"""
brain/memory_filter.py

Purpose:
Decide whether a sentence is likely to
contain personal memory.
"""

MEMORY_KEYWORDS = [

    "my",
    "i am",
    "i'm",
    "i study",
    "my dream",
    "my goal",
    "i want",
    "favorite",
    "favourite",
    "birthday",
    "age",
    "college",
    "university",
    "language",
    "food",
    "wake",
    "sleep"
]


def should_extract_memory(command):

    command = command.lower()

    for keyword in MEMORY_KEYWORDS:

        if keyword in command:
            return True

    return False