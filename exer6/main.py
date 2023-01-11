'''
Mateusz Miekicki s20691
Oskar Przydatek s19388
If you close your eyes while watching the ad, the ad stops, when you open it it starts playing.
'''

import numpy as np
import cv2
import vlc
import time

curr_time = round(time.time()*1000)

cap = cv2.VideoCapture(0)
#loading of haar-cascade XML file
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_eye.xml')
media = vlc.MediaPlayer("ad.mp4")

while True:
    #capture webcam image
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #detection of face border coordinate
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        media.set_pause(1)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
        roi_gray = gray[y:y+w, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        #if a face is detected, the next step is to detect the position of the eyes
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
        #if we detect an eye, we can start to play a commercial
        if len(eyes) != 0:
            media.play()
            curr_time = round(time.time()*1000)
        else:
            #if not, the advertisement will be stopped
            #additionally take a time delta, for blinking or simply imperfect detection
            if curr_time - round(time.time()*1000) < 500:
                media.set_pause(1)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey),
                          (ex + ew, ey + eh), (0, 255, 0), 5)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()