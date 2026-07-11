"""
commands/desktop/media.py

Purpose:
Handle Windows media and volume controls.
"""

import pyautogui


def handle_media(command):

    command = command.lower().strip()

    # ==========================
    # VOLUME UP
    # ==========================

    if (
        "volume up" in command
        or "increase volume" in command
        or "raise volume" in command
    ):

        pyautogui.press("volumeup", presses=5)

        return "Increasing volume, Boss."

    # ==========================
    # VOLUME DOWN
    # ==========================

    if (
        "volume down" in command
        or "decrease volume" in command
        or "lower volume" in command
    ):

        pyautogui.press("volumedown", presses=5)

        return "Decreasing volume, Boss."

    # ==========================
    # MUTE
    # ==========================

    if (
        "mute volume" in command
        or "mute sound" in command
        or command == "mute"
    ):

        pyautogui.press("volumemute")

        return "Volume muted, Boss."

    # ==========================
    # UNMUTE
    # ==========================

    if (
        "unmute volume" in command
        or "unmute sound" in command
        or command == "unmute"
    ):

        pyautogui.press("volumemute")

        return "Volume unmuted, Boss."

    return None