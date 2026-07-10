"""
core/voice.py

Purpose:
Convert text to speech safely.
JARVIS should never crash because of TTS.
"""

import asyncio
import os

import edge_tts
from playsound import playsound


VOICE = "en-US-GuyNeural"
TEMP_FILE = "temp.mp3"


async def generate_voice(text):

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )

    await communicate.save(TEMP_FILE)


def speak(text):

    text = str(text)

    print("Jarvis:", text)

    try:

        asyncio.run(generate_voice(text))

        if os.path.exists(TEMP_FILE):

            playsound(TEMP_FILE)

    except KeyboardInterrupt:
        print("Voice playback interrupted.")

    except Exception as e:
        print(f"TTS Error: {e}")

    finally:

        if os.path.exists(TEMP_FILE):

            try:
                os.remove(TEMP_FILE)
            except Exception:
                pass