# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 21:12:51 2018

@author: Jannis
"""

import pickle
import numpy as np

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.utils import np_utils

from sklearn.model_selection import train_test_split

def normalize(image_data, a=0.1, b=0.9):
    """
    Normalize the image data with Min-Max scaling to a range of [0.1, 0.9]
    :param image_data: The image data to be normalized
    :return: Normalized image data
    """
    # Implement Min-Max scaling for image data
    return a + (((image_data-np.min(image_data)) * (b - a)) / (np.max(image_data) - np.min(image_data)))

batch_size = 64
nb_classes = 6 # background, 50_kmh, priority, stop, right_curve, no_passing
nb_epoch = 10

img_rows, img_cols, channels = 32, 32, 3

training_file = 'pickles/traffic_sign_all.p'

with open(training_file, mode='rb') as f:
    data = pickle.load(f)

    
X, y = data['features'], data['labels']
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

X_train = normalize(X_train)
X_valid = normalize(X_valid)

y_train = np_utils.to_categorical(y_train, nb_classes)
y_valid = np_utils.to_categorical(y_valid, nb_classes)


model = Sequential()

model.add(Convolution2D(24, 5, 5, border_mode='valid', input_shape=(img_rows, img_cols, channels)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(64, 5, 5, border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(64, 3, 3, border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(240))
model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(168))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=nb_epoch, validation_data=(X_valid, y_valid))
    
model.save('model_traffic_2_10epochs.h5')

'''
from keras.models import load_model
model = load_model('traffic_1.h5')

import os
import cv2

#l = []
path = os.listdir()
for i in path:
    img = cv2.imread(i)
    img = cv2.resize(img, (32,32))
    img_org = img.copy()
    img = normalize(img)
    img = np.expand_dims(img, axis=0)
    pred = model.predict(img)
    print(np.where(pred==np.max(pred))[1][0], "----", np.max(pred))
    cv2.imshow(str(np.where(pred==np.max(pred))[1][0]), img_org)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    #l.append(np.where(b==np.max(pred))[1][0])
''' 
