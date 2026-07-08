"""
brain/router.py

Purpose:
Central command router for JARVIS-X.

Decides which subsystem should
handle the user's command.
"""


def get_route(command: str):

    command = command.lower().strip()

    # --------------------
    # Browser Commands
    # --------------------
    browser_keywords = [
        "open",
        "youtube",
        "google",
        "chrome",
        "website"
    ]

    # --------------------
    # Memory Commands
    # --------------------
    memory_keywords = [
        "remember",
        "my",
        "i am",
        "i'm",
        "i study",
        "dream",
        "goal",
        "favorite",
        "favourite"
    ]

    # --------------------
    # System Commands
    # --------------------
    system_keywords = [
        "shutdown",
        "restart",
        "sleep",
        "lock",
        "exit",
        "bye"
    ]

    # Browser
    if any(word in command for word in browser_keywords):
        return "browser"

    # Memory
    if any(word in command for word in memory_keywords):
        return "memory"

    # System
    if any(word in command for word in system_keywords):
        return "system"

    # AI
    return "ai"