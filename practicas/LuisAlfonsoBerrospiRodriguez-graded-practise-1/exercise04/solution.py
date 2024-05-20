import numpy as np
import cv2
import math
import sys 
# Cambiar el brillo de una imagen

img_path = img_path = sys.argv[1] if len(sys.argv) > 1 else 'lenna.png'
final_img_path = 'exercise04/output/lenna-colorscale.png'

def target(img, target_img):

    img = img.astype(np.float32)
    new_img = np.zeros((img.shape[0], img.shape[1], 3))
    rates = np.max(img, axis=2)
    rates /= 255
    new_img = target_img * rates[:, :, None]
    new_img = new_img.astype(np.uint8)
    
    return new_img

img = cv2.imread(img_path)
widh, height = img.shape[:2]
target_img = np.zeros((widh, height, 3), np.uint8)
center = (widh // 2, height // 2)
radius = widh // 2
for i in range(widh):
    for j in range(height):
        if math.sqrt((i - center[0])**2 + (j - center[1])**2) < radius:
            target_img[i, j] = [255, 0, 0]


img = target(img, target_img)
cv2.imwrite(final_img_path, img)