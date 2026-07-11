"""
commands/desktop/screenshot.py

Purpose:
Handle screenshot commands.
"""

import os
from datetime import datetime

import pyautogui


def handle_screenshot(command):

    command = command.lower().strip()

    if (
        "take screenshot" in command
        or "take a screenshot" in command
        or "capture screen" in command
        or "screenshot" == command
    ):

        try:

            home = os.path.expanduser("~")

            possible_folders = [
                os.path.join(home, "Pictures", "Jarvis Screenshots"),
                os.path.join(
                    home,
                    "OneDrive",
                    "Pictures",
                    "Jarvis Screenshots"
                ),
            ]

            screenshot_folder = None

            for folder in possible_folders:

                parent_folder = os.path.dirname(folder)

                if os.path.exists(parent_folder):
                    screenshot_folder = folder
                    break

            if screenshot_folder is None:
                return "I could not find your Pictures folder, Boss."

            os.makedirs(
                screenshot_folder,
                exist_ok=True
            )

            timestamp = datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S"
            )

            file_name = f"screenshot_{timestamp}.png"

            file_path = os.path.join(
                screenshot_folder,
                file_name
            )

            screenshot = pyautogui.screenshot()

            screenshot.save(file_path)

            return (
                "Screenshot captured and saved, Boss."
            )

        except Exception as error:

            print(f"Screenshot Error: {error}")

            return (
                "I could not capture the screenshot, Boss."
            )

    return None