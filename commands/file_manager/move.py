"""
commands/file_manager/move.py

Purpose:
Move files between common user folders.
"""

import os
import shutil


_pending_move_file = None


FOLDER_MAP = {
    "documents": os.path.join(os.path.expanduser("~"), "Documents"),
    "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
    "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
    "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
    "music": os.path.join(os.path.expanduser("~"), "Music"),
    "videos": os.path.join(os.path.expanduser("~"), "Videos"),
}


def extract_move_details(command):

    command = command.lower().strip()

    prefixes = [
        "move file ",
        "move my file ",
    ]

    for prefix in prefixes:

        if command.startswith(prefix):

            value = command[len(prefix):].strip()

            if value:
                return value

    return None


def find_file(file_name):

    search_locations = [
        FOLDER_MAP["documents"],
        FOLDER_MAP["downloads"],
        FOLDER_MAP["desktop"],
    ]

    for location in search_locations:

        if not os.path.exists(location):
            continue

        for root, dirs, files in os.walk(location):

            for name in files:

                if name.lower() == file_name.lower():

                    return os.path.join(root, name)

    return None


def handle_move_file(command):

    global _pending_move_file

    command = command.lower().strip()

    # ==========================
    # WAITING FOR DESTINATION
    # ==========================

    if _pending_move_file:

        if command in {
            "cancel",
            "cancel it",
            "never mind",
            "nevermind",
            "stop",
        }:

            _pending_move_file = None

            return "File move cancelled, Boss."

        destination = FOLDER_MAP.get(command)

        if not destination:

            return (
                "Boss, please specify Documents, "
                "Downloads, Desktop, Pictures, "
                "Music, or Videos."
            )

        source = _pending_move_file

        _pending_move_file = None

        try:

            os.makedirs(destination, exist_ok=True)

            target = os.path.join(
                destination,
                os.path.basename(source)
            )

            if os.path.exists(target):

                return (
                    "Boss, a file with the same name "
                    "already exists there."
                )

            shutil.move(source, target)

            return (
                f"{os.path.basename(source)} moved to "
                f"{command.capitalize()}, Boss."
            )

        except OSError as e:

            return (
                f"I couldn't move the file, Boss. "
                f"Error: {e}"
            )

    # ==========================
    # EXTRACT FILE
    # ==========================

    file_name = extract_move_details(command)

    if not file_name:
        return None

    source = find_file(file_name)

    if not source:

        return (
            f"I couldn't find {file_name}, Boss."
        )

    _pending_move_file = source

    return (
        f"I found {os.path.basename(source)}, Boss. "
        f"Where should I move it?"
    )