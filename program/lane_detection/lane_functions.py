# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 18:10:37 2018

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

def abs_sobel_thresh(image, orient='x', thresh_min=0, thresh_max=255):
    '''
    calculate directional gradient
    apply threshold
    returns binary image
    '''
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply x or y gradient with the OpenCV Sobel() function
    # and take the absolute value
    if orient == 'x':
        abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 1, 0))
    if orient == 'y':
        abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 0, 1))
    # Rescale back to 8 bit integer
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    # Create a copy and apply the threshold
    binary_output = np.zeros_like(scaled_sobel)
    # Here I'm using inclusive (>=, <=) thresholds, but exclusive is ok too
    binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 255      

    # Return the result
    return binary_output

def perspective_transform(img, src, dst, orientation: 'src-dst'):
    '''
    Transfrom perspective of given image from source to destination points
    Return transformed image
    '''
    img_size = img.shape[1::-1]
    
    if orientation == 'src-dst':
        M = cv2.getPerspectiveTransform(src, dst) # Compute the perspective transform matrix M
        
    elif orientation == 'dst-src':
        M = cv2.getPerspectiveTransform(dst, src) # Compute the perspective transform matrix M

    trans_img = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_LINEAR) # Warp an image using the perspective transform matrix M   
    
    return trans_img
    
def histogram_analysis(binary_warped):
    '''
    Find left/right peak in histogram
    Return peak x-value
    '''
    
    histogram = np.sum(binary_warped[250:280,:], axis=0) # Take a histogram of the bottom half of the image
    # Find the peak of the left and right halves of the histogram
    # These will be the starting point for the left and right lines
    midpoint = np.int(histogram.shape[0]//2)
    if np.max(histogram[:midpoint]) <= 2000:
        histogram = np.sum(binary_warped[100:280,:], axis=0) # Take a histogram of the bottom half of the image
        leftx_base = np.where(histogram[:midpoint] > 2000)[0][-1]
    else:
        leftx_base = np.where(histogram[:midpoint] > 2000)[0][-1]

    if np.max(histogram[midpoint:]) <= 2000:
        histogram = np.sum(binary_warped[100:280,:], axis=0) # Take a histogram of the bottom half of the image
        rightx_base = np.where(histogram[midpoint:] > 2000)[0][0] + midpoint
    else:
        rightx_base = np.where(histogram[midpoint:] > 2000)[0][0] + midpoint
    
    return leftx_base, rightx_base

def window_search(binary_warped, nonzeroy, nonzerox, nwindows, window_height, leftx_base, rightx_base, margin, minpix):
    '''
    Search left/right lane parts with ascending window search (image bottom -> up)
    Return left/right line pixel positions
    '''
    # Create empty lists to receive left and right lane pixel indices
    left_lane_inds = []
    right_lane_inds = []
    
    # Current positions to be updated for each window
    leftx_current = leftx_base
    rightx_current = rightx_base

    for window in range(nwindows): # Step through the windows one by one
       
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
            
    # Concatenate the arrays of indices
    left_lane_inds = np.concatenate(left_lane_inds)
    right_lane_inds = np.concatenate(right_lane_inds)

    # Extract left and right line pixel positions
    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds] 
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds] 

    return leftx, lefty, rightx, righty, left_lane_inds, right_lane_inds
 
def fit_poly_line(x_values, y_values, shape_0, orientation = 'Left'):
    '''
    Fit 2nd order polynomial to a line (left/right)
    Return points on line
    '''
    # Fit a second order polynomial to each
    line_fit = np.polyfit(y_values, x_values, 2)

    ploty = np.linspace(0, shape_0 - 1, shape_0)
    line_fitx = line_fit[0]*ploty**2 + line_fit[1]*ploty + line_fit[2]
    
    if orientation == 'Left':
        pts = np.array([np.transpose(np.vstack([line_fitx, ploty]))])
    elif orientation == 'Right':
        pts = np.array([np.flipud(np.transpose(np.vstack([line_fitx, ploty])))])
    
    return pts, line_fitx

def lane_pipeline(image, src=[], dst=[]):
    '''
    '''
    #undist_img = cal_undistort(image, objpoints, imgpoints)
    #undist_img = image
    x_binary = abs_sobel_thresh(image, orient='x', thresh_min=20, thresh_max=100)
    x_binary = perspective_transform(x_binary, src, dst, orientation = 'src-dst')
    
    leftx_base, rightx_base = histogram_analysis(x_binary)       
        
    nwindows = 12 # Choose the number of sliding windows
    window_height = np.int(x_binary.shape[0]//nwindows) # Set height of windows
    margin = 40 # Set the width of the windows +/- margin
    minpix = 35 # Set minimum number of pixels found to recenter window
            
    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = x_binary.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])
    leftx, lefty, rightx, righty, left_lane_inds, right_lane_inds  = window_search(x_binary, nonzeroy, nonzerox, nwindows, window_height, leftx_base, rightx_base, margin, minpix)
    pts_left, left_fitx = fit_poly_line(leftx, lefty, x_binary.shape[0], 'Left')
    pts_right, right_fitx = fit_poly_line(rightx, righty, x_binary.shape[0], 'Right')
    pts = np.hstack((pts_left, pts_right))

    window_img = np.zeros_like(image) # PLaceholder image  
    

    # Draw the lane onto the warped blank image
    window_img[nonzeroy[left_lane_inds], nonzerox[left_lane_inds]] = [0, 0, 255]
    window_img[nonzeroy[right_lane_inds], nonzerox[right_lane_inds]] = [255, 0, 0]
    window_img = cv2.dilate(window_img, np.ones((11, 11)))
        
    cv2.fillPoly(window_img, np.int_([pts]), (0,255, 0))
    unwarped = perspective_transform(window_img, src, dst, orientation = 'dst-src')
    result = cv2.addWeighted(unwarped, 0.1, image, 1 - 0.4, 50)
    
    return result