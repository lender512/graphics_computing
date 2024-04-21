import numpy as np
import cv2
import math

# Cambiar el brillo de una imagen


def target(img, color):

    img = img.astype(np.float32)
    new_img = np.zeros((img.shape[0], img.shape[1], 3))
    rates = np.max(img, axis=2)
    rates /= 255
    new_img = color * rates[:, :, None]
    new_img = new_img.astype(np.uint8)
    
    return new_img

def replace_color(img, target_color, new_color, tolerance=100):

    img = img.astype(np.float32)
    # bitmap = np.all(img == target_color, axis=2)
    # bitmap = np.all(img >= target_color - tolerance, axis=2) & np.all(img <= target_color + tolerance, axis=2)
    distance = np.linalg.norm(img - target_color, axis=2)
    bitmap = distance < tolerance
    new_img = img
    new_img[bitmap] = new_color
    new_img = new_img.astype(np.uint8)
    # img = new_img
    return new_img

def replace_background(img, background_img, target_color, tolerance=100):
    background_img = cv2.resize(background_img, (img.shape[1], img.shape[0]))
    img = img.astype(np.float32)
    # bitmap = np.all(img == target_color, axis=2)
    # bitmap = np.all(img >= target_color - tolerance, axis=2) & np.all(img <= target_color + tolerance, axis=2)
    distance = np.linalg.norm(img - target_color, axis=2)
    bitmap = distance < tolerance
    new_img = img
    new_img[bitmap] = background_img[bitmap]
    new_img = new_img.astype(np.uint8)
    # img = new_img
    return new_img

def change_color_grid(img, rows, cols):
    rows_step = img.shape[0] // rows
    cols_step = img.shape[1] // cols
    for i in range(0, img.shape[0], rows_step):
        for j in range(0, img.shape[1], cols_step):
            random_color = np.random.randint(0, 255, 3)
            img[i - rows_step:i, j - cols_step:j] = target(img[i - rows_step:i, j - cols_step:j], random_color)
    return img

# img = target(img, np.array([0, 100, 100]))
# img = change_color_grid(img, 10, 10)

bkg = cv2.imread('lab6/503.jpg')
img = cv2.imread('lab6/odin.jpg')

# img = replace_color(img, np.array([67,255,0]), np.array([0, 0, 100]), 100)
img = replace_background(img, bkg, np.array([67,255,0]),  100)
cv2.imshow('image', img)
# cv2.createTrackbar('tolerance', 'image', 0, 255, lambda x: replace_color(img, np.array([67,255,0]), np.array([0, 0, 0]), x))

cv2.waitKey(0)