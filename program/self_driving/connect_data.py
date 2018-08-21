# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 11:41:43 2018

@author: Jannis
"""

import os
import numpy as np
import cv2

img_all = []
for number in range(1,3): # Adjust range accordingly
    directory_1 = 'time_press_release_' + str(number) + '/'
    path = os.listdir(directory_1)
    
    press_file = open(directory_1+path[0], 'r')
    time_file = open(directory_1+path[1], 'r')
    
    press_lines = press_file.readlines(); press_lines = press_lines[0::2]
    time_lines = time_file.readlines(); time_lines = time_lines[0::2]
    
    time_lines = [round(float(i.split('\n')[0]),2) for i in time_lines]
    
    start = time_lines[0]
    end = time_lines[-1]
    
    time_all = np.arange(start,end,0.01); time_all = np.round(time_all, 2)
    
    
    key_all = []
    prevous_key = ''
    u = 0
    for i in time_all:
        if i == time_lines[u]:
            previous_key = press_lines[u]
            key_all.append(previous_key)
            u+=1
        else:
            key_all.append(previous_key)
            
      
    directory_2 = 'driving_frames_' + str(number) + '/'
    path = os.listdir(directory_2)
    key_img = []
    for i in path:      
        img = round(float(i.split('.jpg')[0]),2)
        
        if any(time_all == img):
            time_new = np.where(time_all == img)[0][0]
            key_img.append(key_all[time_new])           
            img_new = cv2.imread(directory_2+i)
            img_name = key_all[time_new].split('\n')[0]+'_'+i
            img_all.append(img_name)
    
            cv2.imwrite('IMG/'+img_name, img_new)

with open('driving_data.txt', 'w') as data_file:  
    for data in img_all:
        data_file.write('%s\n' % data)           
    
