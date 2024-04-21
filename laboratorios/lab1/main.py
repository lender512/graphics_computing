import numpy as np
import cv2

img = cv2.imread('image.jpg', 0)

array = np.array(img)

length = len(array)
width = len(array[0])

new_lengh = 100
new_width = 100

new_array = np.zeros((new_lengh, new_width))

print(array)


def interpolation(a, b, c_x):
    a_x = a[0]
    a_y = a[1]
    b_x = b[0]
    b_y = b[1]

    return (c_x, a_y + (b_y - a_y) * (c_x - a_x) / (b_x - a_x))


def get_normal_coordinate(lenght, width, x, y):
    return (x / (width-1), y / (lenght-1))


def get_neighbours(x, lenght):
    space_x = 1/(lenght-1)
    return (int((x//space_x)), int((x//space_x+1)))

for i in range(0, new_lengh):
    for j in range(0, new_width):
        x,y = get_normal_coordinate(new_lengh, new_width, i, j)
        neighbours_x = get_neighbours(x, length)
        neighbours_y = get_neighbours(y, width)
        point_a = (neighbours_x[0], neighbours_y[0])
        point_b = (neighbours_x[1], neighbours_y[0])
        point_c = (neighbours_x[0], neighbours_y[1])
        point_d = (neighbours_x[1], neighbours_y[1])
        
        point_list = [point_a, point_b, point_c, point_d]
        
        try:   

            # a = interpolation((point_a[0], array[point_a[0]][point_a[1]]), (point_b[0], array[point_b[0]][point_b[1]]), x)
            # b = interpolation((point_c[0], array[point_c[0]][point_c[1]]), (point_d[0], array[point_d[0]][point_d[1]]), x)
            # c = interpolation(a, b, normal_a[1])
            mean = 0
            for point in point_list:
                mean += array[point[0]][point[1]]
            mean = mean/4
            new_array[i][j] = mean
        except:
            new_array[i][j] = 255

# output image
cv2.imshow('image', new_array)
cv2.waitKey(0)
