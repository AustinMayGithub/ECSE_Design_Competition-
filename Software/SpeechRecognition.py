import os
import torch
# needs TTS installed
# pip install TTS
from TTS.api import TTS

import speech_recognition as sr

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Create a recognizer object
r = sr.Recognizer()

print(TTS().list_models())

# Init TTS
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=(device=="cuda"))


# Use the microphone as the audio source
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

try:
    # Use Google Speech Recognition to convert audio to text
    text = r.recognize_google(audio)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

# make tts from recognized text
output_path = "output.wav"
tts.tts_to_file(text=text, file_path=output_path)
# play the output file
os.system(f"aplay {output_path}") # doesn't work probably need something else installed
print(f"Recognized text: {text}")
print(f"Audio saved to {output_path}")