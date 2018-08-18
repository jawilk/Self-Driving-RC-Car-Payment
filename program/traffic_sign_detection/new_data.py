# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 00:35:24 2018

@author: Jannis
"""

import pickle
import numpy as np
import glob
import cv2
import sys


def get_new_data(label, data_dir):
    ###  Set path to image directory
    path = glob.glob(data_dir+'/*.jpg')
    img_list = []
    for img_name in path:
        img = cv2.imread(img_name)
        img = cv2.resize(img, (32,32))
        img_list.append(img)
        
    img_list = np.array(img_list)
    labels = np.zeros(len(img_list))
    labels.fill(label)
    
    # Save new data
    data_dict = {'features': img_list, 'labels': labels}
    with open(data_dir+'.p', 'wb') as file:
       pickle.dump(data_dict, file, protocol=pickle.HIGHEST_PROTOCOL)
    

if __name__ == "__main__":
    label = int(sys.argv[1])
    data_dir = sys.argv[2]
    get_new_data(label, data_dir)
    print('Finished!')
