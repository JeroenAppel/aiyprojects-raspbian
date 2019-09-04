#!/usr/bin/env python3
#
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Camera image classification demo code.

Runs continuous image classification on camera frames and prints detected object
classes.

Example:
image_classification_camera.py --num_frames 10
"""
import argparse
import contextlib
import time
import enum
import requests

from aiy.vision.inference import CameraInference
from aiy.vision.models import image_classification
from picamera import PiCamera

def classes_info(classes):
    return ', '.join('%s (%.2f)' % pair for pair in classes)

def getMilliseconds():
    millis = int(round(time.time() * 1000))
    return millis

def itemLost(lastseen, current):
    if lastseen is None:
        return False
    else:
        if (lastseen + 5000) < current:
            return True
        else:
            return False

@contextlib.contextmanager
def CameraPreview(camera, enabled):
    if enabled:
        camera.start_preview()
    try:
        yield
    finally:
        if enabled:
            camera.stop_preview()

def postRequest(label, score, operation):
    # the current sandbox environment
    API_ENDPOINT = "https://fruitninja-sandbox.mxapps.io/rest/aitrigger/v1/fruit/" + operation
    
    # the auth credentials should be moved to environment variables soon
    USER = 'googleaiy'
    PASS = 'ZE76!9@C7t#fqRgg'
  
    # the image feature will be implemented later 
    image = 'The image feature has not been implemented.'
  
    # data to be sent to FruitNinja 
    data = {'FruitName':label, 
           'Score':str(score), 
           'Base64Image':image }
  
    # sending post request and print response whenever this actions runs in to an error
    r = requests.post(url = API_ENDPOINT, json = data, auth = (USER, PASS))
    
    if r.status_code == requests.codes.ok:
        print('An update has been send to FruitNinja')
    else:
        print('Something went wrong while informing FruitNinja') 
        print('Content: ' + str(r.content))

def main():
    parser = argparse.ArgumentParser('Image classification camera inference example.')
    parser.add_argument('--num_frames', '-n', type=int, default=None,
        help='Sets the number of frames to run for, otherwise runs forever.')
    parser.add_argument('--num_objects', '-c', type=int, default=3,
        help='Sets the number of object interences to print.')
    parser.add_argument('--nopreview', dest='preview', action='store_false', default=True,
        help='Enable camera preview')
    args = parser.parse_args()

    # Initialize all the fruits which are supported by the model.
    class wait_status(enum.Enum): 
        waitForRemove = 1
        waitForAdd = 2

    current_time = None
    supported_fruits = ('banana', 'apple', 'orange')
    fruit_seen = {
        'banana':0,
        'apple':0,
        'orange':0
        }
    fruit_status = {
        'banana':wait_status.waitForAdd,
        'apple':wait_status.waitForAdd,
        'orange':wait_status.waitForAdd
        }

    with PiCamera(sensor_mode=4, framerate=30) as camera, \
         CameraPreview(camera, enabled=args.preview), \
         CameraInference(image_classification.model()) as inference:
        for result in inference.run(args.num_frames):
            classes = image_classification.get_classes(result, top_k=args.num_objects)
            print(classes_info(classes))
            if classes:
                camera.annotate_text = '%s (%.2f)' % classes[0]
                current_time = getMilliseconds()
                for item in classes:
                    # label, score = classes[0]
                    label, score = item
                    if label in supported_fruits:
                        fruit_seen[label] = current_time
                        if fruit_status[label] == wait_status.waitForAdd:
                            print('Send message to FruitNinja: ' + label + ' added')
                            postRequest(label, score, 'add')
                            fruit_status[label] = wait_status.waitForRemove

                for fruit in fruit_status:
                    # We will now check all the fruits which are not detected. TODO: Verify if the fruit lookup in classes is working as expected
                    if (fruit in classes) == False:
                        if fruit_status[fruit] == wait_status.waitForRemove:
                            lostItem = itemLost(fruit_seen[fruit], current_time)
                            if lostItem:
                                print('Send message to FruitNinja: ' + fruit + ' removed')
                                postRequest(label, score, 'remove')
                                fruit_status[fruit] = wait_status.waitForAdd

if __name__ == '__main__':
    main()
