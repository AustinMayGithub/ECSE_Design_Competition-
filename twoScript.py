import cv2
import serial
import threading
import os
import sys
import platform
import pyttsx3
import speech_recognition as sr
import random

# ---------- Config ----------
TRIGGER_RESPONSES = {
    "job": [
        "dont ever say the j word infront of me ever again",
        "Please not the forbidden j word , i need a job pleeeeease pleeeeease pleeeease "
    ],
    "employment": [
        "Sorry what does eh-eh-ployment mean, could you please tell me"
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
        "do i look like a watch to you",
        "Time flies! Check your system clock for the current time."
    ],
    "joke": [
        "Why don't scientists trust atoms? Because they make up everything!",
        "I told my computer a joke about UDP... but I'm not sure if it got it.",
        "Why do programmers prefer dark mode? Because light attracts bugs!"
    ],
    "teacher": [
        "im dooleaping it, im dooleaping it, im dooleaping it, "
    ]
}
USE_RANDOM_RESPONSES = True
stop_threads = False
# ----------------------------

# Serial setup
ser = serial.Serial('COM15', 115200)  # Change COM15 to your port

# Face detection setup
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
command = "Stop"

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

def find_trigger_and_respond(text: str):
    lower_text = text.lower()
    words_in_text = lower_text.split()
    for trigger_word in TRIGGER_RESPONSES.keys():
        if trigger_word in words_in_text or trigger_word in lower_text:
            responses = TRIGGER_RESPONSES[trigger_word]
            if USE_RANDOM_RESPONSES:
                response = random.choice(responses)
            else:
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

def face_tracking():
    global command, stop_threads
    while not stop_threads:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_center_x = x + w // 2
            face_center_x = ((face_center_x / 180))
            if face_center_x > 1.9:
                if command != "Left":
                    print("Left")
                    command = "Left"
                    ser.write("L\n".encode())
            elif face_center_x < 1.5:
                if command != "Right":
                    print("Right")
                    command = "Right"
                    ser.write("R\n".encode())
            else:
                if command != "Stop":
                    print("Stop")
                    command = "Stop"
                    ser.write("S\n".encode())
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            ser.write("STOP\n".encode())
        cv2.imshow("Face Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_threads = True
            break
    cap.release()
    cv2.destroyAllWindows()
    ser.close()

def speech_recognition_loop():
    global stop_threads
    print("\nAvailable trigger words:")
    for trigger in TRIGGER_RESPONSES.keys():
        print(f"  • {trigger}")
    print("\nSay any trigger word to get a response. Press Ctrl+C to stop.\n")
    while not stop_threads:
        with sr.Microphone() as source:
            print("Listening... 👂")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"📝 Recognized: '{text}'")
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
        print("-" * 50)

if __name__ == "__main__":
    try:
        t1 = threading.Thread(target=face_tracking)
        t2 = threading.Thread(target=speech_recognition_loop)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        stop_threads = True
        sys.exit(0)



