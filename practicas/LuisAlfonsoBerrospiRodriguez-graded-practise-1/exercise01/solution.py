import sys
import cv2
import numpy as np
import os
import math
if len(sys.argv) != 4:
    print("Usage: python main.py <image_path> <new_height> <new_width>")
    sys.exit(1)

img_path = sys.argv[1]
new_height = int(sys.argv[2])
new_width = int(sys.argv[3])

def bilinear_interpolation(img, new_height, new_width):
    height, width = img.shape[:2]
    new_img = np.zeros((new_height, new_width, 3), np.uint8)
    for i in range(new_height):
        for j in range(new_width):
            x = i * height / new_height
            y = j * width / new_width
            x1 = math.floor(x)
            y1 = math.floor(y)
            x2 = x1 +1 if x1 + 1 < height else height - 1
            y2 = y1 +1 if y1 + 1 < width else width - 1
            a = x - x1
            b = y - y1
            new_img[i, j] = (1 - a) * (1 - b) * img[x1, y1] + a * (1 - b) * img[x2, y1] + (1 - a) * b * img[x1, y2] + a * b * img[x2, y2]
    return new_img

img = cv2.imread(img_path)
new_img = bilinear_interpolation(img, new_height, new_width)

path = 'exercise01/output/'

new_image_path = os.path.join(path,f"{img_path.split(".")[0]}_{new_height}_{new_width}.png")

print(new_image_path)
cv2.imwrite(new_image_path, new_img)



