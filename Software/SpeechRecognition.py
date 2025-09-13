# # import os
# # import torch
# # # needs TTS installed
# # # pip install TTS
# # from TTS.api import TTS

# # import speech_recognition as sr

# # # Get device
# # device = "cuda" if torch.cuda.is_available() else "cpu"

# # # Create a recognizer object
# # r = sr.Recognizer()

# # print(TTS().list_models())

# # # Init TTS
# # tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=(device=="cuda"))


# # # Use the microphone as the audio source
# # with sr.Microphone() as source:
# #     print("Say something!")
# #     audio = r.listen(source)

# # try:
# #     # Use Google Speech Recognition to convert audio to text
# #     text = r.recognize_google(audio)
# # except sr.UnknownValueError:
# #     print("Google Speech Recognition could not understand audio")
# # except sr.RequestError as e:
# #     print("Could not request results from Google Speech Recognition service; {0}".format(e))

# # # make tts from recognized text
# # output_path = "output.wav"
# # tts.tts_to_file(text=text, file_path=output_path)
# # # play the output file
# # os.system(f"aplay {output_path}") # doesn't work probably need something else installed
# # print(f"Recognized text: {text}")
# # print(f"Audio saved to {output_path}")



# import os
# import sys
# import platform
# import torch
# from TTS.api import TTS
# import speech_recognition as sr

# # ---------- Config ----------
# TRIGGER_WORDS = {"computer", "assistant", "buddy"}     # <- edit to your wake/trigger words
# REPLY_TEXT = "Hi! I heard the trigger. How can I help?" # simple synthesized reply
# TTS_MODEL = "tts_models/en/ljspeech/tacotron2-DDC"      # Coqui TTS model
# # ----------------------------

# device = "cuda" if torch.cuda.is_available() else "cpu"
# tts = TTS(model_name=TTS_MODEL, progress_bar=False, gpu=(device == "cuda"))

# r = sr.Recognizer()

# def play(path: str):
#     """Cross-platform audio playback for a WAV file."""
#     system = platform.system()
#     if system == "Darwin":       # macOS
#         os.system(f"afplay '{path}'")
#     elif system == "Linux":
#         # 'aplay' is common; fall back to python alt if missing
#         rc = os.system(f"aplay '{path}'")
#         if rc != 0:
#             try:
#                 from pydub import AudioSegment
#                 from pydub.playback import play as pplay
#                 pplay(AudioSegment.from_wav(path))
#             except Exception:
#                 print("Install pydub & simpleaudio for fallback playback: pip install pydub simpleaudio")
#     elif system == "Windows":
#         os.system(f'start /min wmplayer "{path}"')  # simple fallback
#     else:
#         print("Unknown OS; install pydub+simpleaudio for playback.")

# def contains_trigger(text: str) -> bool:
#     lower = text.lower()
#     return any(tw in lower.split() or tw in lower for tw in TRIGGER_WORDS)

# def speak(text: str, outfile="output.wav"):
#     tts.tts_to_file(text=text, file_path=outfile)
#     play(outfile)

# def main():
#     with sr.Microphone() as source:
#         print("Listening… (ctrl+C to stop)")
#         r.adjust_for_ambient_noise(source, duration=0.5)
#         audio = r.listen(source)

#     try:
#         text = r.recognize_google(audio)  # requires internet
#         print(f"Recognized: {text}")
#     except sr.UnknownValueError:
#         print("Didn't catch that.")
#         return
#     except sr.RequestError as e:
#         print(f"Speech service error: {e}")
#         return

#     if contains_trigger(text):
#         speak(REPLY_TEXT, "reply.wav")
#     else:
#         # pass-through: “repeat back” the heard text
#         speak(text, "echo.wav")

# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         sys.exit(0)



import os
import sys
import platform
import pyttsx3
import speech_recognition as sr

TRIGGER_WORDS = {"computer", "assistant", "buddy"}
REPLY_TEXT = "Hi! I heard the trigger. How can I help?"

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

if name == "main":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
