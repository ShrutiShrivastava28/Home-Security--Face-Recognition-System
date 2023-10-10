import numpy as np
import pickle
import os
import cv2
import time
import datetime
import imutils
import pymongo
from pymongo import MongoClient
import base64
import tkinter as tk
from tkinter import messagebox
import subprocess

def recognize_face():
    curr_path = os.getcwd()

    # Connect to the MongoDB database
    client = MongoClient("mongodb://localhost:27017/")
    db = client["FaceRecognition"]
    collection = db["image"]

    print("Loading face detection model")
    proto_path = os.path.join(curr_path, 'model', 'deploy.prototxt')
    model_path = os.path.join(curr_path, 'model', 'res10_300x300_ssd_iter_140000.caffemodel')
    face_detector = cv2.dnn.readNetFromCaffe(prototxt=proto_path, caffeModel=model_path)

    print("Loading face recognition model")
    recognition_model = os.path.join(curr_path, 'model', 'openface_nn4.small2.v1.t7')
    face_recognizer = cv2.dnn.readNetFromTorch(model=recognition_model)

    recognizer = pickle.loads(open('recognizer.pickle', "rb").read())
    le = pickle.loads(open('le.pickle', "rb").read())

    print("Starting test video file")
    vs = cv2.VideoCapture(0)
    time.sleep(1)

    count = {}
    capture_count = 0

    # Create a Tkinter window
    root = tk.Tk()
    root.withdraw()

    while True:
        ret, frame = vs.read()
        frame = imutils.resize(frame, width=600)

        (h, w) = frame.shape[:2]

        image_blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0), False, False)

        face_detector.setInput(image_blob)
        face_detections = face_detector.forward()

        face_detected = False  # flag to check if any faces are detected
        num_faces = 0  # counter for number of faces detected in the frame

        for i in range(0, face_detections.shape[2]):
            confidence = face_detections[0, 0, i, 2]

            if confidence >= 0.5:
                num_faces += 1
                if num_faces > 1:
                    capture = False
                    tk.messagebox.showwarning("Multiple faces detected", "Please ensure only one person is in the frame")
                    break  # exit loop if more than one face is detected

                box = face_detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                face = frame[startY:endY, startX:endX]

                (fH, fW) = face.shape[:2]

                face_blob = cv2.dnn.blobFromImage(face, 1.0/255, (96, 96), (0, 0, 0), True, False)

                face_recognizer.setInput(face_blob)
                vec = face_recognizer.forward()

                preds = recognizer.predict_proba(vec)[0]
                j = np.argmax(preds)
                proba = preds[j]
                name = le.classes_[j]

                if name not in count:
                    count[name] = 0

                if count[name] < 5:
                    count[name] += 1

                if name not in count:
                    count[name] = 0

                if count[name] < 5:
                    count[name] += 1

                if cv2.waitKey(1) & 0xFF == ord('r'):  # check for 'r' key press
                    cv2.imwrite('face_{}.jpg'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S%f')), frame)

                    if len(face_detections) > 1:
                        tk.messagebox.showwarning("Multiple faces detected",
                                                  "Please ensure only one person is in the frame")
                    elif len(face_detections) == 0:
                        tk.messagebox.showwarning("No face detected", "Please ensure a person is in the frame")
                    else:
                        # Convert image to JPEG format and encode it in base64
                        ret, jpeg = cv2.imencode('.jpg', face)
                        jpeg_base64 = base64.b64encode(jpeg).decode('utf-8')

                        face_data = {
                            "image": jpeg_base64,
                            "timestamp": datetime.datetime.now(),
                            "person": name,
                            "confidence": str(proba)
                        }

                        # Insert the face data into the MongoDB database
                        result = collection.insert_one(face_data)

                        print("Face data inserted with ID:", result.inserted_id)
                        # Show a message box with the image capture confirmation
                        messagebox.showinfo("Image Captured", "Image has been captured.")

                text = "{}: {:.2f}".format(name, proba * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)

                face_detected = True

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(10) & 0xFF

        if key == ord('a'):
            break

        if not face_detected:
            break

    # Release the video capture and close the window
    vs.release()
    cv2.destroyAllWindows()

recognize_face()

