"""
core/speech.py

Purpose:
Convert speech to text with robust microphone handling
and command normalization.
"""

import speech_recognition as sr


# ==========================
# SPEECH CORRECTIONS
# ==========================

CORRECTIONS = {
    "ise": "is",
    "whats": "what is",
    "im": "i'm",
    "dont": "don't",
    "cant": "can't",

    # Personal correction
    "anu": "annu",
}


# ==========================
# NORMALIZATION
# ==========================

def normalize(command: str) -> str:

    command = command.lower().strip()

    words = command.split()

    corrected = [
        CORRECTIONS.get(word, word)
        for word in words
    ]

    return " ".join(corrected)


# ==========================
# CREATE RECOGNIZER
# ==========================

def create_recognizer():

    recognizer = sr.Recognizer()

    recognizer.dynamic_energy_threshold = True

    recognizer.energy_threshold = 300

    recognizer.pause_threshold = 0.6

    recognizer.phrase_threshold = 0.2

    recognizer.non_speaking_duration = 0.3

    return recognizer


# ==========================
# LISTEN
# ==========================

def listen():

    recognizer = create_recognizer()

    try:

        with sr.Microphone() as source:

            print("Listening...")

            # Short calibration for each fresh microphone stream.
            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.2
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        command = recognizer.recognize_google(audio)

        command = normalize(command)

        print("You:", command)

        return command

    except sr.WaitTimeoutError:

        return ""

    except sr.UnknownValueError:

        return ""

    except sr.RequestError:

        print("Speech Recognition API Error")

        return ""

    except OSError as e:

        print(f"Microphone Error: {e}")

        return ""

    except KeyboardInterrupt:

        print("\nJARVIS stopped by user.")

        return "exit"

    except Exception as e:

        print(f"Speech Error: {e}")

        return ""


# ==========================
# CONFIRMATION LISTEN
# ==========================

def listen_confirmation():

    recognizer = create_recognizer()

    # Make short words easier to capture.
    recognizer.pause_threshold = 0.4
    recognizer.phrase_threshold = 0.1
    recognizer.non_speaking_duration = 0.2

    try:

        with sr.Microphone() as source:

            print("Waiting for confirmation...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.2
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=3
            )

        command = recognizer.recognize_google(audio)

        command = normalize(command)

        print("You:", command)

        return command

    except sr.WaitTimeoutError:

        return ""

    except sr.UnknownValueError:

        return ""

    except sr.RequestError:

        print("Speech Recognition API Error")

        return ""

    except OSError as e:

        print(f"Microphone Error: {e}")

        return ""

    except KeyboardInterrupt:

        print("\nJARVIS stopped by user.")

        return "exit"

    except Exception as e:

        print(f"Speech Error: {e}")

        return ""