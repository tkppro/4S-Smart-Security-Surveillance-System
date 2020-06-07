from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
from datetime import datetime, timedelta


imagePaths = list(paths.list_images('dataset'))
known_face_encodings = []
known_face_metadata = []

def encodingFace(): 
    for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
        print("[INFO] processing image {}/{}".format(i + 1,
            len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]

        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb,
            model="hog")

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            known_face_encodings.append(encoding)
            # Add a matching dictionary entry to our metadata list.
            # We can use this to keep track of how many times a person has visited, when we last saw them, etc.
            known_face_metadata.append({
                "first_seen": datetime.now(),
                "first_seen_this_interaction": datetime.now(),
                "last_seen": datetime.now(),
                "seen_count": 1,
                "seen_frames": 1,
                "face_image": '',
                "send_data": False,
                "name": name
            })

def save_known_faces():
    with open("encodings.pickle", "wb") as face_data_file:
        face_data = [known_face_encodings, known_face_metadata]
        pickle.dump(face_data, face_data_file)
        print("Known faces backed up to disk.")

encodingFace()
save_known_faces()