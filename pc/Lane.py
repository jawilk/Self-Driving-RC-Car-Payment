# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 00:35:08 2018

@author: Jannis
"""

import numpy as np
import cv2

def cal_undistort(img, objpoints, imgpoints):
    '''
    Perform camera calibration and image distortion correction 
    Return the undistorted image
    '''
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape[1::-1], None, None)
    undist = cv2.undistort(img, mtx, dist, None, mtx)
   
    return undist


def abs_sobel_thresh(image, thresh_min=0, thresh_max=255):
    '''
    Calculate directional gradient
    Apply threshold
    Return binary image
    '''
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # Convert to grayscale
    abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 1, 0)) # Apply x gradient and take the absolute value
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel)) # Rescale back to 8 bit integer
    binary_output = np.zeros_like(scaled_sobel) # Create a copy and apply the threshold
    binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1 # Here I'm using inclusive (>=, <=) thresholds, but exclusive is ok too
      
    return binary_output    


def hls_select(img, thresh=(0, 255)):
    '''
    Threshold image inside S-channel of HLS image
    Return thresholded binary image
    '''
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS) # Convert image to HLS color space
    s_channel = hls[:,:,2] # Extract S channel
    binary_output = np.zeros_like(s_channel) # Create all black image
    binary_output[(s_channel > thresh[0]) & (s_channel <= thresh[1])] = 1 # Threshold S channel and add print on the black image

    return binary_output


def combine(x_thres_img, s_thres_img):
    '''
    Combine 2 threshold images into 1
    Return combined binary image
    '''  
    combined_binary = np.zeros_like(x_thres_img) # Create all black image
    combined_binary[(x_thres_img == 1) | (s_thres_img == 1)] = 1 # Combine 2 images
    
    return combined_binary


def perspective_transform(img, src, dst):
    '''
    Transfrom perspective of given image from source to destination points
    Return transformed image
    '''
    #src = np.float32([[720,470],[1038,670],[259,670],[562,470]]) # Define 4 source points for perspective tansformation
    #dst = np.float32([[1038,0],[1038,720],[259,720],[259,0]]) # Define 4 destination points for perspective tansformation
    M = cv2.getPerspectiveTransform(src, dst) # Compute the perspective transform, M
    img_size = img.shape[1::-1] # Warp an image using the perspective transform, M
    trans_img = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_LINEAR)
    
    return trans_img
 
    
def histogram_analysis(binary_warped):
    '''
    Find left/right peak in histogram
    Return peak x-value
    '''
    histogram = np.sum(binary_warped[binary_warped.shape[0]//2:,:], axis=0) # Take a histogram of the bottom half of the image
    # Find the peak of the left and right halves of the histogram
    # These will be the starting point for the left and right lines
    midpoint = np.int(histogram.shape[0]//2)
    leftx_base = np.argmax(histogram[:midpoint])
    rightx_base = np.argmax(histogram[midpoint:]) + midpoint
    
    return leftx_base, rightx_base


def window_search(binary_warped, nwindows, window_height, leftx_base, rightx_base, margin, minpix):
    '''
    Search left/right lane parts with ascending window search (image bottom -> up)
    Return left/right line pixel positions
    '''
    # Create empty lists to receive left and right lane pixel indices
    left_lane_inds = []
    right_lane_inds = []
    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = binary_warped.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])
    # Current positions to be updated for each window
    leftx_current = leftx_base
    rightx_current = rightx_base

    # Step through the windows one by one
    for window in range(nwindows):
        # Identify window boundaries in x and y (and right and left)
        win_y_low = binary_warped.shape[0] - (window+1)*window_height
        win_y_high = binary_warped.shape[0] - window*window_height
        win_xleft_low = leftx_current - margin
        win_xleft_high = leftx_current + margin
        win_xright_low = rightx_current - margin
        win_xright_high = rightx_current + margin
        # Identify the nonzero pixels in x and y within the window
        good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) &  (nonzerox < win_xleft_high)).nonzero()[0]
        good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) &  (nonzerox < win_xright_high)).nonzero()[0]
        # Append these indices to the lists
        left_lane_inds.append(good_left_inds)
        right_lane_inds.append(good_right_inds)
        # If you found > minpix pixels, recenter next window on their mean position
        if len(good_left_inds) > minpix:
            leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
        if len(good_right_inds) > minpix:        
            rightx_current = np.int(np.mean(nonzerox[good_right_inds]))
            
    np.concatenate(left_lane_inds), np.concatenate(right_lane_inds)               
    # Extract left and right line pixel positions
    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds] 
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds] 

    return leftx, lefty, rightx, righty
    
def fit_poly_line(leftx, lefty, rightx, righty, shape_0):
    '''
    Fit 2nd order polynomial to left/right line
    Add values to line
    Return left/right line
    '''
    # Fit a second order polynomial to each
    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)

    ploty = np.linspace(0, shape_0 - 1, shape_0)
    left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
    right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]
    
    return left_fitx, right_fitx


def lane_pipeline(image):
    undist_img = cal_undistort(image, objpoints, imgpoints)
    x_binary = abs_sobel_thresh(undist_img, thresh_min=0, thresh_max=255)
    s_binary = hls_select(undist_img, thresh=(0, 255))
    combined_binary = combine(x_binary, s_binary)
    binary_warped = perspective_transform(combined_binary, src, dst)
    leftx_base, rightx_base = histogram_analysis(binary_warped)
    
    nwindows = 9 # Choose the number of sliding windows
    window_height = np.int(binary_warped.shape[0]//nwindows) # Set height of windows
    margin = 75 # Set the width of the windows +/- margin
    minpix = 45 # Set minimum number of pixels found to recenter window
    leftx, lefty, rightx, righty  = window_search(binary_warped, nwindows, window_height, leftx_base, rightx_base, margin, minpix)
    left_fitx, right_fitx = fit_poly_line(leftx, lefty, rightx, righty, binary_warped.shape[0])


