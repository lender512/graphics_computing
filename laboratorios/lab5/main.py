import numpy as np
import cv2
import math

# Cambiar el brillo de una imagen

img_base = cv2.imread('lab5/image.jpg')
img = cv2.imread('lab5/image.jpg')

def change_brightness(alpha):
    global img, img_base
    img = img_base
    img = img.astype(np.float32)
    img = np.clip(img + alpha, 0, 255)
    img = img.astype(np.uint8)
    # img = 
    # return img

def change_contrast(contrast_factor):
    contrast_factor /= 255
    global img, img_base
    img = img_base
    img = img.astype(np.float32)
    min_intensity = np.min(img)
    max_intensity = np.max(img)

    min_intensity = min_intensity + (max_intensity - min_intensity) * (contrast_factor)
    max_intensity = max_intensity - (max_intensity - min_intensity) * (contrast_factor)

    img = ((img - min_intensity) / (max_intensity - min_intensity)) * 255

    img = np.clip(img, 0, 255)
    img = img.astype(np.uint8)
    
        

def onTrackbarChange(val):
    alpha = int((val-50)/100*127)
    # change_brightness(alpha)
    change_contrast(alpha)
    cv2.imshow('image', img)
                

cv2.namedWindow('image')

cv2.createTrackbar('Brightness', 'image', 50, 100, lambda x: onTrackbarChange(x))
#above with text input




cv2.imshow('image', img)
cv2.waitKey(0)
