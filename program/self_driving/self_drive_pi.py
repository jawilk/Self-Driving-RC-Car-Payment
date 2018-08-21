# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 17:01:04 2018

@author: Jannis
"""

import cv2
import numpy as np
from keras.models import load_model
import bluetooth
import time

from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera

      
def predict_image(camera, rawCapture, model, sock):
    print('Capturing frames...')
    print('Press Ctrl-C to end')

    try:
        # capture frames from the camera
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            img = frame.array
         
            #img = cv2.imread(i,0)
            #img = cv2.resize(img, (320,160))
            img = np.expand_dims(img, axis=0)
            img = np.expand_dims(img, axis=3)
            pred = model.predict(img)
            pred = str(np.where(pred==np.max(pred))[1][0])
            
            if pred == 0:
                command = b"W"
            elif pred == 1:
                command = b"Q"
            elif pred == 2:
                command = b"E"
            print(pred)
            sock.send(command)
            
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)
       
    except (KeyboardInterrupt, picamera.exc.PiCameraValueError): 
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        print('Stopped')
        pass

def get_device():
    return bluetooth.discover_devices()[0] # '00:13:EF:00:0D:FE'

if __name__ == "__main__":
    model = load_model('driving_model.h5')

    bd_addr = get_device()
    port = 1
    sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port)) 
    
    previous = ''

    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (320, 160)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(320, 160))
    
    # allow the camera to warmup
    time.sleep(0.1)

    predict_image(camera, rawCapture, model, sock)
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    

