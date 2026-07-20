# End-to-End AI Capstone

A modular AI system that combines three components built across earlier internship projects:

1. **Face authentication** (from the Face Detection & Recognition project) — verifies who's using the system before granting access.
2. **Voice assistant** (speech-to-text + text-to-speech) — listens for spoken commands and responds aloud.
3. **Command executor** — a rule-based mapping from recognized commands to real actions (check the time, search the web, open a website/app).

The flow is simple: **authenticate with your face → speak a command → the assistant acts on it and replies** — looping until you say "exit."

## Tech Stack

- **Python 3**
- **OpenCV** + **face_recognition** (dlib) — face authentication
- **SpeechRecognition** (Google Speech API) — speech-to-text
- **pyttsx3** — offline text-to-speech
- **webbrowser** / **subprocess** — command execution

## Project Structure

```
ai-capstone/
├── auth/
│   └── face_auth.py         # webcam-based identity verification
├── assistant/
│   ├── voice_assistant.py   # speech-to-text (listen) + text-to-speech (speak)
│   └── command_executor.py  # rule-based command -> action mapping
├── main.py                  # orchestrates the full flow
├── requirements.txt
└── .gitignore
```

This modular design means each piece (auth, listening, speaking, command logic) can be tested and reused independently — e.g. `face_auth.py` and `encodings.pickle` are reused directly from the earlier face-recognition project with no changes needed.

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/ai-capstone.git
cd ai-capstone

python -m venv venv
source venv/Scripts/activate    # Windows (Git Bash)
# or: venv\Scripts\activate     # Windows (cmd)
# or: source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

> **Windows note on `pyaudio`:** if `pip install pyaudio` fails to build, install a precompiled wheel instead:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### Bring your face data over
Copy `encodings.pickle` from your earlier face-recognition project into this project's root folder. (If you don't have one yet, go to that project, run `register_faces.py` then `encode_faces.py`, and copy the resulting file here.)

## How to Run

```bash
python main.py
```

1. A webcam window opens — look at the camera. If your face matches a known encoding within 10 seconds, you're authenticated (3 attempts allowed).
2. Once authenticated, the assistant greets you by name and starts listening.
3. Speak a command (see sample list below). It executes the action and replies out loud.
4. Say **"exit"**, **"quit"**, or **"stop"** to end the session.

## Sample Commands

- "What's the time"
- "Search for python tutorials"
- "Open YouTube" / "Open Google" / "Open GitHub" / "Open Gmail"
- "Open notepad" / "Open calculator"
- "Exit" / "Quit" / "Stop"

## Error Handling

- **No face matched in time** → up to 3 authentication attempts before the program exits.
- **Encodings file missing** → clear error message pointing to the earlier project's registration steps.
- **Microphone not available / no speech detected** → the assistant says so and re-prompts, rather than crashing.
- **Unrecognized command** → the assistant explains it doesn't have that action mapped and suggests trying a sample command.

## Reusing / Extending

- Add new commands by extending `command_executor.py`'s `execute_command()` — no changes needed elsewhere.
- Add new authorized users the same way as the original project: `register_faces.py` + `encode_faces.py` from the face-recognition repo, then copy the updated `encodings.pickle` here.
- Swap `pyttsx3` for `gTTS` if you'd prefer online, more natural-sounding voices (trade-off: requires internet + audio playback setup).