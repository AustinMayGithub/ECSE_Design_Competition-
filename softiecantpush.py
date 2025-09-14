# import os
# import sys
# import platform
# import pyttsx3
# import speech_recognition as sr
# import random

# # ---------- Config ----------
# # Define your trigger words and their responses
# TRIGGER_RESPONSES = {
#     "computer": [
#         "Yes, I'm listening. How can I assist you?",
#         "Computer here. What do you need?",
#         "I'm ready to help!"
#     ],
#     "assistant": [
#         "Your assistant is here. What can I do for you?",
#         "How may I assist you today?",
#         "Assistant activated. How can I help?"
#     ],
#     "buddy": [
#         "Hey buddy! What's up?",
#         "Your buddy is here! How can I help?",
#         "Hey there, friend!"
#     ],
#     "hello": [
#         "Hello! Nice to hear from you!",
#         "Hi there! How are you doing?",
#         "Hello! What can I do for you?"
#     ],
#     "weather": [
#         "I'd love to help with weather, but I don't have access to weather data right now.",
#         "For weather information, you might want to check your weather app."
#     ],
#     "time": [
#         "I don't have access to the current time, but you can check your device's clock.",
#         "Time flies! Check your system clock for the current time."
#     ],
#     "joke": [
#         "Why don't scientists trust atoms? Because they make up everything!",
#         "I told my computer a joke about UDP... but I'm not sure if it got it.",
#         "Why do programmers prefer dark mode? Because light attracts bugs!"
#     ]
# }

# # Set to True if you want random responses, False for cycling through responses
# USE_RANDOM_RESPONSES = True
# # ---------------------------- 

# r = sr.Recognizer()
# response_counters = {word: 0 for word in TRIGGER_RESPONSES.keys()}

# def play(path: str):
#     system = platform.system()
#     if system == "Darwin":
#         os.system(f"afplay '{path}'")
#     elif system == "Linux":
#         os.system(f"aplay '{path}'")
#     elif system == "Windows":
#         os.system(f'start "" "{path}"')
#     else:
#         print("Unknown OS; can't play audio.")

# def find_trigger_and_respond(text: str) -> tuple[str, str] or None:
#     """
#     Find trigger word in text and return (trigger_word, response).
#     Returns None if no trigger found.
#     """
#     lower_text = text.lower()
#     words_in_text = lower_text.split()
    
#     # Check each trigger word
#     for trigger_word in TRIGGER_RESPONSES.keys():
#         # Check if trigger word appears as a whole word or as part of text
#         if trigger_word in words_in_text or trigger_word in lower_text:
#             responses = TRIGGER_RESPONSES[trigger_word]
            
#             if USE_RANDOM_RESPONSES:
#                 response = random.choice(responses)
#             else:
#                 # Cycle through responses
#                 counter = response_counters[trigger_word]
#                 response = responses[counter % len(responses)]
#                 response_counters[trigger_word] += 1
            
#             return trigger_word, response
    
#     return None

# def speak(text: str, outfile="output.wav"):
#     engine = pyttsx3.init()
#     engine.save_to_file(text, outfile)
#     engine.runAndWait()
#     play(outfile)

# def print_available_triggers():
#     print("\nAvailable trigger words:")
#     for trigger in TRIGGER_RESPONSES.keys():
#         print(f"  • {trigger}")
#     print()

# def main():
#     print("🎤 Customizable Voice Assistant Started!")
#     print_available_triggers()
#     print("Say any trigger word to get a response. Press Ctrl+C to stop.\n")
    
#     while True:
#         with sr.Microphone() as source:
#             print("Listening... 👂")
#             r.adjust_for_ambient_noise(source, duration=0.5)
#             audio = r.listen(source)

#         try:
#             text = r.recognize_google(audio)
#             print(f"📝 Recognized: '{text}'")
            
#             # Check for trigger words and get response
#             result = find_trigger_and_respond(text)
            
