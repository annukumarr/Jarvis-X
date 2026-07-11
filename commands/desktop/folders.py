"""
commands/desktop/folders.py

Purpose:
Handle Windows folder navigation safely.
"""

import os


def get_folder_path(folder_name):

    home = os.path.expanduser("~")

    possible_paths = [
        os.path.join(home, folder_name),
        os.path.join(home, "OneDrive", folder_name),
    ]

    for path in possible_paths:

        if os.path.exists(path):
            return path

    return None


def open_folder(folder_name):

    path = get_folder_path(folder_name)

    if path is None:
        return False

    try:
        os.startfile(path)
        return True

    except OSError:
        return False


def handle_folders(command):

    command = command.lower().strip()

    # ==========================
    # DOWNLOADS
    # ==========================

    if (
        "open download" in command
        or "open downloads" in command
        or "open download folder" in command
        or "open downloads folder" in command
    ):

        if open_folder("Downloads"):
            return "Opening Downloads folder, Boss."

        return "I could not find the Downloads folder, Boss."

    # ==========================
    # DOCUMENTS
    # ==========================

    if (
        "open document" in command
        or "open documents" in command
        or "open document folder" in command
        or "open documents folder" in command
    ):

        if open_folder("Documents"):
            return "Opening Documents folder, Boss."

        return "I could not find the Documents folder, Boss."

    # ==========================
    # DESKTOP
    # ==========================

    if (
        "open desktop" in command
        or "open desktop folder" in command
    ):

        if open_folder("Desktop"):
            return "Opening Desktop folder, Boss."

        return "I could not find the Desktop folder, Boss."

    # ==========================
    # PICTURES
    # ==========================

    if (
        "open picture" in command
        or "open pictures" in command
        or "open picture folder" in command
        or "open pictures folder" in command
    ):

        if open_folder("Pictures"):
            return "Opening Pictures folder, Boss."

        return "I could not find the Pictures folder, Boss."

    return None