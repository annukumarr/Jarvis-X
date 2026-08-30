from core.voice import speak
from core.speech import listen, listen_confirmation

from commands import execute_command

from brain.ai import ask_ai

from brain.action_manager import (
    check_command,
    handle_confirmation,
)

from brain.pending_action import (
    get_pending_action,
)

from brain.action_executor import (
    execute_action,
)

from brain.exit import is_exit_command

from database.db import initialize_database


def main():

    # ==========================
    # INITIALIZE DATABASE
    # ==========================

    initialize_database()

    # ==========================
    # START JARVIS
    # ==========================

    speak("Hello Boss, Jarvis is online.")

    while True:

        # ==========================
        # CHECK PENDING ACTION
        # ==========================

        pending = get_pending_action()

        if pending is not None:

            # Use dedicated confirmation listener
            command = listen_confirmation()

            if not command:

                speak(
                    "I didn't hear your response, Boss. "
                    "Please say yes or no."
                )

                continue

            # ==========================
            # HANDLE CONFIRMATION
            # ==========================

            confirmation = handle_confirmation(command)

            if confirmation is None:
                continue

            # ==========================
            # CONFIRMED
            # ==========================

            if confirmation["confirmed"] is True:

                action = confirmation["action"]
                data = confirmation["data"]

                speak(
                    f"Confirmed, Boss. "
                    f"Executing {action}."
                )

                response = execute_action(
                    action,
                    data
                )

                speak(response)

                continue

            # ==========================
            # CANCELLED
            # ==========================

            if confirmation["confirmed"] is False:

                action = confirmation["action"]

                # Make the action name user-friendly
                if action == "delete_file":
                    action_name = "Delete"

                else:
                    action_name = action.capitalize()

                speak(
                    f"{action_name} action "
                    f"cancelled, Boss."
                )

                continue

            # ==========================
            # UNKNOWN RESPONSE
            # ==========================

            speak(
                "Please answer yes or no, Boss."
            )

            continue

        # ==========================
        # NORMAL COMMAND LISTENER
        # ==========================

        command = listen()

        if not command:
            continue

        # ==========================
        # EXIT / OFFLINE COMMAND
        # ==========================

        if is_exit_command(command):

            speak(
                "Going offline, Boss. See you soon."
            )

            break

        # ==========================
        # CHECK CONFIRMATION REQUIRED
        # ==========================

        confirmation_message = check_command(command)

        if confirmation_message:

            speak(confirmation_message)

            continue

        # ==========================
        # BUILT-IN COMMANDS
        # ==========================

        response = execute_command(command)

        # ==========================
        # AI FALLBACK
        # ==========================

        if response is None:

            response = ask_ai(command)

        # ==========================
        # SPEAK RESPONSE
        # ==========================

        speak(response)


if __name__ == "__main__":
    main()