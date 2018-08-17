# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 21:12:34 2018

@author: Jannis
"""
import cv2
import numpy as np
import sys
import zxing # for decode qr_code; see sources


def read_qr_code(image, display = True):
            
    crop_img = img.copy()[600:1100, :500, :]
    crop_img = cv2.resize(crop_img, (500,500))
    
    row, col = crop_img.shape[:2]    
    
    M = cv2.getRotationMatrix2D((col/2,row/2),310,1)
    crop_img = cv2.warpAffine(crop_img,M,(col,row))
            
    new = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    new[new>95] = 255
    new[new<=95] = 0
    new = cv2.dilate(new, None, iterations=11)
    
    mask = np.zeros_like(new)
    _,contours, _= cv2.findContours(new,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #perimeter = cv2.arcLength(cnt,True)
        x,y,w,h = cv2.boundingRect(cnt)
        if abs(w-h) < 100 and area > 5000 and x+y != 0 and y+h < row and x+w < col:
             cv2.fillPoly(mask, pts =[cnt], color=(255,255,255))
             cv2.rectangle(new,(x,y),(x+w,y+h),(255,255,255),2)
      
    crop_img[mask==0] = 0 
    #crop_img = crop_img[y:y+h,x:w+x]
        
    cv2.imwrite('detected_qr_code.jpg', crop_img)
    if display:
        cv2.imshow('crop', crop_img)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
                
    reader = zxing.BarCodeReader()
    barcode = reader.decode('detected_qr_code.jpg')
    barrier_address = barcode.raw
    
    return barrier_address
    
if __name__ == "__main__":    
    display = int(sys.argv[1])
    img_name = 'qr_img_barrier.jpg'
    img = cv2.imread(img_name)
    barrier_address = read_qr_code(img, display)
    
    print('The address is:', barrier_address)