# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 12:43:18 2018

@author: Jannis
"""
import numpy as np
import cv2
import socket
import struct
import io
import time
from keras.models import load_model

import iota
#from iota import Iota
#from iota import Address

#import zxing
from driving_functions import sign_threshold, slide_window, predict_sign, read_qr_code, barrier_motion


def run(model, conncetion, conncetion_2):
    state = 'Normal'  # State of the car
    stop_detect = 0  # Stop sign detection count; avoid false positives
    flag = 1  # Printing flag
    first_frame_barrier = None  # Barrier motion detection frame initialisation
                
    print('Start collecting images...')

    # stream video frames one by one
    try:
        while True:
            if flag:
                print('State:', state)
                flag = 0
                
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            image_stream.seek(0)
            data = np.frombuffer(image_stream.getvalue(), dtype=np.uint8)
            # "Decode" the image from the array, preserving colour
            img = cv2.imdecode(data, 1)   
            #cv2.imwrite('driving_frames_pc/'+str(time.time())+'.jpg', img)  # Save image
                    
            if state == 'Barrier':
                print('Approaching Barrier...')
                time.sleep(7) # 5sec to establish new camera stream
                state = 'qr-code'
                flag = 1  # Printing flag
    
            elif state == 'qr-code':  # Search for QR-Code and decode + make transaction
                
                print('Scanning for QR-Code...')
                barrier_address = read_qr_code(img, display = False)
                if barrier_address:
                    print('Extracted QR-Code!')
                    print('Address:', barrier_address)
                      
                ########## MAKE PAYMENT ###########
                uri = ""  #  Node URL  
                depth = 3        
                # Receiver seed
                send_seed = ""  # Sending Seed
                send_addr = ""  # Sending address derived from seed/private key
                rec_addr = barrier_address 
    
                # Create an IOTA object
                api = iota.Iota(uri, seed=send_seed)
                print('Making transaction...')
                # Make transaction
                proposedTransaction = iota.ProposedTransaction(address = iota.Address(rec_addr), value = 2)
    
                transfer = api.send_transfer(transfers = [proposedTransaction], 
                      depth = depth,
                      inputs = [iota.Address(send_addr, key_index=0, security_level=2)])
         
                connection_2.send(b'4')  # Send QR-Code extracted signal to Pi
                time.sleep(7) # 5sec to establish new camera stream
                state = 'barrier_motion_detection'            
                flag = 1  # Printing flag
    
            elif state == 'barrier_motion_detection':  # Barrier motion detection
                if first_frame_barrier is None:
                    first_frame_barrier = cv2.cvtColor(img, cv2.COLOR_BGRGRAY)
                    connection_2.send(b'0')
                else:
                    slope = barrier_motion(img, first_frame_barrier)
                    if slope > 1:
                        connection_2.send(b'5')
                        print('Keep driving!')
                        state = 'Normal'
                        flag = 1  # Printing flag
                    else:
                        connection_2.send(b'0')
                        
                      
            else:  # Normal driving state; state == 'normal'
                img = cv2.resize(img, (640,320))
                # Threshold image and extract region proposals
                mask, img = sign_threshold(img)
                windows = slide_window(img, x_start_stop=[380, None], y_start_stop=[70, 180], 
                                        xy_window=(32, 32), xy_overlap=(0.25, 0.25))
                for window in windows:
                    # Threshold region proposals, skip low pixel value regions (i.e. black regions)
                    if np.sum(mask[window[0][1]:window[1][1],window[0][0]:window[1][0]]) <= 100000:
                        next
                    else:
                        img_cropped =  img[window[0][1]:window[1][1],window[0][0]:window[1][0],:]  # Extract single window
                        img_cropped_copy = img_cropped.copy()
                        pred_num, prob = predict_sign(img_cropped, model)  # Predict single window
    
                        if pred_num == 3 and prob > 0.99:  # If prediction equals stop sign (==3) with high confidence (> 0.99)
                            print(pred_num, "----", prob, '----', time.time())
                            stop_detect += 1  # To avoid false positives, initiate a detection count
                            if stop_detect == 1:
                                stop_first = time.time()  # Time value at first stop sign detection
                                connection_2.send(b'0')  # Send no stop sign detected signal to Pi
                            elif stop_detect == 3:  # If 3 consecutive images were stop sign
                                if time.time() - stop_first < 2:  # if time between detections below 2 sec.
                                    connection_2.send(b'1')  # Send stop sign detected signal to Pi
                                    print(pred_num, "----", prob, '----', time.time())
                                    #cv2.imwrite('stop_detecion/'+str(time.time())+'.jpg', img_cropped_copy) # Save cropped image of (predicted) stop sign
                                    state = 'Barrier'  # Change state to barrier
                                    flag = 1  # Printing flag
                                    time.sleep(13) # 5sec halt + ~8sec barrier approaching
                                else:
                                    stop_detect = 0  # If no stop sign detected, set count=0
                                    connection_2.send(b'0')  # Send no stop sign detected signal to Pi
                            else:
                                connection_2.send(b'0')  # Send no stop sign detected signal to Pi
                        else:
                            connection_2.send(b'0')  # Send no stop sign detected signal to Pi
                
    
    finally:
        connection.close()
        connection_2.close()
        server_socket.close()
        server_socket_2.close()

if __name__ == "__main__":
    model = load_model('model_traffic_3_25epochs.h5')
        
    # Image stream from Pi
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)
    # accept a single connection
    connection = server_socket.accept()[0].makefile('rb')
    
    # Signal stream to Pi 
    server_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_2.bind(('0.0.0.0', 8001))
    server_socket_2.listen(1)
    
    connection_2, addr_2 = server_socket_2.accept()
    
    run(model, connection, connection_2)
