# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 19:22:06 2018

@author: Jannis
"""
import numpy as np
import cv2

def sign_threshold(img):
    '''
    Thresholding function to search for traffic sign candidates
    :param img: Single image to be thresholded
    :return: Thresholded image data
    '''
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

def slide_window(img, x_start_stop=[None, None], y_start_stop=[None, None], 
                    xy_window=(64, 64), xy_overlap=(0.5, 0.5)):
    '''
    Define a function that takes an image start and stop positions in both x and y, 
    window size (x and y dimensions),  and overlap fraction (for both x and y)
    :return: List of extracted windows
    '''

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
    '''
    Predicting function to predict traffic sign in cropped image 
    :param img: Single cropped image; trained model 
    :return: prediction number (0-5); probability of prediction
    '''
    img_cropped = cv2.resize(img_cropped, (32,32))
    img_cropped = normalize(img_cropped)
    img_cropped = np.expand_dims(img_cropped, axis=0)
    pred = model.predict(img_cropped)
    pred_num = np.where(pred==np.max(pred))[1][0]
    prob = np.max(pred)
    
    return pred_num, prob


def sign_pipeline(path_to_images, model):
    '''
    '''
    prev_pred = 0
    for img_name in path_to_images:
        image = cv2.imread(img_name)
        image = cv2.resize(image, (640,320))
        img_2 = image.copy()
        mask, image = sign_threshold(image)
        windows = slide_window(image, x_start_stop=[480, None], y_start_stop=[70, 180], 
                                        xy_window=(32, 32), xy_overlap=(0.25, 0.25))
        img_tiny = []
        img_sign = None
        for window in windows:
            #cv2.rectangle(image, window[0], window[1], (0,0,255), 4) # show all boxes
            if np.sum(mask[window[0][1]:window[1][1],window[0][0]:window[1][0]]) <= 100000:
                next
            else:
             #   cv2.rectangle(image, window[0], window[1], (0,0,255), 4) # show thresholded boxes
                img_cropped =  img_2[window[0][1]:window[1][1],window[0][0]:window[1][0],:]
                img_cropped_copy = img_cropped.copy()
                pred_num, prob = predict_sign(img_cropped, model)
                if pred_num != 0 and prob > 0.99:
                    #cv2.imwrite('test_new/'+str(time.time())+'_'+str(pred_num)+'_.jpg', image) #img_cropped_copy
                    if  prev_pred == pred_num:
                        img_tiny = img_cropped_copy      
                        img_sign = cv2.imread('traffic_sign_img/sign_'+str(pred_num)+'.jpg')
                        cv2.rectangle(image, window[0], window[1], (0,255,0), 4)
                    prev_pred = pred_num
                    
        if len(img_tiny) != 0:
            y_offset = 60; x_offset = 0
            image[y_offset:y_offset+img_sign.shape[0], x_offset:x_offset+img_sign.shape[1]] = img_sign
            y_offset = img_sign.shape[0] + 60
            image[y_offset:y_offset+img_tiny.shape[0], x_offset:x_offset+img_tiny.shape[1]] = img_tiny 

        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        #cv2.imwrite('test_new/'+str(time.time())+'_'+str(pred_num)+'_.jpg', image) #img_cropped_copy
    
    return 0