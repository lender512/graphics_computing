import cv2
import numpy as np
import math


def apply_border(img, padding, value=0):
    new_img = np.zeros(
        (img.shape[0] + 2*padding, img.shape[1] + 2*padding, img.shape[2]))
    new_img[padding:img.shape[0] + padding,
            padding:img.shape[1] + padding] = img
    new_img[0:padding] = value
    new_img[-padding:] = value
    new_img[:, 0:padding] = value
    new_img[:, -padding:] = value
    return new_img


def apply_kernel(img, kernel):
    size = kernel.shape[0]
    img_size = img.shape[0]
    padding = size // 2
    img = img.astype(np.float32)
    new_img = np.zeros_like(img)
    img = apply_border(img, padding)
    for i in range(0 + size // 2, img_size - size//2 + 1):
        for j in range(0 + size // 2, img_size - size//2 + 1):
            for k in range(img.shape[2]):
                new_img[i, j, k] = np.sum(
                    img[i - size//2:i + size//2+1, j - size//2:j + size//2+1, k] * kernel)
    new_img = np.clip(new_img, 0, 255)
    new_img = new_img.astype(np.uint8)
    return new_img


def create_filter(version, grade):
    if version == 'box':
        return np.ones((grade, grade)) / (grade * grade)


def create_filter_manual(kernel):
    sum = np.sum(kernel)
    if sum == 0:
        return kernel
    return kernel / sum


barlett = np.array([[1, 2, 3, 2, 1],
                    [2, 4, 6, 4, 2],
                    [3, 6, 9, 6, 3],
                    [2, 4, 6, 4, 2],
                    [1, 2, 3, 2, 1]])

gaussian = np.array([[1, 4, 6, 4, 1],
                     [4, 16, 24, 16, 4],
                     [6, 24, 36, 24, 6],
                     [4, 16, 24, 16, 4],
                     [1, 4, 6, 4, 1]])

laplacian = np.array([[0, 0, -1, 0, 0],
                      [0, -1, -2, -1, 0],
                      [-1, -2, 16, -2, -1],
                      [0, -1, -2, -1, 0],
                      [0, 0, -1, 0, 0]])

def to_freq_domain(img):
    return np.fft.fft2(img)

def to_spatial_domain(img):
    return np.fft.ifft2(img)

def high_pass_filter(img, function):
    img = img.astype(np.float32)

    img = to_freq_domain(img)
    img = np.fft.fftshift(img)
    for i in range(img.shape[0]):
        img[i] = np.fft.fftshift(function(img[i]))
    img = np.fft.ifftshift(img)
    img = to_spatial_domain(img)
    img = np.abs(img)
    img = np.clip(img, 0, 255)
    img = img.astype(np.uint8)
    return img

img = cv2.imread('lenna.png', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('lenna.png')
img = img[:, :, None]

# img = apply_kernel(img, create_filter('box', 7))
# img = apply_kernel(img, create_filter_manual(laplacian)).astype(np.float32) + apply_kernel(img, create_filter_manual(gaussian)).astype(np.float32)
# img = np.clip(img, 0, 255)
# img = img.astype(np.uint8)
function = lambda x: math.log(1 + x)
img = high_pass_filter(img, function)
cv2.imwrite('lab8/lenna_freq_high.png', img)
cv2.imshow('img', img)
cv2.waitKey(0)
