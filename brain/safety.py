"""
brain/safety.py

Purpose:
Provide safety checks before executing
high-risk system actions.
"""

DANGEROUS_ACTIONS = {
    "shutdown",
    "restart",
}


def is_dangerous_action(action):
    """
    Check whether an action is considered dangerous.
    """

    return action in DANGEROUS_ACTIONS


def get_safety_message(action):
    """
    Return a safety message for a dangerous action.
    """

    if action == "shutdown":

        return (
            "Your computer will shut down shortly, Boss."
        )

    if action == "restart":

        return (
            "Your computer will restart shortly, Boss."
        )

    return None