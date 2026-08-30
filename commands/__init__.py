"""
commands/__init__.py

Purpose:
Central command router for JARVIS-X.
"""

from .browser import handle_browser
from .memory import handle_memory
from .file_manager import handle_file_manager
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
    #
    # IMPORTANT:
    # Desktop modules are imported lazily.
    #
    # This prevents desktop dependencies such as
    # pyautogui from being loaded when the API/server
    # is starting in a cloud environment.
    #
    # Personal/local JARVIS still gets the complete
    # desktop functionality when execute_command()
    # actually reaches this section.
    # ==========================

    from .desktop_router import handle_desktop

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