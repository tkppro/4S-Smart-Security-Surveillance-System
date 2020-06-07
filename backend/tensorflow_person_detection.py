# Code adapted from Tensorflow Object Detection Framework
# https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb
# Tensorflow Object Detection Detector

import numpy as np
import tensorflow as tf
import cv2
import time
import sort
import pickle
import face_recognition
import imutils
import dlib
from imutils import face_utils
import threading
from datetime import datetime, timedelta
import uuid
import json 
from imgur import uploadImage
from firebase import uploadRecord

FOLDER_OUTPUT = './pictures/raw'
FOLDER_JSON_RAW = './data_json/raw/'

class DetectorAPI:
    def __init__(self, path_to_ckpt):
        self.path_to_ckpt = path_to_ckpt

        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.default_graph = self.detection_graph.as_default()
        self.sess = tf.Session(graph=self.detection_graph)

        # Definite input and output Tensors for detection_graph
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

    def processFrame(self, image):
        # Expand dimensions since the trained_model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image, axis=0)
        # Actual detection.
        start_time = time.time()
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})
        end_time = time.time()

        # print("Elapsed Time:", end_time-start_time)

        im_height, im_width,_ = image.shape
        boxes_list = [None for i in range(boxes.shape[1])]
        for i in range(boxes.shape[1]):
            boxes_list[i] = (int(boxes[0,i,0] * im_height),
                        int(boxes[0,i,1]*im_width),
                        int(boxes[0,i,2] * im_height),
                        int(boxes[0,i,3]*im_width))

        return boxes_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])

    def close(self):
        self.sess.close()
        self.default_graph.close()

def faceRecognition(frame):
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    r = frame.shape[1] / float(rgb.shape[1])
    
    # detect faces in the grayscale frame
    rects = detector.detectMultiScale(gray, scaleFactor=1.1,
        minNeighbors=5, minSize=(30, 30))

    countName = 0
    boxesFace = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    # compute the facial embeddings for each face bounding box
    encodings = face_recognition.face_encodings(rgb, boxesFace)
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(dataSaved["encodings"],
            encoding, 0.4)
        # start_time = time.time()
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
                name = dataSaved["names"][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)
            print(name + ' has been here!')
        
        else: 
            countName += 1
            savingName = f"{name} {countName}"
            dataSaved['encodings'].append(encoding)
            dataSaved['names'].append(savingName)
            print(name + " has been here! <3")
            
            
        # update the list of names
        names.append(name)

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxesFace, names):

        top = int(top * r)
        right = int(right * r)
        bottom = int(bottom * r)
        left = int(left * r)

        # draw the predicted face name on the image
        # cv2.rectangle(frame, (left, top), (right, bottom),
        #     (0, 255, 0), 2)
        # y = top - 15 if top - 15 > 15 else top + 15
        # cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
        #     0.75, (0, 255, 0), 2)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), 
            (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, name, 
            (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)


if __name__ == "__main__":
    
    model_path = 'models/ssd_mobilenet_v1_coco_2017_11_17/frozen_inference_graph.pb'
    odapi = DetectorAPI(path_to_ckpt=model_path)
    threshold = 0.3
    # dataSaved = pickle.loads(open("./encodings.pickle", "rb").read())
    # detector = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
    known_metadata = []
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture('test/Safety_Full_Hat_and_Vest.mp4')
    tracker = sort.Sort()
    fps = int(cap.get(cv2.CAP_PROP_FPS))
       

    while True:
        r, frame = cap.read()
        # frame = cv2.resize(frame, (1280, 720))
        dets = []
        t1 = time.time()
        
        boxes, scores, classes, num = odapi.processFrame(frame)

        # Visualization of the results of a detection.
        for i in range(len(boxes)):
            # Class 1 represents human
            if classes[i] == 1 and scores[i] > threshold:
                box = boxes[i]
                # cv2.rectangle(frame,(box[1],box[0]),(box[3],box[2]),(255,0,0),2)
                dets.append(np.array([box[1], box[0], box[3], box[2], scores[i]]))
                
                

        dataTrack = tracker.update(np.array(dets))
        for data in dataTrack:
            (start_x, start_y, end_x, end_y) = (int(data[0]), int(data[1]), int(data[2]), int(data[3]))
            trackingID = int(data[4])
            label = ''
            cv2.putText(frame, "{}".format(trackingID), (int((start_x + end_x)/2),int((start_y  + 50))), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 4)   
            
            # check trackID in known_metadata. If trackingID does not exist, append new into known_metadata
            item =  next((item for item in known_metadata if item["id"] == trackingID), False)
            if item is not False: 
                time_at_door = datetime.now() - item['first_seen_time']

                trackID = item['id']
                visibleTime = f"{trackID}-{int(time_at_door.total_seconds())}s"
                label = visibleTime
                print(visibleTime)
                
                if time_at_door > timedelta(seconds=3) and item['saved_image'] is False:
                    imageId = uuid.uuid1()
                    imageName = imageId.hex + '.jpg'
                    cv2.imwrite(FOLDER_OUTPUT + '/' + imageName,frame)
                    print("Saved face with image's name: ", imageName)  
                    item['image_name'] = imageName
                    item['saved_image'] = True

                if time_at_door > timedelta(seconds=15) and item['send_data'] is False:
                    print('Update visible time on firebase with image.....', item['image_name'])
                    name = f"Unknown - {item['id']}"

                    imageUploadedUrl = FOLDER_OUTPUT + '/' + item['image_name']
                    imageResponseUrl = uploadImage(imageUploadedUrl, name)
                    detectedAt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    visibleTime = timedelta(seconds=15).total_seconds()
                    
                    objectPushData = {
                        'name':  name,
                        'image': imageResponseUrl,
                        # 'image': item['image_name'],
                        'detectedAt': str(detectedAt),
                        'visibleTime': str(visibleTime)
                    }
                    item['send_data'] = True
                    
                    with open(FOLDER_JSON_RAW + item['image_name'] + '.json', 'w') as outfile:
                        json.dump(objectPushData, outfile)


            else: 
                known_metadata.append({
                    'id': trackingID,
                    'first_seen_time': datetime.now(),
                    'send_data': False,
                    # 'image_name': imageName,
                    'saved_image': False,
                })
                newNumb = f"register new number: {trackingID}"
                print(newNumb)        

            # cv2.rectangle(frame, (start_x,start_y), (end_x,end_y),(0,255,0),2)
            # cv2.putText(frame, "" + trackingID, (start_x,start_y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # cv2.putText(frame, "{}".format(label), (int((start_x + end_x)/2),int((start_y  + 50))), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 4)   

        fps  = ( fps + (1./(time.time()-t1)) ) / 2
        cv2.putText(frame, "FPS: {:.2f}".format(fps), (0, 60),
                          cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)

        cv2.imshow("preview", frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break


