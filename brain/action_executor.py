"""
brain/action_executor.py

Purpose:
Safely execute confirmed system actions.
"""

import os
import subprocess


SAFETY_DELAY = 5


def schedule_shutdown():
    """Schedule Windows shutdown with a safety delay."""

    return subprocess.run(
        ["shutdown", "/s", "/t", str(SAFETY_DELAY)],
        check=False
    )


def schedule_restart():
    """Schedule Windows restart with a safety delay."""

    return subprocess.run(
        ["shutdown", "/r", "/t", str(SAFETY_DELAY)],
        check=False
    )


def cancel_system_action():
    """Cancel a scheduled Windows shutdown/restart."""

    return subprocess.run(
        ["shutdown", "/a"],
        check=False
    )


def delete_file(data):
    """
    Delete a confirmed file.

    The file path comes from the file-manager
    detection result.
    """

    if not isinstance(data, dict):

        return (
            "I couldn't determine which file "
            "should be deleted, Boss."
        )

    file_path = data.get("file_path")
    file_name = data.get("file_name")

    if not file_path:

        return (
            "I couldn't determine the file path, Boss."
        )

    # ==========================================
    # SAFETY CHECK
    # ==========================================

    if not os.path.isfile(file_path):

        return (
            f"{file_name or 'That file'} "
            f"could not be found, Boss."
        )

    try:

        os.remove(file_path)

        return (
            f"{file_name} deleted successfully, Boss."
        )

    except OSError as e:

        return (
            f"I couldn't delete {file_name}, Boss. "
            f"Error: {e}"
        )


def execute_action(action, data=None):
    """
    Execute a confirmed system action.

    Parameters:
        action:
            Action identifier.

        data:
            Optional action-specific data.
    """

    # ==========================================
    # SHUTDOWN
    # ==========================================

    if action == "shutdown":

        schedule_shutdown()

        return (
            f"Shutdown scheduled in "
            f"{SAFETY_DELAY} seconds, Boss."
        )

    # ==========================================
    # RESTART
    # ==========================================

    if action == "restart":

        schedule_restart()

        return (
            f"Restart scheduled in "
            f"{SAFETY_DELAY} seconds, Boss."
        )

    # ==========================================
    # DELETE FILE
    # ==========================================

    if action == "delete_file":

        return delete_file(data)

    # ==========================================
    # UNKNOWN ACTION
    # ==========================================

    return (
        f"I don't know how to execute "
        f"the {action} action yet, Boss."
    )