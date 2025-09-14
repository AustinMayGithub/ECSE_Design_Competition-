
        t1 = threading.Thread(target=face_tracking)
        t2 = threading.Thread(target=speech_recognition_loop)
        t1.start()