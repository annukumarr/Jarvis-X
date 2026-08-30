"""
commands/file_manager/search.py

Purpose:
Search files inside the user's Documents folder.
"""

import os


def search_files(command):

    command = command.lower().strip()

    prefixes = [
        "search for ",
        "search file ",
        "search files ",
        "find file ",
        "find files ",
        "find my file ",
        "find my files ",
    ]

    search_term = None

    for prefix in prefixes:

        if command.startswith(prefix):

            search_term = command[len(prefix):].strip()
            break

    if not search_term:
        return None

    documents_path = os.path.join(
        os.path.expanduser("~"),
        "Documents"
    )

    if not os.path.exists(documents_path):

        return (
            "Boss, I couldn't find your Documents folder."
        )

    matches = []

    for root, dirs, files in os.walk(documents_path):

        for file_name in files:

            if search_term in file_name.lower():

                full_path = os.path.join(
                    root,
                    file_name
                )

                matches.append(full_path)

    if not matches:

        return (
            f"I couldn't find any file matching "
            f"{search_term}, Boss."
        )

    # Limit output to avoid huge responses.
    matches = matches[:10]

    if len(matches) == 1:

        return (
            f"I found {os.path.basename(matches[0])}, "
            f"Boss. It is located at {matches[0]}."
        )

    response = (
        f"I found {len(matches)} files matching "
        f"{search_term}, Boss:\n"
    )

    for index, path in enumerate(matches, start=1):

        response += (
            f"{index}. {os.path.basename(path)}\n"
        )

    return response