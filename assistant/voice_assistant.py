"""
Voice Assistant Module
------------------------
Handles speech-to-text (listening for commands) and text-to-speech
(speaking responses). This is the core of Project 1, reused here as
a module inside the capstone.
"""

import speech_recognition as sr
import pyttsx3


class VoiceAssistantError(Exception):
    """Raised for microphone/recognition failures."""
    pass


# ---------------------------------------------------------------------------
# Text-to-Speech
# ---------------------------------------------------------------------------
_tts_engine = None


def _get_tts_engine():
    global _tts_engine
    if _tts_engine is None:
        _tts_engine = pyttsx3.init()
        _tts_engine.setProperty("rate", 175)
    return _tts_engine


def speak(text):
    """Speaks the given text aloud and also prints it for visibility/logging."""
    print(f"Assistant: {text}")
    engine = _get_tts_engine()
    engine.say(text)
    engine.runAndWait()


# ---------------------------------------------------------------------------
# Speech-to-Text
# ---------------------------------------------------------------------------
def listen_command(timeout=5, phrase_time_limit=6):
    """
    Listens via microphone and returns the recognized command as lowercase text.

    Returns:
        str: recognized text (lowercase), or "" if nothing understandable was heard
    """
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    except sr.WaitTimeoutError:
        print("Listening timed out - no speech detected.")
        return ""
    except OSError as e:
        raise VoiceAssistantError(
            f"Microphone not accessible: {e}. Check that a microphone is connected."
        )

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        raise VoiceAssistantError(
            f"Speech recognition service error: {e}. Check your internet connection."
        )


if __name__ == "__main__":
    # Standalone test: python voice_assistant.py
    speak("Voice assistant module ready. Say something.")
    heard = listen_command()
    if heard:
        speak(f"You said: {heard}")
    else:
        speak("I didn't catch that.")