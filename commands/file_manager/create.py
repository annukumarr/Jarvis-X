"""
commands/file_manager/create.py

Purpose:
Handle folder creation commands and
multi-turn folder creation conversations.
"""

import os
import re


# ==========================
# PENDING FOLDER CREATION
# ==========================

_pending_folder_creation = False


# ==========================
# EXTRACT FOLDER NAME
# ==========================

def extract_folder_name(command):

    command = command.lower().strip()

    patterns = [

        r"^create\s+a\s+folder\s+named\s+(.+)$",

        r"^create\s+a\s+folder\s+name\s+(.+)$",

        r"^create\s+folder\s+named\s+(.+)$",

        r"^create\s+folder\s+name\s+(.+)$",

        r"^create\s+a\s+folder\s+called\s+(.+)$",

        r"^create\s+folder\s+called\s+(.+)$",

        r"^make\s+a\s+folder\s+named\s+(.+)$",

        r"^make\s+a\s+folder\s+name\s+(.+)$",

        r"^make\s+a\s+folder\s+called\s+(.+)$",

        r"^make\s+folder\s+named\s+(.+)$",

        r"^make\s+folder\s+name\s+(.+)$",

        r"^make\s+folder\s+called\s+(.+)$",
    ]

    for pattern in patterns:

        match = re.match(pattern, command)

        if match:

            folder_name = match.group(1).strip()

            if folder_name:
                return folder_name

    return None


# ==========================
# INCOMPLETE COMMAND
# ==========================

def is_create_folder_command(command):

    command = command.lower().strip()

    incomplete_patterns = [

        r"^create\s+a\s+folder$",

        r"^create\s+folder$",

        r"^create\s+a\s+folder\s+name$",

        r"^create\s+folder\s+name$",

        r"^create\s+a\s+folder\s+named$",

        r"^create\s+folder\s+named$",

        r"^create\s+a\s+folder\s+called$",

        r"^create\s+folder\s+called$",

        r"^make\s+a\s+folder$",

        r"^make\s+folder$",

        r"^make\s+a\s+folder\s+name$",

        r"^make\s+folder\s+name$",

        r"^make\s+a\s+folder\s+named$",

        r"^make\s+folder\s+named$",

        r"^make\s+a\s+folder\s+called$",

        r"^make\s+folder\s+called$",
    ]

    for pattern in incomplete_patterns:

        if re.match(pattern, command):
            return True

    return False


# ==========================
# CREATE FOLDER
# ==========================

def create_folder(folder_name):

    documents_path = os.path.join(
        os.path.expanduser("~"),
        "Documents"
    )

    # ==========================
    # SECURITY CHECK
    # ==========================

    if (
        os.path.dirname(folder_name)
        or folder_name in [".", ".."]
        or ".." in folder_name
    ):

        return (
            "Boss, I can only create folders "
            "inside your Documents folder."
        )

    folder_path = os.path.join(
        documents_path,
        folder_name
    )

    # ==========================
    # ALREADY EXISTS
    # ==========================

    if os.path.exists(folder_path):

        return (
            f"The folder {folder_name} "
            f"already exists, Boss."
        )

    # ==========================
    # CREATE
    # ==========================

    try:

        os.makedirs(folder_path)

        return (
            f"{folder_name} folder created "
            f"in Documents, Boss."
        )

    except OSError as e:

        return (
            f"I couldn't create the folder, Boss. "
            f"Error: {e}"
        )


# ==========================
# HANDLE CREATE FOLDER
# ==========================

def handle_create_folder(command):

    global _pending_folder_creation

    command = command.lower().strip()

    # ==================================================
    # STEP 1:
    # JARVIS IS WAITING FOR A FOLDER NAME
    # ==================================================

    if _pending_folder_creation:

        # --------------------------
        # Cancel folder creation
        # --------------------------

        if command in {
            "cancel",
            "cancel it",
            "never mind",
            "nevermind",
            "stop",
            "no"
        }:

            _pending_folder_creation = False

            return (
                "Folder creation cancelled, Boss."
            )

        # --------------------------
        # Ignore empty response
        # --------------------------

        if not command:

            return (
                "Please tell me the name "
                "of the folder, Boss."
            )

        # --------------------------
        # User provided folder name
        # --------------------------

        folder_name = command

        _pending_folder_creation = False

        return create_folder(folder_name)

    # ==================================================
    # STEP 2:
    # COMPLETE COMMAND
    # ==================================================

    folder_name = extract_folder_name(command)

    if folder_name:

        return create_folder(folder_name)

    # ==================================================
    # STEP 3:
    # INCOMPLETE COMMAND
    # ==================================================

    if is_create_folder_command(command):

        _pending_folder_creation = True

        return (
            "Sure, Boss. What should I name "
            "the new folder?"
        )

    return None