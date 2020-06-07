from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time

import pathlib
from glob import glob

import cv2
import json
import os

import new_recognize_image


def recognize_faces():
    try:

        new_recognize_image.handle()

    except Exception as inst:
        print ("error:", inst)

def recognize_face_single_image(image):
    try:
        new_recognize_image.handle_single_image(image)
    except Exception as inst:
        print ("error:", inst)


class Watcher:
    DIRECTORY_TO_WATCH = "./pictures/raw"

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

    # @staticmethod
    # def on_any_event(event):
    #     # delay for image loaded
    #     time.sleep(3)
    #     recognize_faces()

    @staticmethod
    def on_created(event):
        # waiting for 15+1 second until json file has been created
        time.sleep(16)
        recognize_face_single_image(event.src_path)

if __name__ == '__main__':

    w = Watcher()
    w.run()
