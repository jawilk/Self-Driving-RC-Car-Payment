# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 21:14:25 2018

@author: Jannis
"""
### Source: https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

#import numpy as np
#import cv2
import time
    
import tkinter as tk    
#from tkinter import *
from PIL import ImageTk
import serial

from iota import Iota
from iota import Address

# Function for checking address balance on the IOTA tangle. 
def check_balance(iota_api, iota_address):
    print("Checking Balance...")
    gb_result = iota_api.get_balances(iota_address)
    balance = gb_result['balances']
    return (balance[0])

def is_transaction(iota_api, iota_address): 
    # Get current address balance at startup and use as baseline for measuring new funds being added.   
    current_balance = check_balance(iota_api, iota_address)
    last_balance = current_balance
    while True:
        # Check for new funds
        current_balance = check_balance()
        if current_balance > last_balance:
            last_balance = current_balance
            print(current_balance)
            print("TRANSACTION RECEIVED")
            time.sleep(1)
            
            return 1
        
        else:
            print(current_balance)
    
        # Pause for 1 sec.
        time.sleep(1)


def car_detection(ser, iota_api, iota_address):
    
    '''
    firstFrame = None
    listening = 1
    detected = 0
    w_prev = 0
    h_prev = 0
    count_pos = 0
    
    cap = cv2.VideoCapture(0)

    while listening:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (960,540))
        cv2.imwrite('frames_barrier_normal/'+str(time.time())+'.jpg', frame)
        #cv2.imwrite('frame_'+str(time.time())+'.jpg', frame); u += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue
     
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
     
        # dilate the thresholded image to fill in holes, then find contours
    	# on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        _,contours, _= cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:  # Perimeter = Umfang
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt,True)
            x,y,w,h = cv2.boundingRect(cnt)
            if area < 1000:
                continue
            print(perimeter); print(area); print(x,y,w,h); print(w-h)
            if abs(w_prev - w) < 10 and abs(h_prev - h) < 10:
                count_pos += 1
            else:
                count_pos = 0
                detected = 0
            w_prev = w
            h_prev = h
    
            if count_pos == 20:
                detected = 1
                
    	# compute the bounding box for the contour, draw it on the frame,
    	# and update the text
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
        #cv2.imwrite('frames_barrier_rectangle/'+str(time.time())+'.jpg', frame)
    '''
    try:
        listening = 1
        while listening:
            msg = ser.read(ser.inWaiting()) # read everything in the input buffer
            if 49 in list(msg): #and detected == 1:  # 49 == 1, barrier ultra sonic detected car
                print('Car detected...')
                flag = 0
                time_save = 0
                root = tk.Tk()
                root.geometry('%sx%s+%s+%s'%(1500,1100,-1100,-100)) #(w,h,a,b)
                img = ImageTk.PhotoImage(file="images/qr_code.png")
                panel = tk.Label(image = img)
                panel.configure(bg='black')
                panel.pack(side = "bottom", fill = "both", expand = "yes")
                def callback():
                    img2 = ImageTk.PhotoImage(file='images/safe_drive.png')
                    panel.configure(image=img2)
                    panel.image = img2
                while flag != 2:
                    root.update_idletasks()
                    root.update()
                    trans = is_transaction(iota_api, iota_address)  # checking for transaction
                    if flag == 0 and trans:
                        print('Opening Barrier...')
                        ser.write(b'O')  # Open barrier
                        callback()
                        time_save = time.time()
                        flag = 1
                    if time.time() - time_save > 7 and time_save != 0:
                        ser.send('1')  # Reset barrier
                        root.destroy()
                        flag = 2 
                        
                        state = 'Searching Car'
                        print('State:', state)
                listening = 0
                
    finally:
        ser.close()
        # When everything done, release the capture
        #cap.release()
        #cv2.destroyAllWindows()

if __name__ == "__main__":
    ser = serial.Serial(port='COM4',
            baudrate=9600,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS)
    #ser.isOpen()
    
    # URL to IOTA fullnode used when checking balance
    iotaNode = ""    
    # Create an IOTA object
    api = Iota(iotaNode)   
    # IOTA address to be checked for new funds 
    address = [Address(b'')]
    
    car_detection(ser, api, address)