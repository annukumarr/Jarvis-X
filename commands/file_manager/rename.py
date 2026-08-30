"""
commands/file_manager/rename.py

Purpose:
Rename files in common user folders.
"""

import os


_pending_rename_file = None


SEARCH_LOCATIONS = [
    os.path.join(os.path.expanduser("~"), "Documents"),
    os.path.join(os.path.expanduser("~"), "Downloads"),
    os.path.join(os.path.expanduser("~"), "Desktop"),
]


def extract_rename_details(command):

    command = command.lower().strip()

    prefixes = [
        "rename file ",
        "rename my file ",
    ]

    for prefix in prefixes:

        if command.startswith(prefix):

            value = command[len(prefix):].strip()

            if " to " in value:

                old_name, new_name = value.split(
                    " to ",
                    1
                )

                old_name = old_name.strip()
                new_name = new_name.strip()

                if old_name and new_name:
                    return old_name, new_name

            return value, None

    return None, None


def find_file(file_name):

    for location in SEARCH_LOCATIONS:

        if not os.path.exists(location):
            continue

        for root, dirs, files in os.walk(location):

            for name in files:

                if name.lower() == file_name.lower():

                    return os.path.join(root, name)

    return None


def rename_file(source, new_name):

    directory = os.path.dirname(source)

    target = os.path.join(
        directory,
        new_name
    )

    if os.path.exists(target):

        return (
            f"Boss, {new_name} already exists."
        )

    try:

        os.rename(source, target)

        return (
            f"{os.path.basename(source)} renamed to "
            f"{new_name}, Boss."
        )

    except OSError as e:

        return (
            f"I couldn't rename the file, Boss. "
            f"Error: {e}"
        )


def handle_rename_file(command):

    global _pending_rename_file

    command = command.lower().strip()

    # ==========================
    # WAITING FOR NEW NAME
    # ==========================

    if _pending_rename_file:

        if command in {
            "cancel",
            "cancel it",
            "never mind",
            "nevermind",
            "stop",
        }:

            _pending_rename_file = None

            return "File rename cancelled, Boss."

        source = _pending_rename_file

        _pending_rename_file = None

        # Preserve existing extension
        old_extension = os.path.splitext(source)[1]

        new_name = command

        if not os.path.splitext(new_name)[1]:
            new_name += old_extension

        return rename_file(
            source,
            new_name
        )

    # ==========================
    # EXTRACT COMMAND
    # ==========================

    old_name, new_name = extract_rename_details(command)

    if not old_name:
        return None

    source = find_file(old_name)

    if not source:

        return (
            f"I couldn't find {old_name}, Boss."
        )

    # ==========================
    # DIRECT RENAME
    # ==========================

    if new_name:

        if not os.path.splitext(new_name)[1]:

            extension = os.path.splitext(source)[1]

            new_name += extension

        return rename_file(
            source,
            new_name
        )

    # ==========================
    # MULTI-TURN RENAME
    # ==========================

    _pending_rename_file = source

    return (
        f"I found {os.path.basename(source)}, Boss. "
        f"What should I rename it to?"
    )