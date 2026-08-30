"""
brain/decision.py

Purpose:
Decide whether a command requires user confirmation.

This module does not execute actions.
It only classifies the command.
"""

CONFIRMATION_REQUIRED_ACTIONS = {
    "shutdown",
    "restart",
    "delete",
    "remove",
}


def normalize_command(command):
    """
    Normalize the incoming command.
    """

    return command.lower().strip()


def get_action(command):
    """
    Identify whether the command contains
    a confirmation-required action.

    Returns:
        action name -> if confirmation is required
        None        -> otherwise
    """

    command = normalize_command(command)

    # Shutdown
    if command in {
        "shutdown",
        "shutdown pc",
        "shutdown computer",
        "shutdown my pc",
        "shutdown my computer",
        "shut down",
        "shut down pc",
        "shut down computer",
    }:
        return "shutdown"

    # Restart
    if command in {
        "restart",
        "restart pc",
        "restart computer",
        "restart my pc",
        "restart my computer",
    }:
        return "restart"

    # Delete
    if command.startswith("delete "):
        return "delete"

    # Remove
    if command.startswith("remove "):
        return "remove"

    return None


def requires_confirmation(command):
    """
    Check whether a command requires confirmation.
    """

    return get_action(command) is not None