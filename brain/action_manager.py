"""
brain/action_manager.py

Purpose:
Manage actions that require confirmation.

This module connects:

- Decision Engine
- Pending Action
- Confirmation Engine
- File Manager

It does NOT execute system actions.
"""

from brain.decision import get_action
from brain.confirmation import get_confirmation_result

from brain.pending_action import (
    set_pending_action,
    get_pending_action,
    clear_pending_action,
)

from commands.file_manager.delete import (
    handle_delete_file,
)


# ==========================================================
# CHECK COMMAND
# ==========================================================

def check_command(command):
    """
    Check whether a command requires confirmation.

    Returns:
        None
            -> no confirmation required

        str
            -> confirmation message
    """

    command = command.lower().strip()

    # ======================================================
    # DELETE FILE
    # ======================================================

    delete_data = handle_delete_file(command)

    # IMPORTANT:
    # handle_delete_file() may return:
    #
    # None
    # dict
    # string
    #
    # Only a dictionary represents a valid pending
    # delete action.

    if isinstance(delete_data, dict):

        set_pending_action(
            action="delete_file",
            data=delete_data,
        )

        file_name = delete_data.get(
            "file_name",
            "the requested file",
        )

        return (
            f"Boss, deleting '{file_name}' "
            f"requires your confirmation. "
            f"Do you want me to proceed?"
        )

    # If the file manager returned an informational
    # response, do not create a pending action here.
    #
    # The caller can continue normal processing.
    if isinstance(delete_data, str):

        # A valid "couldn't find" response should be
        # returned to the caller instead of crashing.
        return delete_data

    # ======================================================
    # OTHER CONFIRMATION ACTIONS
    # ======================================================

    action = get_action(command)

    if action is None:
        return None

    set_pending_action(
        action=action,
        data=command,
    )

    return (
        f"Boss, the '{action}' action requires "
        f"your confirmation. Do you want me to proceed?"
    )


# ==========================================================
# HANDLE CONFIRMATION
# ==========================================================

def handle_confirmation(command):
    """
    Handle YES/NO response for a pending action.

    Returns:
        None
            -> no pending action

        dict
            -> confirmation result
    """

    pending = get_pending_action()

    if pending is None:
        return None

    result = get_confirmation_result(
        command
    )

    # ======================================================
    # CONFIRMED
    # ======================================================

    if result is True:

        action = pending["action"]
        data = pending["data"]

        clear_pending_action()

        return {
            "confirmed": True,
            "action": action,
            "data": data,
        }

    # ======================================================
    # CANCELLED
    # ======================================================

    if result is False:

        action = pending["action"]

        clear_pending_action()

        return {
            "confirmed": False,
            "action": action,
            "data": None,
        }

    # ======================================================
    # UNKNOWN RESPONSE
    # ======================================================

    return {
        "confirmed": None,
        "action": pending["action"],
        "data": pending["data"],
    }