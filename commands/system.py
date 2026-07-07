import datetime


def handle_system(command):

    if "what time" in command:

        current_time = datetime.datetime.now().strftime("%I:%M %p")

        return f"The time is {current_time}"

    elif "exit" in command:

        return "Goodbye Boss"

    return None