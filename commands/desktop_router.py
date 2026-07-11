"""
commands/desktop.py

Purpose:
Desktop automation router.
"""

from .desktop.apps import handle_apps
from .desktop.folders import handle_folders
from .desktop.media import handle_media
from .desktop.power import handle_power
from .desktop.screenshot import handle_screenshot


def handle_desktop(command):

    response = handle_apps(command)
    if response:
        return response

    response = handle_folders(command)
    if response:
        return response

    response = handle_media(command)
    if response:
        return response

    response = handle_power(command)
    if response:
        return response

    response = handle_screenshot(command)
    if response:
        return response

    return None