# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 16:42:44 2018

@author: Jannis
"""
import cv2
import numpy as np
import glob
import time

def hough_lines(img_org, img_binary, rho=1, theta=np.pi/180, threshold=15, min_line_len=50, max_line_gap=40):
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
            
        cv2.line(img_org,(x1,y1),(x2,y2),(0,255,0),2)
        m = (y2-y1)/(x2-x1)
        text = 'Slope: ' + str(m)
        cv2.putText(img_org, text, (10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)

    return img_org

def find_contours(img_org, binary_img):
    """
    img_binary should be the output of a binary threshold transform. 
    img_org is original image to be drawn on     
    Returns an image with rectangle(s) drawn around regions of interest
    """    
    _,contours, _= cv2.findContours(binary_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #perimeter = cv2.arcLength(cnt,True)
        x,y,w,h = cv2.boundingRect(cnt)
        #print(perimeter); print(area); print(x,y,w,h); print(w-h)
        if area < 400:
            continue
                
      	 # compute the bounding box for the contour, draw it on the frame
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(img_org, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
    return img_org


def run(img_names):       
    firstFrame = None
    for name in img_names:
        frame = cv2.imread(name)
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
        thresh = cv2.dilate(thresh, None, iterations=5)
            
        if np.sum(thresh) > 200000:
            frame = hough_lines(frame, thresh)
    
        frame = find_contours(frame, thresh)        
    
        #cv2.imwrite('frames_barrier_car/'+str(time.time())+'.jpg', frame)
        #cv2.imshow('gray', gray)
        #cv2.imshow('thresh', thresh)
        cv2.imshow('frame', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        

if __name__ == "__main__":    
    img_names = glob.glob('barrier_moving/*.jpg')
    run(img_names)