#             if result:
#                 trigger_word, response = result
#                 print(f"🎯 Trigger '{trigger_word}' detected!")
#                 print(f"🤖 Response: {response}")
#                 speak(response, f"{trigger_word}_response.wav")
#             else:
#                 print("🔁 No trigger word detected. Echoing back...")
#                 print(f"🤖 Echo: {text}")
#                 speak(text, "echo.wav")
                
#         except sr.UnknownValueError:
#             print("🔇 Didn't catch that. Please try again.")
#             continue
#         except sr.RequestError as e:
#             print(f"❌ Speech service error: {e}")
#             continue
        
#         print("-" * 50)  # Visual separator

# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("\n⚡ Pikachu is shutting down. Pika pika! ⚡")
#         sys.exit(0)

import os
import sys
import platform
import pyttsx3
import speech_recognition as sr
import random

# ---------- Config ----------
# Define your trigger words and their responses
TRIGGER_RESPONSES = {
    "job": [
        "dont ever say the j word infront of me ever again",

    ],
    "employment": [
        "Sorry what does e-e-employment mean, could you please tell me"
    ],
    "buddy": [
        "never call me buddy again bozo",
        ""
    ],
    "pika": [
        "peeka peeka . . . achoo"
    ],
    "weather": [
        "I'd love to help with weather, but I don't have access to weather data right now.",
        "For weather information, you might want to check your weather app."
    ],
    "time": [
        "I don't have access to the current time, but you can check your device's clock.",
        "Time flies! Check your system clock for the current time."
    ],
    "joke": [
        "Why don't scientists trust atoms? Because they make up everything!",
        "I told my computer a joke about UDP... but I'm not sure if it got it.",
        "Why do programmers prefer dark mode? Because light attracts bugs!"
    ]
}

# Set to True if you want random responses, False for cycling through responses
USE_RANDOM_RESPONSES = True
# ---------------------------- 

r = sr.Recognizer()
response_counters = {word: 0 for word in TRIGGER_RESPONSES.keys()}

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

def find_trigger_and_respond(text: str) -> tuple[str, str] or None:
    """
    Find trigger word in text and return (trigger_word, response).
    Returns None if no trigger found.
    """
    lower_text = text.lower()
    words_in_text = lower_text.split()
    
    # Check each trigger word
    for trigger_word in TRIGGER_RESPONSES.keys():
        # Check if trigger word appears as a whole word or as part of text
        if trigger_word in words_in_text or trigger_word in lower_text:
            responses = TRIGGER_RESPONSES[trigger_word]
            
            if USE_RANDOM_RESPONSES:
                response = random.choice(responses)
            else:
                # Cycle through responses
                counter = response_counters[trigger_word]
                response = responses[counter % len(responses)]
                response_counters[trigger_word] += 1
            
            return trigger_word, response
    
    return None

def speak(text: str, outfile="output.wav"):
    engine = pyttsx3.init()
    engine.save_to_file(text, outfile)
    engine.runAndWait()
    play(outfile)

def print_available_triggers():
    print("\nAvailable trigger words:")
    for trigger in TRIGGER_RESPONSES.keys():
        print(f"  • {trigger}")
    print()

def main():
    print("🎤 Customizable Voice Assistant Started!")
    print_available_triggers()
    print("Say any trigger word to get a response. Press Ctrl+C to stop.\n")
    
    while True:
        with sr.Microphone() as source:
            print("Listening... 👂")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print(f"📝 Recognized: '{text}'")
            
            # Check for trigger words and get response
            result = find_trigger_and_respond(text)
            
            if result:
                trigger_word, response = result
                print(f"🎯 Trigger '{trigger_word}' detected!")
                print(f"🤖 Response: {response}")
                speak(response, f"{trigger_word}_response.wav")
            else:
                print("🔁 No trigger word detected. Echoing back...")
                print(f"🤖 Echo: {text}")
                speak(text, "echo.wav")
                
        except sr.UnknownValueError:
            print("🔇 Didn't catch that. Please try again.")
            continue
        except sr.RequestError as e:
            print(f"❌ Speech service error: {e}")
            continue
        
        print("-" * 50)  # Visual separator

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚡ Pikachu is shutting down. Pika pika! ⚡")
        sys.exit(0)