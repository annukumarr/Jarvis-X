"""
commands/desktop/apps.py

Purpose:
Handle application launching.
"""

import os
import subprocess


def handle_apps(command):

    command = command.lower()

    # Notepad
    if "open notepad" in command:
        subprocess.Popen("notepad")
        return "Opening Notepad, Boss."

    # Calculator
    if "open calculator" in command:
        subprocess.Popen("calc")
        return "Opening Calculator, Boss."

    # File Explorer
    if (
        "open explorer" in command
        or "open file explorer" in command
    ):
        subprocess.Popen("explorer")
        return "Opening File Explorer, Boss."

    # Chrome
    if "open chrome" in command:

        try:
            subprocess.Popen("chrome")

        except FileNotFoundError:
            os.startfile(
                r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            )

        return "Opening Google Chrome, Boss."

    # VS Code
    if (
        "open vscode" in command
        or "open vs code" in command
        or "open visual studio code" in command
    ):

        try:
            subprocess.Popen("code")

        except FileNotFoundError:

            try:
                os.startfile(
                    r"C:\Users\Asus\AppData\Local\Programs\Microsoft VS Code\Code.exe"
                )

            except Exception:
                return "VS Code is not installed."

        return "Opening VS Code, Boss."

    return None