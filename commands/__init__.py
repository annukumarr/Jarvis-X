"""
commands/__init__.py

Purpose:
Central command router for JARVIS-X.
"""

from .browser import handle_browser
from .memory import handle_memory
from .file_manager import handle_file_manager
from .desktop_router import handle_desktop
from .system import handle_system


def execute_command(command):

    # ==========================
    # BROWSER
    # ==========================

    response = handle_browser(command)

    if response:
        return response

    # ==========================
    # MEMORY
    # ==========================

    response = handle_memory(command)

    if response:
        return response

    # ==========================
    # FILE MANAGER
    # ==========================

    response = handle_file_manager(command)

    if response:
        return response

    # ==========================
    # DESKTOP
    # ==========================

    response = handle_desktop(command)

    if response:
        return response

    # ==========================
    # SYSTEM
    # ==========================

    response = handle_system(command)

    if response:
        return response

    # ==========================
    # NO COMMAND MATCHED
    # ==========================

    return None