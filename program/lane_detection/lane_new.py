# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 00:08:40 2018

@author: Jannis
"""
import cv2
import numpy as np  
from lane_functions import lane_pipeline

img_name = 'project_images/lane_test_1.jpg'
image = cv2.imread(img_name)

src = np.float32([[415,150],[505,320],[180,320],[285,150]]) # Define 4 source points for perspective tansformation
dst = np.float32([[450,0],[450,320],[150,320],[150,0]]) # Define 4 destination points for perspective tansformation

result = lane_pipeline(image, src, dst)

cv2.imshow('result', result) 
cv2.waitKey(0)
cv2.destroyAllWindows()