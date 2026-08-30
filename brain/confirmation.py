"""
brain/confirmation.py

Purpose:
Handle user confirmation responses.

This module does not execute actions.
It only determines whether the user confirmed
or rejected a pending action.
"""

YES_PATTERNS = {
    "yes",
    "yeah",
    "yep",
    "yup",
    "yes please",
    "yeah please",
    "sure",
    "okay",
    "ok",
    "confirm",
    "confirmed",
    "do it",
    "go ahead",
    "proceed",
}

NO_PATTERNS = {
    "no",
    "nope",
    "cancel",
    "cancel it",
    "stop",
    "don't",
    "do not",
    "not now",
    "no please",
}


def normalize_confirmation(command):
    """
    Normalize speech-recognition output.
    """

    command = command.lower().strip()

    # Remove common punctuation
    command = command.replace(".", "")
    command = command.replace(",", "")
    command = command.replace("!", "")
    command = command.replace("?", "")

    return command


def is_confirmation(command):
    """
    Check whether the command is a YES response.
    """

    command = normalize_confirmation(command)

    if command in YES_PATTERNS:
        return True

    # Speech recognition may return phrases containing yes.
    if command.startswith("yes "):
        return True

    if command.startswith("yeah "):
        return True

    if command.startswith("yep "):
        return True

    if command.startswith("yup "):
        return True

    return False


def is_rejection(command):
    """
    Check whether the command is a NO response.
    """

    command = normalize_confirmation(command)

    if command in NO_PATTERNS:
        return True

    if command.startswith("no "):
        return True

    if command.startswith("nope "):
        return True

    if command.startswith("cancel "):
        return True

    return False


def get_confirmation_result(command):
    """
    Return the confirmation result.

    Returns:
        True     -> confirmed
        False    -> rejected
        None     -> not a confirmation response
    """

    if is_confirmation(command):
        return True

    if is_rejection(command):
        return False

    return None