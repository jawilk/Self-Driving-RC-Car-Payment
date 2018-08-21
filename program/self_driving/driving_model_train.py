# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 13:55:37 2018

@author: Jannis
"""

import cv2
import numpy as np
import sklearn

from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Cropping2D, Dropout, Activation
from keras.layers.convolutional import Convolution2D
from keras.utils import np_utils

from sklearn.model_selection import train_test_split

# Load data from working directory
data_file = 'driving_data.txt'
samples_file = open(data_file, 'r')
samples = samples_file.readlines()


# Split data in train set (80%) and validation set (20%)
train_samples, validation_samples = train_test_split(samples, test_size=0.2)

# Change brightness of image for augmentation purpose
def gamma_correction(img, correction):
    img = img/255.0
    img = cv2.pow(img, correction)
    return np.uint8(img*255)

# Define generator to load files in batches from directory 'IMG/' when needed, avoid MemoryError
def generator(samples, nb_classes, batch_size=64):
    num_samples = len(samples)
    while 1: # Loop forever so the generator never terminates
        sklearn.utils.shuffle(samples)
        for offset in range(0, num_samples, batch_size):
            batch_samples = samples[offset:offset+batch_size]

            img_all = []
            key_all = []
            key_num = None
            for batch_sample in batch_samples:
                img_name = 'IMG/' + batch_sample.split('\n')[0]                
                img = cv2.imread(img_name,0)
                img = cv2.resize(img, (320, 160))
                key = batch_sample.split('_')[0]
                if key == 'w':
                    key_num = 0
                elif key == 'q':
                    key_num = 1
                elif key == 'e': 
                    key_num = 2
                else:
                    continue
                img_all.append(img)
                key_all.append(key_num)
                img_all.append(cv2.flip(img, 1))
                key_all.append(abs(key_num - 3) % 3) # Swap 1 and 2 while 0 stays same; f(x)=|x-3|%3
                
                #value = np.random.uniform(0.2,1.5)
                #if value > 0.8 and value < 1.1:
                #    value -= 0.4
                #img_bright = gamma_correction(img, value)
                #img_all.append(img_bright)
                #key_all.append(key_num)

            X_train = np.array(img_all)
            X_train = np.expand_dims(X_train, axis=3)

            #y_train = np.array(key_all)
            y_train = np_utils.to_categorical(key_all, nb_classes)

            yield sklearn.utils.shuffle(X_train, y_train)

# Parameters
row, col, ch = 160, 320, 1
nb_classes = 3

# compile and train the model using the generator function
train_generator = generator(train_samples, nb_classes, batch_size=128)
validation_generator = generator(validation_samples, nb_classes, batch_size=128)


model = Sequential()
# Preprocess incoming data, centered around zero with small standard deviation 
model.add(Lambda(lambda x: x/255.0 - 0.5, input_shape=(row, col, ch)))
model.add(Cropping2D(cropping=((80,10), (50,20))))
model.add(Convolution2D(24, 5, 5, subsample=(2,2), activation='relu'))
model.add(Convolution2D(36, 5, 5, subsample=(2,2), activation='relu'))
model.add(Convolution2D(48, 5, 5, subsample=(2,2), activation='relu'))
model.add(Convolution2D(64, 3, 3, activation='relu'))
model.add(Convolution2D(64, 3, 3, activation='relu'))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(100))
model.add(Dropout(0.5))
model.add(Dense(10))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit_generator(train_generator, samples_per_epoch= len(train_samples)*2/128,
                    validation_data=validation_generator,
                    nb_val_samples=len(validation_samples)*2/128, nb_epoch=20)
# Save model
model.save('driving_model_grey.h5')

'''
#import os
from keras.models import load_model

model = load_model('driving_model_grey.h5')
#l = []
path = os.listdir()
for i in path:
    img = cv2.imread(i,0)
    img = cv2.resize(img, (320,160))
    img_org = img.copy()
    img = np.expand_dims(img, axis=0)
    img = np.expand_dims(img, axis=3)
    pred = model.predict(img)
    cv2.imshow(str(np.where(pred==np.max(pred))[1][0]), img_org)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    #l.append(np.where(b==np.max(pred))[1][0])
'''
