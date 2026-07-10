"""
core/speech.py

Purpose:
Convert speech to text with basic normalization.
"""

import speech_recognition as sr


# Common speech recognition corrections
CORRECTIONS = {
    "ise": "is",
    "whats": "what is",
    "im": "i'm",
    "dont": "don't",
    "cant": "can't",

    # Personal correction
    "anu": "annu",
}


def normalize(command: str) -> str:

    command = command.lower().strip()

    words = command.split()

    corrected = [
        CORRECTIONS.get(word, word)
        for word in words
    ]

    return " ".join(corrected)


def listen():

    recognizer = sr.Recognizer()

    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8

    try:

        with sr.Microphone() as source:

            print("Listening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
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

    except Exception as e:
        print(f"Speech Error: {e}")
        return ""