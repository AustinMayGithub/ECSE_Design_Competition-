import cv2
import serial
import threading
import time
import os
import sys
import platform
import pyttsx3
import speech_recognition as sr
# from playsound import playsound

# ---------- Config ----------
TRIGGER_WORDS = {"computer", "assistant", "buddy"}
REPLY_TEXT = "Hi! I heard the trigger. How can I help?"
# ----------------------------

# Serial setup
ser = serial.Serial('COM15', 115200)  # Change COM15 to your port

# Face detection setup
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
command = "Stop"
stop_threads = False

def play(path: str):
    system = platform.system()
    if system == "Darwin":
        os.system(f"afplay '{path}'")
    elif system == "Linux":
        os.system(f"aplay '{path}'")
    elif system == "Windows":
        os.system(f'start /min wmplayer "{path}"')
    else:
        print("Unknown OS; can't play audio.")

def contains_trigger(text: str) -> bool:
    lower = text.lower()
    return any(tw in lower.split() or tw in lower for tw in TRIGGER_WORDS)

def speak(text: str, outfile="spoken.wav"):
    engine = pyttsx3.init()
    # engine.save_to_file(text, outfile)
    engine.say(text)
    engine.runAndWait()
    # play(outfile)

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
    r = sr.Recognizer()
    while not stop_threads:
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
            speak(text, "reply.wav")

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



