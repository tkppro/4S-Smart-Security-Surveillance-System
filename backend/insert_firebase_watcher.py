from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time

import pathlib
from glob import glob

import cv2
import json
import os
from firebase import uploadRecord

FOLDER_JSON_DONE = './data_json/done/'

def upload_firebase(json_file):
    image_name = json_file.split("\\")[-1]
    if(image_name == json_file):
        image_name = json_file.split("/")[-1]

    print ('picture:',image_name)
    if image_name != "data_json":
        
        with open(FOLDER_JSON_DONE + image_name, 
            encoding='utf-8', 
            errors='ignore') as json_data:
            data = json.load(json_data, strict=False)
            
            objectPushData = {
                'name':  data['name'],
                'image': data['image'],
                'detectedAt': data['detectedAt'],
                'visibleTime': data['visibleTime']
            }
            print('prepare data and ready to push:', objectPushData)
            print(uploadRecord(objectPushData))

        # sleep 3 second waiting for data inserted into Firebase
        # time.sleep(3)
        # if os.path.exists(json_file):
        #     print ('removed ' + json_file)
        #     os.remove(json_file)


class Watcher:
    DIRECTORY_TO_WATCH = "./data_json/done"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):
    
    @staticmethod
    def  on_created(event):
        print(f"hey, {event.src_path} has been created!")
        
        upload_firebase(event.src_path)


if __name__ == '__main__':
    print('Initializing insert firebase watcher.....')
    w = Watcher()
    w.run()
