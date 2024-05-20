import cv2
import numpy as np
import math
import sys

def apply_border(img, padding, value=0):
    if len(img.shape) == 2:
        new_img = np.zeros(
            (img.shape[0] + 2*padding, img.shape[1] + 2*padding))
        new_img[padding:img.shape[0] + padding,
                padding:img.shape[1] + padding] = img
        new_img[0:padding] = value
        new_img[-padding:] = value
        new_img[:, 0:padding] = value
        new_img[:, -padding:] = value
        return new_img

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
    if len(img.shape) == 2:
        for i in range(0 + size // 2, img_size - size//2):
            for j in range(0 + size // 2, img_size - size//2):
                new_img[i, j] = np.sum(
                    img[i - size//2:i + size//2+1, j - size//2:j + size//2+1] * kernel)
        new_img = np.clip(new_img, 0, 255)
        new_img = new_img.astype(np.uint8)
        return new_img

    for i in range(0 + size // 2, img_size - size//2):
        for j in range(0 + size // 2, img_size - size//2):
            for k in range(img.shape[2]):
                new_img[i, j, k] = np.sum(
                    img[i - size//2:i + size//2+1, j - size//2:j + size//2+1, k] * kernel)
    new_img = np.clip(new_img, 0, 255)
    new_img = new_img.astype(np.uint8)
    return new_img


def create_filter_box(grade):
    return np.ones((grade, grade)) / (grade * grade)


def create_filter_manual(kernel):
    sum = np.sum(kernel)
    if sum == 0:
        return kernel
    return kernel / sum


def create_barlett(grade):
    vector = np.zeros(grade)
    for i in range(grade):
        if i < grade // 2:
            vector[i] = i + 1
        else:
            vector[i] = grade - i
    matrix = np.outer(vector, vector)
    return matrix / np.sum(matrix)


def create_gaussian(grade):
    raw = np.zeros((grade, grade))
    for i in range(grade):
        for j in range(grade):
            raw[i, j] = np.exp(-((i - grade // 2) * 2 + (j - grade // 2) * 2) / (2 * (grade // 2) ** 2))
    return raw / np.sum(raw)
    
    


gaussian = np.array([[1, 4, 6, 4, 1],
                     [4, 16, 24, 16, 4],
                     [6, 24, 36, 24, 6],
                     [4, 16, 24, 16, 4],
                     [1, 4, 6, 4, 1]])

laplacian = {'3': np.array([[0, -1, 0],
                            [-1, 4, -1],
                            [0, -1, 0]]),
             '5': np.array([[0, 0, -1, 0, 0],
                            [0, -1, -2, -1, 0],
                            [-1, -2, 16, -2, -1],
                            [0, -1, -2, -1, 0],
                            [0, 0, -1, 0, 0]])}


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


img_path = sys.argv[1] if len(sys.argv) > 1 else 'lenna.png'

columns = ['original', '3x3', '5x5', '7x7', '9x9', '11x11',
           '13x13', '15x15', '17x17', '19x19', '21x21', '23x23', '25x25']
rows = ['box-grayscale', 'box-rgb', 'barlett-rgb', 'barlett-grayscale',
        'gaussian-rgb', 'gaussian-grayscale', 'laplacian-rgb', 'laplacian-grayscale']

html = '<table border="1">'

for row in rows:
    html += '<tr>'
    html += f'<td>{row}</td>'
    for column in columns:
        
        
        size = int(column.split('x')[0]) if column != 'original' else 0
        if column == 'original':
            img = cv2.imread(img_path)
            cv2.imwrite(f'exercise05/output/{row}-{column}.png', img)
            html += f'<td><img src="{row}-{column}.png"></td>'
            continue
        if 'grayscale' in row:
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        else:
            img = cv2.imread(img_path)
        if 'box' in row:
            img = apply_kernel(img, create_filter_box(size))
        elif 'barlett' in row:
            img = apply_kernel(img, create_barlett(size))
        elif 'gaussian' in row:
            img = apply_kernel(img, create_gaussian(size))
        elif 'laplacian' in row:
            if str(size) in laplacian:
                img = apply_kernel(img, laplacian[str(size)])
            else:
                img = np.zeros((img.shape[0], img.shape[1], 3))
        cv2.imwrite(f'exercise05/output/{row}-{column}.png', img)
        html += f'<td><img src="{row}-{column}.png"></td>'
    html += '</tr>'

html += '</table>'

with open('exercise05/output/table.html', 'w+') as file:
    file.write(html)
