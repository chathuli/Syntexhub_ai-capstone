"""
End-to-End AI Capstone - Main CLI
------------------------------------
Flow:
    1. Authenticate the user via face recognition (webcam).
    2. If authenticated, greet them by name.
    3. Loop: listen for a voice command -> execute the mapped action ->
       speak the response -> repeat until the user says "exit"/"quit".

Run:
    python main.py

Requires:
    - encodings.pickle in the project root (copy from your
      face-recognition project, or generate fresh via register_faces.py
      + encode_faces.py from that earlier project).
    - A working microphone and webcam.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "auth"))
sys.path.append(os.path.join(os.path.dirname(__file__), "assistant"))

from face_auth import authenticate_user, FaceAuthError
from voice_assistant import speak, listen_command, VoiceAssistantError
from command_executor import execute_command, SAMPLE_COMMANDS


ENCODINGS_PATH = os.path.join(os.path.dirname(__file__), "encodings.pickle")
AUTH_TIMEOUT_SECONDS = 10
MAX_AUTH_ATTEMPTS = 3


def run_authentication():
    print("=" * 50)
    print("STEP 1: Face Authentication")
    print("=" * 50)

    for attempt in range(1, MAX_AUTH_ATTEMPTS + 1):
        try:
            name = authenticate_user(
                encodings_path=ENCODINGS_PATH, timeout_seconds=AUTH_TIMEOUT_SECONDS
            )
        except FaceAuthError as e:
            print(f"Authentication error: {e}")
            return None

        if name:
            return name

        print(f"Attempt {attempt}/{MAX_AUTH_ATTEMPTS}: No known face detected in time.")

    return None


def run_assistant_loop(user_name):
    print("=" * 50)
    print("STEP 2: Voice Command Mode")
    print("=" * 50)
    print("Sample commands you can try:")
    for cmd in SAMPLE_COMMANDS:
        print(f"  - {cmd}")
    print()

    speak(f"Welcome, {user_name.replace('_', ' ')}. How can I help you?")

    while True:
        try:
            command_text = listen_command()
        except VoiceAssistantError as e:
            speak(f"There was a problem with the microphone: {e}")
            continue

        if not command_text:
            speak("I didn't catch that. Please try again.")
            continue

        response, should_exit = execute_command(command_text)
        speak(response)

        if should_exit:
            break


def main():
    user_name = run_authentication()

    if not user_name:
        print("Authentication failed. Exiting.")
        try:
            speak("Authentication failed. Access denied.")
        except Exception:
            pass  # in case TTS itself fails, don't crash on the way out
        sys.exit(1)

    print(f"Authenticated as: {user_name}")

    try:
        run_assistant_loop(user_name)
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")
    except VoiceAssistantError as e:
        print(f"Voice assistant error: {e}")


if __name__ == "__main__":
    main()
