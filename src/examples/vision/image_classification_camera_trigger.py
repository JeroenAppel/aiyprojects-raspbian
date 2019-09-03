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
import requests

from aiy.vision.inference import CameraInference
from aiy.vision.models import image_classification
from picamera import PiCamera

def classes_info(classes):
    return ', '.join('%s (%.2f)' % pair for pair in classes)

@contextlib.contextmanager
def CameraPreview(camera, enabled):
    if enabled:
        camera.start_preview()
    try:
        yield
    finally:
        if enabled:
            camera.stop_preview()

def postRequest(label, score):
    # defining the api-endpoint  
    API_ENDPOINT = "http://pastebin.com/api/api_post.php"
    
    # your API key here 
    API_KEY = "a1f20a39b76f05943513b8de15187c4d"
  
    # your source code here 
    message = ''' 
    A new banana has been detected!
    Score: ''' + str(score)
  
    # data to be sent to api 
    data = {'api_dev_key':API_KEY, 
           'api_option':'paste', 
           'api_paste_code':message, 
           'api_paste_format':'python'} 
  
    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, data = data) 
  
    # extracting response text  
    pastebin_url = r.text 
    print("The pastebin URL is:%s"%pastebin_url) 

def main():
    parser = argparse.ArgumentParser('Image classification camera inference example.')
    parser.add_argument('--num_frames', '-n', type=int, default=None,
        help='Sets the number of frames to run for, otherwise runs forever.')
    parser.add_argument('--num_objects', '-c', type=int, default=3,
        help='Sets the number of object interences to print.')
    parser.add_argument('--nopreview', dest='preview', action='store_false', default=True,
        help='Enable camera preview')
    args = parser.parse_args()

    with PiCamera(sensor_mode=4, framerate=30) as camera, \
         CameraPreview(camera, enabled=args.preview), \
         CameraInference(image_classification.model()) as inference:
        for result in inference.run(args.num_frames):
            classes = image_classification.get_classes(result, top_k=args.num_objects)
            print(classes_info(classes))
            if classes:
                camera.annotate_text = '%s (%.2f)' % classes[0]
                label, score = classes[0]
                if 'banana' == label:
                    postRequest(label, score)

if __name__ == '__main__':
    main()
