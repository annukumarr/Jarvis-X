"""
commands/file_manager/__init__.py

Purpose:
Central router for file manager commands.
"""

from .create import handle_create_folder
from .create_file import handle_create_file
from .search import search_files
from .move import handle_move_file
from .rename import handle_rename_file


def handle_file_manager(command):

    response = handle_create_folder(command)

    if response:
        return response

    response = handle_create_file(command)

    if response:
        return response

    response = search_files(command)

    if response:
        return response

    response = handle_move_file(command)

    if response:
        return response

    response = handle_rename_file(command)

    if response:
        return response

    return None