# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 19:46:21 2018

@author: Jannis
"""
import cv2
import numpy as np
import zxing
#import socket
#import time

def sign_threshold(img):
    # Stop
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(img_hsv)
    mask_1 = cv2.inRange(h, 130, 255)
    mask_2 = cv2.inRange(s, 175, 195)

    # Priority
    lower_color_bounds = np.array([150, 170, 70])
    upper_color_bounds = np.array([255,255,130])
    mask_3 = cv2.inRange(img,lower_color_bounds,upper_color_bounds )
    
    # All/Right curve
    b, g, r = cv2.split(img)
    r_value = 0.2
    g_value = -0.4
    t = 0.5 * 255
    r =  r*r_value
    g = g*g_value
    mask_4 = np.zeros_like(img[:,:,0])
    mask_4[(r + g + b) >= t] = 255
    
    # Road
    mask_5 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask_5[(mask_5<130) & (mask_5>100)] = 255
   
    mask_all = np.zeros_like(mask_1) # Create all black image
    mask_all[(mask_1 == 255) | (mask_2 == 255) | (mask_3 == 255) | (mask_4 == 255)] = 255 # Combine 2 images
    mask_all[mask_5==255] = 0
    kernel = np.ones((7,7), np.uint8)
    mask_all = cv2.dilate(mask_all, kernel, 4)
    
    #img[mask_all == 0] = 0   

    return mask_all, img

# Define a function that takes an imag# start and stop positions in both x and y, 
# window size (x and y dimensions),  
# and overlap fraction (for both x and y)
def slide_window(img, x_start_stop=[None, None], y_start_stop=[None, None], 
                    xy_window=(64, 64), xy_overlap=(0.5, 0.5)):
    # If x and/or y start/stop positions not defined, set to image size
    if x_start_stop[0] == None:
        x_start_stop[0] = 0
    if x_start_stop[1] == None:
        x_start_stop[1] = img.shape[1]
    if y_start_stop[0] == None:
        y_start_stop[0] = 0
    if y_start_stop[1] == None:
        y_start_stop[1] = img.shape[0]
    # Compute the span of the region to be searched    
    xspan = x_start_stop[1] - x_start_stop[0]
    yspan = y_start_stop[1] - y_start_stop[0]
    # Compute the number of pixels per step in x/y
    nx_pix_per_step = np.int(xy_window[0]*(1 - xy_overlap[0]))
    ny_pix_per_step = np.int(xy_window[1]*(1 - xy_overlap[1]))
    # Compute the number of windows in x/y
    nx_buffer = np.int(xy_window[0]*(xy_overlap[0]))
    ny_buffer = np.int(xy_window[1]*(xy_overlap[1]))
    nx_windows = np.int((xspan-nx_buffer)/nx_pix_per_step) 
    ny_windows = np.int((yspan-ny_buffer)/ny_pix_per_step) 
    # Initialize a list to append window positions to
    window_list = []
    # Loop through finding x and y window positions
    # Note: you could vectorize this step, but in practice
    # you'll be considering windows one by one with your
    # classifier, so looping makes sense
    for ys in range(ny_windows):
        for xs in range(nx_windows):
            # Calculate window position
            startx = xs*nx_pix_per_step + x_start_stop[0]
            endx = startx + xy_window[0]
            starty = ys*ny_pix_per_step + y_start_stop[0]
            endy = starty + xy_window[1]
            
            # Append window position to list
            window_list.append(((startx, starty), (endx, endy)))
    # Return the list of windows
    return window_list

def normalize(image_data, a=0.1, b=0.9):
    """
    Normalize the image data with Min-Max scaling to a range of [0.1, 0.9]
    :param image_data: The image data to be normalized
    :return: Normalized image data
    """
    # Implement Min-Max scaling for image data
    return a + (((image_data-np.min(image_data)) * (b - a)) / (np.max(image_data) - np.min(image_data)))

def predict_sign(img_cropped, model):
    img_cropped = cv2.resize(img_cropped, (32,32))
    img_cropped = normalize(img_cropped)
    img_cropped = np.expand_dims(img_cropped, axis=0)
    pred = model.predict(img_cropped)
    pred_num = np.where(pred==np.max(pred))[1][0]
    prob = np.max(pred)
    
    return pred_num, prob

def read_qr_code(img, display = True):
            
    crop_img = img.copy()[600:1100, :500, :]
    crop_img = cv2.resize(crop_img, (500,500))
    
    row, col = crop_img.shape[:2]    
    
    M = cv2.getRotationMatrix2D((col/2,row/2),310,1)
    crop_img = cv2.warpAffine(crop_img,M,(col,row))
            
    new = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    new[new>95] = 255
    new[new<=95] = 0
    new = cv2.dilate(new, None, iterations=11)
    
    mask = np.zeros_like(new)
    _,contours, _= cv2.findContours(new,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #perimeter = cv2.arcLength(cnt,True)
        x,y,w,h = cv2.boundingRect(cnt)
        if abs(w-h) < 100 and area > 5000 and x+y != 0 and y+h < row and x+w < col:
             cv2.fillPoly(mask, pts =[cnt], color=(255,255,255))
             cv2.rectangle(new,(x,y),(x+w,y+h),(255,255,255),2)
      
    crop_img[mask==0] = 0 
    #crop_img = crop_img[y:y+h,x:w+x]
        
    cv2.imwrite('detected_qr_code.jpg', crop_img)
    if display:
        cv2.imshow('crop', crop_img)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
                
    reader = zxing.BarCodeReader()
    barcode = reader.decode('detected_qr_code.jpg')
    barrier_address = barcode.raw
    
    return barrier_address

def hough_lines(img_binary, rho=1, theta=np.pi/180, threshold=15, min_line_len=50, max_line_gap=40):
    """
    img_binary should be the output of a binary threshold transform. 
    img_org is original image to be drawn on     
    Returns an image with hough lines drawn + text of line curvature in top left corner
    """    
    lines = cv2.HoughLines(img_binary, rho, theta, threshold, min_line_len, max_line_gap)
    for rho_new, theta_new in lines[0]:
        a = np.cos(theta_new)
        b = np.sin(theta_new)
        x0 = a*rho_new
        y0 = b*rho_new
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
            
        slope = (y2-y1)/(x2-x1)        

    return slope

def barrier_motion(img, first_frame_barrier):       
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
 
    frameDelta = cv2.absdiff(first_frame_barrier, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
    # dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=5)
        
    if np.sum(thresh) > 200000:
        slope = hough_lines(thresh)
    else:
        slope = 0

    return slope       