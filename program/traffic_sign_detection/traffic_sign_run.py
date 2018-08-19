# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 16:52:27 2018

@author: Jannis
"""
from keras.models import load_model
import glob
import time
from traffic_sign_functions import sign_pipeline    

model = load_model('model_traffic_3_25_epochs.h5')

path_name = 'traffic_sign_test/'
path = glob.glob(path_name + '*.jpg')
sign_pipeline(path, model)