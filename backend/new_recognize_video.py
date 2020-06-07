# -*- coding: utf-8 -*-
# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import VideoStream
# from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import dlib
from imutils import face_utils
# import serial
import datetime
import os
import base64
import uuid
import time

EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 3

FOLDER_OUTPUT = './output'
SAVE_TIME = 5
# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open("./encodings.pickle", "rb").read())
detector = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str,
	help="path to output video")
args = vars(ap.parse_args())
# face_detector = dlib.get_frontal_face_detector()
# face_predictor = dlib.shape_predictor('./models/shape_predictor_68_face_landmarks.dat')

# # grab the indexes of the facial landmarks for the left and
# # right eye, respectively
# (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
# (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# def eye_aspect_ratio(eye):
#     # compute the euclidean distances between the two sets of
#     # vertical eye landmarks (x, y)-coordinates
#     A = dist.euclidean(eye[1], eye[5])
#     B = dist.euclidean(eye[2], eye[4])

#     # compute the euclidean distance between the horizontal
#     # eye landmark (x, y)-coordinates
#     C = dist.euclidean(eye[0], eye[3])

#     # compute the eye aspect ratio
#     ear = (A + B) / (2.0 * C)

#     # return the eye aspect ratio
#     return ear

known_face_encodings = []
known_face_metadata = []

def save_known_faces():
    with open("encodings.pickle", "wb") as face_data_file:
        face_data = [known_face_encodings, known_face_metadata]
        pickle.dump(face_data, face_data_file)
        print("Known faces backed up to disk.")


def load_known_faces():
    global known_face_encodings, known_face_metadata

    try:
        with open("encodings.pickle", "rb") as face_data_file:
            known_face_encodings, known_face_metadata = pickle.load(face_data_file)
            print("Known faces loaded from disk.")
    except FileNotFoundError as e:
        print("No previous face data found - starting with a blank known face list.")
        pass

def register_new_face(face_encoding, face_image):
    """
    Add a new person to our list of known faces
    """
    # Add the face encoding to the list of known faces
    known_face_encodings.append(face_encoding)
    # Add a matching dictionary entry to our metadata list.
    # We can use this to keep track of how many times a person has visited, when we last saw them, etc.
    known_face_metadata.append({
        "first_seen": datetime.now(),
        "first_seen_this_interaction": datetime.now(),
        "last_seen": datetime.now(),
        "seen_count": 1,
        "seen_frames": 1,
        "face_image": face_image,
        "send_data": False,
        "name": "Unknown"
    })



# vs = VideoStream(src='http://admin:admin@192.168.0.105/videostream.cgi?user=admin&pwd=admin&resolution=32&rate=0').start()
vs = VideoStream(0).start()

def recognize_face():
    writer = None
    while True:
        frame = vs.read()
        # convert the input frame from (1) BGR to grayscale (for face
        # detection) and (2) from BGR to RGB (for face recognition)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        r = frame.shape[1] / float(rgb.shape[1])

        # detect faces in the grayscale frame
        rects = detector.detectMultiScale(gray, scaleFactor=1.1,
            minNeighbors=5, minSize=(30, 30))


        # OpenCV returns bounding box coordinates in (x, y, w, h) order
        # but we need them in (top, right, bottom, left) order, so we
        # need to do a bit of reordering
        boxesFace = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(rgb, boxesFace)
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],
                encoding, 0.6)
            name = "Unknown"
            
            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                    # print(name + " has been here!")
                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)
            else: 
                print("Unknown has been here!")
            # update the list of names
            names.append(name)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxesFace, names):

            top = int(top * r)
            right = int(right * r)
            bottom = int(bottom * r)
            left = int(left * r)

            # draw the predicted face name on the image
            cv2.rectangle(frame, (left, top), (right, bottom),
                (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, (0, 255, 0), 2)
            
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    vs.stop()    

def handle():
    recognize_face()


handle()