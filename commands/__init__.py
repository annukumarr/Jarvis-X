from urllib import response

from .browser import handle_browser
from .memory import handle_memory
from .system import handle_system
from .desktop import handle_desktop


def execute_command(command):

    response = handle_desktop(command)
    if response:
        return response

    response = handle_browser(command)
    if response:
        return response

    response = handle_memory(command)
    if response:
        return response

    response = handle_system(command)
    if response:
        return response

    return None