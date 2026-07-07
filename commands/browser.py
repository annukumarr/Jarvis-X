import webbrowser


def handle_browser(command):

    if "open youtube" in command:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube Boss"

    elif "open google" in command:
        webbrowser.open("https://google.com")
        return "Opening Google Boss"

    return None