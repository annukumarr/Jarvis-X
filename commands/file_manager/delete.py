"""
commands/file_manager/delete.py

Purpose:
Find files and prepare them for deletion.

Deletion itself is performed only after
the existing confirmation system approves it.
"""

import os


SEARCH_LOCATIONS = [
    os.path.join(os.path.expanduser("~"), "Documents"),
    os.path.join(os.path.expanduser("~"), "Downloads"),
    os.path.join(os.path.expanduser("~"), "Desktop"),
]


def extract_file_name(command):

    command = command.lower().strip()

    prefixes = [
        "delete file ",
        "delete my file ",
        "remove file ",
        "remove my file ",
    ]

    for prefix in prefixes:

        if command.startswith(prefix):

            file_name = command[len(prefix):].strip()

            if file_name:
                return file_name

    return None


def find_file(file_name):

    for location in SEARCH_LOCATIONS:

        if not os.path.exists(location):
            continue

        for root, dirs, files in os.walk(location):

            for name in files:

                if name.lower() == file_name.lower():

                    return os.path.join(root, name)

    return None


def handle_delete_file(command):

    file_name = extract_file_name(command)

    if not file_name:
        return None

    file_path = find_file(file_name)

    if not file_path:

        return (
            f"I couldn't find {file_name}, Boss."
        )

    return {
        "action": "delete_file",
        "file_name": os.path.basename(file_path),
        "file_path": file_path,
    }