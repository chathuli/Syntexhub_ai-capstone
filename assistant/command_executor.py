"""
Command Executor Module
--------------------------
Maps recognized voice/text commands to concrete actions:
    - tell the time
    - open a website / search the web
    - open a local application
    - exit the assistant

Uses simple keyword matching (rule-based), no ML needed. Keeping this
in its own module makes it easy to extend with new commands later
without touching the voice or auth modules.
"""

import datetime
import subprocess
import sys
import webbrowser


class CommandNotUnderstood(Exception):
    """Raised when no known command pattern matches the input."""
    pass


def tell_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    return f"The time is {now}."


def search_web(query):
    query = query.strip()
    if not query:
        return "You didn't tell me what to search for."
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching the web for {query}."


def open_website(site_name):
    known_sites = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "github": "https://github.com",
        "gmail": "https://mail.google.com",
    }
    url = known_sites.get(site_name.strip().lower())
    if not url:
        return f"I don't have a saved link for {site_name}."
    webbrowser.open(url)
    return f"Opening {site_name}."


def open_application(app_name):
    """
    Opens a local application by name. Platform-dependent.
    Extend APP_PATHS with your own installed apps as needed.
    """
    app_name = app_name.strip().lower()

    APP_COMMANDS = {
        "win32": {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
        },
        "darwin": {
            "notes": "open -a Notes",
            "calculator": "open -a Calculator",
            "textedit": "open -a TextEdit",
        },
        "linux": {
            "calculator": "gnome-calculator",
            "text editor": "gedit",
        },
    }

    platform_key = "win32" if sys.platform.startswith("win") else (
        "darwin" if sys.platform == "darwin" else "linux"
    )
    commands = APP_COMMANDS.get(platform_key, {})
    command = commands.get(app_name)

    if not command:
        return f"I don't know how to open '{app_name}' on this system yet."

    try:
        subprocess.Popen(command, shell=True)
        return f"Opening {app_name}."
    except Exception as e:
        return f"Failed to open {app_name}: {e}"


# ---------------------------------------------------------------------------
# Command routing (rule-based mapping)
# ---------------------------------------------------------------------------
def execute_command(command_text):
    """
    Takes the raw recognized text and routes it to the right action.

    Returns:
        tuple(str response_text, bool should_exit)
    """
    text = command_text.lower().strip()

    if not text:
        return "I didn't catch that. Could you repeat it?", False

    if any(word in text for word in ["exit", "quit", "stop", "goodbye"]):
        return "Goodbye!", True

    if "time" in text:
        return tell_time(), False

    if text.startswith("search for") or text.startswith("search"):
        query = text.replace("search for", "").replace("search", "", 1).strip()
        return search_web(query), False

    if "open youtube" in text:
        return open_website("youtube"), False
    if "open google" in text:
        return open_website("google"), False
    if "open github" in text:
        return open_website("github"), False
    if "open gmail" in text:
        return open_website("gmail"), False

    if text.startswith("open "):
        app_name = text.replace("open", "", 1).strip()
        return open_application(app_name), False

    return (
        "Sorry, I don't have an action mapped for that command yet. "
        "Try: 'what's the time', 'search for <topic>', 'open youtube', or 'open notepad'.",
        False,
    )


SAMPLE_COMMANDS = [
    "what's the time",
    "tell me the time",
    "search for python tutorials",
    "open youtube",
    "open google",
    "open github",
    "open notepad",
    "open calculator",
    "exit / quit / stop",
]


if __name__ == "__main__":
    print("Sample commands this assistant understands:")
    for cmd in SAMPLE_COMMANDS:
        print(f"  - {cmd}")