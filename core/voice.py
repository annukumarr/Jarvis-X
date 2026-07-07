import asyncio
import edge_tts
import os
from playsound import playsound

VOICE = "en-US-GuyNeural"


async def generate_voice(text):

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )

    await communicate.save("temp.mp3")


def speak(text):

    print("Jarvis:", text)

    asyncio.run(generate_voice(str(text)))

    playsound("temp.mp3")

    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")