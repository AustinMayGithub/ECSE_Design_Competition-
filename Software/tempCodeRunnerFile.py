import os
import sys
import platform
import pyttsx3
import speech_recognition as sr

# ---------- Config ----------
TRIGGER_WORDS = {"computer", "assistant", "buddy"}
REPLY_TEXT = "Hi! I heard the trigger. How can I help?"
# ---------------------------- 

r = sr.Recognizer() 

def play(path: str):
    system = platform.system()
    if system == "Darwin":
        os.system(f"afplay '{path}'")
    elif system == "Linux":
        os.system(f"aplay '{path}'")
    elif system == "Windows":
        os.system(f'start "" "{path}"')
    else:
        print("Unknown OS; can't play audio.")

def contains_trigger(text: str) -> bool:
    lower = text.lower()
    return any(tw in lower.split() or tw in lower for tw in TRIGGER_WORDS)

def speak(text: str, outfile="output.wav"):
    engine = pyttsx3.init()
    engine.save_to_file(text, outfile)
    engine.runAndWait()
    play(outfile)

def main():
    while True:
        with sr.Microphone() as source:
            print("Listening… (ctrl+C to stop)")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print(f"Recognized: {text}")
        except sr.UnknownValueError:
            print("Didn't catch that.")
            continue
        except sr.RequestError as e:
            print(f"Speech service error: {e}")
            continue

        # Respond with the word just said
        speak(text, "echo.wav")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)

