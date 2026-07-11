"""
commands/desktop/power.py

Purpose:
Handle safe Windows power commands.
"""

import os


def handle_power(command):

    command = command.lower().strip()

    # ==========================
    # LOCK PC
    # ==========================

    if command in [
        "lock",
        "lock pc",
        "lock computer",
        "lock my pc",
        "lock my computer",
    ]:

        os.system(
            "rundll32.exe user32.dll,LockWorkStation"
        )

        return "Locking your computer, Boss."

    # ==========================
    # SHUTDOWN
    # ==========================

    if command in [
        "shutdown",
        "shutdown pc",
        "shutdown computer",
        "shutdown my pc",
        "shutdown my computer",
        "shut down",
        "shut down pc",
        "shut down computer",
        "shut down my pc",
        "shut down my computer",
    ]:

        return (
            "Shutdown command detected, Boss. "
            "Confirmation system is not enabled yet."
        )

    # ==========================
    # RESTART
    # ==========================

    if command in [
        "restart",
        "restart pc",
        "restart computer",
        "restart my pc",
        "restart my computer",
    ]:

        return (
            "Restart command detected, Boss. "
            "Confirmation system is not enabled yet."
        )

    return None