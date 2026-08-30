"""
commands/file_manager/create_file.py

Purpose:
Handle file creation commands.
"""

import os
import re


# ==========================
# PENDING FILE CREATION
# ==========================

_pending_file_creation = False


# ==========================
# FILE EXTENSIONS
# ==========================

EXTENSIONS = {
    "text": ".txt",
    "txt": ".txt",
    "python": ".py",
    "py": ".py",
    "javascript": ".js",
    "js": ".js",
    "json": ".json",
    "html": ".html",
    "css": ".css",
    "markdown": ".md",
    "md": ".md",
}


# ==========================
# EXTRACT FILE NAME
# ==========================

def extract_file_details(command):

    command = command.lower().strip()

    patterns = [
        r"^create\s+new\s+file\s+(.+)$",
        r"^create\s+a\s+file\s+named\s+(.+)$",
        r"^create\s+file\s+named\s+(.+)$",
        r"^create\s+a\s+file\s+name\s+(.+)$",
        r"^create\s+file\s+name\s+(.+)$",
        r"^create\s+a\s+file\s+called\s+(.+)$",
        r"^create\s+file\s+called\s+(.+)$",
        r"^make\s+a\s+file\s+named\s+(.+)$",
        r"^make\s+file\s+named\s+(.+)$",
        r"^make\s+a\s+file\s+called\s+(.+)$",
        r"^make\s+file\s+called\s+(.+)$",
    ]

    for pattern in patterns:

        match = re.match(pattern, command)

        if match:

            value = match.group(1).strip()

            if value:
                return value

    return None


# ==========================
# INCOMPLETE FILE COMMAND
# ==========================

def is_file_creation_command(command):

    command = command.lower().strip()

    patterns = [
        r"^create\s+new\s+file$",
        r"^create\s+a\s+file$",
        r"^create\s+file$",
        r"^create\s+a\s+file\s+named$",
        r"^create\s+file\s+named$",
        r"^create\s+a\s+file\s+name$",
        r"^create\s+file\s+name$",
        r"^create\s+a\s+file\s+called$",
        r"^create\s+file\s+called$",
        r"^make\s+a\s+file$",
        r"^make\s+file$",
    ]

    for pattern in patterns:

        if re.match(pattern, command):
            return True

    return False


# ==========================
# PARSE FILE NAME + TYPE
# ==========================

def parse_file_name(value):

    value = value.strip()

    # --------------------------------
    # python file
    # --------------------------------

    for file_type, extension in EXTENSIONS.items():

        prefix = f"{file_type} file "

        if value.startswith(prefix):

            file_name = value[len(prefix):].strip()

            if file_name:

                if not file_name.endswith(extension):
                    file_name += extension

                return file_name

    # --------------------------------
    # Default text file
    # --------------------------------

    if "." not in value:
        value += ".txt"

    return value


# ==========================
# CREATE FILE
# ==========================

def create_file(file_name):

    documents_path = os.path.join(
        os.path.expanduser("~"),
        "Documents"
    )

    # Prevent path traversal.
    if (
        os.path.dirname(file_name)
        or file_name in [".", ".."]
        or ".." in file_name
    ):

        return (
            "Boss, I can only create files "
            "inside your Documents folder."
        )

    file_path = os.path.join(
        documents_path,
        file_name
    )

    # ==========================
    # ALREADY EXISTS
    # ==========================

    if os.path.exists(file_path):

        return (
            f"The file {file_name} "
            f"already exists, Boss."
        )

    # ==========================
    # CREATE
    # ==========================

    try:

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ):

            pass

        return (
            f"{file_name} created "
            f"in Documents, Boss."
        )

    except OSError as e:

        return (
            f"I couldn't create the file, Boss. "
            f"Error: {e}"
        )


# ==========================
# HANDLE FILE CREATION
# ==========================

def handle_create_file(command):

    global _pending_file_creation

    command = command.lower().strip()

    # ==================================================
    # PENDING FILE NAME
    # ==================================================

    if _pending_file_creation:

        if command in {
            "cancel",
            "cancel it",
            "never mind",
            "nevermind",
            "stop",
            "no"
        }:

            _pending_file_creation = False

            return (
                "File creation cancelled, Boss."
            )

        if not command:

            return (
                "Please tell me the name "
                "of the file, Boss."
            )

        file_name = parse_file_name(command)

        _pending_file_creation = False

        return create_file(file_name)

    # ==================================================
    # COMPLETE COMMAND
    # ==================================================

    file_value = extract_file_details(command)

    if file_value:

        file_name = parse_file_name(file_value)

        return create_file(file_name)

    # ==================================================
    # INCOMPLETE COMMAND
    # ==================================================

    if is_file_creation_command(command):

        _pending_file_creation = True

        return (
            "Sure, Boss. What should I name "
            "the new file?"
        )

    return None