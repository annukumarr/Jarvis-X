"""
brain/exit.py

Purpose:
Handle natural commands used to stop JARVIS.
"""

EXIT_COMMANDS = {
    "exit",
    "quit",
    "goodbye",
    "bye",
    "stop",
    "stop listening",
    "go offline",
    "shutdown jarvis",
    "turn off jarvis",
    "close jarvis",
    "sleep",
    "go to sleep",
}


def is_exit_command(command):
    """
    Check whether the user wants JARVIS to stop.
    """

    if not command:
        return False

    command = command.lower().strip()

    return command in EXIT_COMMANDS