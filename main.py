from core.voice import speak
from core.speech import listen

from commands import execute_command
from brain.ai import ask_ai
from database.db import initialize_database


def main():

    # Initialize database
    initialize_database()

    # Start Jarvis
    speak("Hello Boss, Jarvis is online.")

    while True:

        command = listen()

        if not command:
            continue

        # Check built-in commands
        response = execute_command(command)

        # If no command matched, ask AI
        if response is None:
            response = ask_ai(command)

        # Exit
        if command in ["exit", "quit", "goodbye", "bye"]:
            speak("Goodbye Boss.")
            break

        # Speak response
        speak(response)


if __name__ == "__main__":
    main()