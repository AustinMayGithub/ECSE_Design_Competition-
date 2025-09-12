import cv2
import serial
import math

# Connect to Pico
ser = serial.Serial('COM15', 115200)  # Change COM15 to your port

# Open camera
cap = cv2.VideoCapture(1)

# Face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
command = "Stop"


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Mirror image
    
    # Find faces
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(faces) > 0:
        # Person found - send face position
        x, y, w, h = faces[0]
        face_center_x = x + w // 2
        face_center_x = ((face_center_x / 180))
        if face_center_x > 1.9 :
            if command != "Left":
                print("Left")
                command = "Left"
                ser.write("L\n".encode())
            
        elif face_center_x < 1.5:
            if command != "Right":
                print("Right")
                command = "Right"
                ser.write("R\n".encode())
        else :
            if command != "Stop":
                print("Stop")
                command = "Stop"
                ser.write("S\n".encode())
        
        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    else:
        # No person - stop servo
        ser.write("STOP\n".encode())
    
    # Show camera
    cv2.imshow("Face Tracking", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()