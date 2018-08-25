# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 19:57:46 2018

@author: Jannis
"""
import io
import socket
import struct
#import threading
import time
import cv2
import numpy as np
import bluetooth
from keras.models import load_model

import picamera
from picamera import PiCamera


def predict_driving(img, model):
    """
    Predict key presses for driving (Left/Forward/Right)
    :param img: The image from the Pi camera, model: The pre trained driving model
    :return: Driving command
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Grayscale 
    img = cv2.resize(img, (320,160))  # Resize to fit model input size
    img = np.expand_dims(img, axis=0)  # Expand axis to fit model input size
    img = np.expand_dims(img, axis=3)  # Expand axis to fit model input size
    pred = model.predict(img)
    pred = np.where(pred==np.max(pred))[1][0]  # Extract prediction with highest probability
    
    if pred == 0:
        command = b"W"
        print('Prediction: W')
    elif pred == 1:
        command = b"Q"
        print('Prediction: Q')
    elif pred == 2:
        command = b"E"
        print('Prediction: E')

    return command


def stream_qr(model, sock, connection, client_socket_2):
    """
    Stream images (640x320) to PC for stop sign detection
    Predict key presses for driving (Left/Forward/Right) and send signal to arduino
    :param model: The pre trained driving model, sock: Bluetooth connection to ardunio (HC-06),
    connection: Image stream to PC, client_socket_2: Signal stream to PC
    :return: - (No direct return, after finish go back to stream_normal function)
    """
    print('Looking for QR-code')
    time.sleep(2)  # Let camera cool down
    camera = PiCamera()
    camera.resolution = (2048, 1236)
    camera.framerate = 10
    # Set some camera parameters to avoid different image qualities
    camera.iso = 800  # Set ISO to the desired value
    time.sleep(2)  # Wait for the automatic gain control to settle
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
            
    time.sleep(0.1)  # allow the camera to warmup
    
    stream = io.BytesIO()  # Image stream to PC
    BUFFER_SIZE = 1024  # Signal stream message buffer
    
    # send jpeg format video stream
    for frame in camera.capture_continuous(stream, format='jpeg', use_video_port = True):
        print('Stream 2')
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        stream.seek(0)
        connection.write(stream.read())            
    
        is_qr = client_socket_2.recv(BUFFER_SIZE) # Check for signal from PC if qr code detected
        if 52 in list(is_qr):  # 52 == 4
            print('QR-code found')
            camera.close()  # Close Qr-Code stream
            break  # Break streaming
        stream.seek(0)
        stream.truncate()

    time.sleep(2)  # Let camera cool down
    stream_normal(model, sock, connection, client_socket_2, barrier=1) # Go back to normal stream
        

def stream_normal(model, sock, connection, client_socket_2, barrier=0):
    """
    Stream images (640x320) to PC for stop sign detection
    Predict key presses for driving (Left/Forward/Right) and send signal to arduino
    :param model: The pre trained driving model, sock: Bluetooth connection to ardunio (HC-06),
    connection: Image stream to PC, client_socket_2: Signal stream to PC, barrier: Logic argument, if true check for barrier movement
    :return: -
    """
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 320)
    camera.framerate = 25
    # Set some camera parameters to avoid different image qualities
    camera.iso = 800  # Set ISO to the desired value
    time.sleep(2)  # Wait for the automatic gain control to settle
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
            
    time.sleep(0.1)  # allow the camera to warmup

    print('Driving...')
    print('Press Ctrl-C to end')

    try:    
        stream = io.BytesIO()  # Image stream to PC
        BUFFER_SIZE = 1024  # Signal stream message buffer
        stop_time = 0  # Time measure from arrival at stop sign
        
        # Send jpeg format video stream
        for frame in camera.capture_continuous(stream, format='jpeg', use_video_port = True):
            print('Stream 1')
            # PC stream
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())  
        
            # Grab image from camera for driving prediction on Pi
            data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
            # "Decode" the image from the array, preserving colour
            img = cv2.imdecode(data, 1)
            cv2.imwrite('driving_frames_pi/'+str(time.time())+'.jpg', img)  # Save timnestamped images 
    
            if barrier: # check for barrier movement
            
                is_barrier = client_socket_2.recv(BUFFER_SIZE)
                if 53 in list(is_barrier):  # 53 == 5, barrier open signal from PC backend
                    barrier = 0
                    print('Keep driving!')
                    sock.send(b"W") # Start car
                stream.seek(0)
                stream.truncate()
          
            else:
                is_stop = client_socket_2.recv(BUFFER_SIZE)  # Read signal stream from PC for stop sign detection signal
                print('Stop:', is_stop)
                if 49 in list(is_stop): # 49 == 1; stop sign detected on PC backend
                    print('STOP!')
                    sock.send(b"O") # Stop car, send signal to arduino
                    time.sleep(5) # Wait 5 seconds
                    #sock.send(b"2") # increase speed
                    stop_time = time.time()  # Measure time before resume driving
                    print('Approaching BARRIER!')
                    command = predict_driving(img, model)
                    sock.send(command)  # Send driving signal to arduino
    
                    '''
                elif 50 in list(is_stop):
                    print('Approaching BARRIER!')
                    command = predict_driving(img, model)
                    sock.send(command)
                elif 51 in list(is_stop):
                    print('BARRIER infront, stopping.')
                    sock.send(b"O") # Stop car
                    '''
                else:
                    command = predict_driving(img, model)
                    sock.send(command)
    
                stream.seek(0)
                stream.truncate()
                
                if time.time() - stop_time > 8 and stop_time != 0: # Take ~8sec from stop sign to approach barrier
                    print('Stopping driving stream')
                    sock.send(b"O") # Stop car
                    camera.close()
                    break

        stream_qr(model, sock, connection, client_socket_2) # after "break" 1st stream, open 2nd one with higher resolution for qr_code img streaming 
    
    except (KeyboardInterrupt, picamera.exc.PiCameraValueError): 
        print('Stopped')
        camera.close()
        connection.close()
        client_socket.close()
        client_socket_2.close()
        pass

def get_device():
    """
    :return: available bluetooth connections
    """
    return bluetooth.discover_devices()[0] # '00:13:EF:00:0D:FE'

if __name__ == "__main__":
    # Load trained self-driving model from disc (within Pi)
    model = load_model('driving_model.h5')
    # Connect to HC-06 bluetooth module to send driving signals to arduino
    bd_addr = get_device()
    port = 1
    sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port)) 
    sock.send(b"3")# Car speed adjustment, change as needed; see arduino car_control_bluetooth.ino file
    
    # Image stream to PC
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('Jannis', 8000))
    connection = client_socket.makefile('wb')
    # Signal stream to PC 
    client_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket_2.connect(('Jannis', 8001))
    
    # Start streaming/driving
    stream_normal(model, sock, connection, client_socket_2)