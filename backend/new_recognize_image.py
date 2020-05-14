# import the necessary packages
from scipy.spatial import distance as dist
# from imutils.video import VideoStream
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

from glob import glob

FOLDER_RAW = './pictures/raw'
FOLDER_DONE = './pictures/done'

EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 3


# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open("./encodings.pickle", "rb").read())
detector = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')

# face_detector = dlib.get_frontal_face_detector()
face_predictor = dlib.shape_predictor('./models/shape_predictor_68_face_landmarks.dat')

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear



def recognize_face(fn):
    image_name = fn.split("\\")[-1]
    if(image_name == fn):
        image_name = fn.split("/")[-1]

    print ('picture:',image_name)
    frame = cv2.imread(fn)


    # convert the input frame from (1) BGR to grayscale (for face
    # detection) and (2) from BGR to RGB (for face recognition)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    # detect faces in the grayscale frame
    rects = detector.detectMultiScale(gray, scaleFactor=1.1,
        minNeighbors=5, minSize=(30, 30))


    # OpenCV returns bounding box coordinates in (x, y, w, h) order
    # but we need them in (top, right, bottom, left) order, so we
    # need to do a bit of reordering
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    # compute the facial embeddings for each face bounding box
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
            encoding, 0.35)
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
            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
            name = max(counts, key=counts.get)

        # update the list of names
        names.append(name)

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):

        cv2.rectangle(frame, (left, top), (right, bottom),
            (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.75, (0, 255, 0), 2)

        print ('recognize_name:', name)

    # move file that done from raw to done
    cv2.imwrite(FOLDER_DONE + '/'+ image_name + '' + str(names) + '.jpg',frame)

    if os.path.exists(fn):
        print ('removed ' + fn)
        os.remove(fn)


def handle():
    for fn in glob(FOLDER_RAW + '/*.*'):
        recognize_face (fn)


handle()