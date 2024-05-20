import numpy as np
import cv2
import time

def lines_intersect(segmentA, segmentB):
    signB_0 = np.sign(np.cross(segmentA[1] - segmentA[0], segmentB[0] - segmentA[0]))
    signB_1 = np.sign(np.cross(segmentA[1] - segmentA[0], segmentB[1] - segmentA[0]))
    if signB_0 == signB_1:
        return False
    signA_0 = np.sign(np.cross(segmentB[1] - segmentB[0], segmentA[0] - segmentB[0]))
    signA_1 = np.sign(np.cross(segmentB[1] - segmentB[0], segmentA[1] - segmentB[0]))
    if signA_0 == signA_1:
        return False
    
    return True

def point_segment_distance(point, segment):
    sign_0 = np.sign(np.dot(segment[1] - segment[0], point - segment[0]))
    sign_1 = np.sign(np.dot(segment[0] - segment[1], point - segment[1]))
    if sign_0 == sign_1:
        print("sign_0 == sign_1")
        return abs(np.cross(segment[1] - segment[0], point - segment[0]) / np.linalg.norm(segment[1] - segment[0]))
    else:
        print("sign_0 != sign_1")
        return min(abs(np.linalg.norm(point - segment[0])), abs(np.linalg.norm(point - segment[1])))
    
def pointIsInTriangle(point, triangle):
    sign_0 = np.sign(np.cross(triangle[1] - triangle[0], point - triangle[0]))
    sign_1 = np.sign(np.cross(triangle[2] - triangle[1], point - triangle[1]))
    sign_2 = np.sign(np.cross(triangle[0] - triangle[2], point - triangle[2]))
    return (sign_0 == sign_1 and sign_1 == sign_2)    
    
    
width = 800
height = 600

img = np.zeros((height, width, 3), np.uint8)
img.fill(255)

def draw_random_segments():
    segmentA = np.array(np.random.rand(2, 2) * [width, height], np.int32)
    segmentB = np.array(np.random.rand(2, 2) * [width, height], np.int32)

    if lines_intersect(segmentA, segmentB):
        cv2.line(img, tuple(segmentA[0]), tuple(segmentA[1]), (0, 0, 0), 2)
        cv2.line(img, tuple(segmentB[0]), tuple(segmentB[1]), (0, 0, 0), 2)
    else:
        cv2.line(img, tuple(segmentA[0]), tuple(segmentA[1]), (0, 0, 255), 2)
        cv2.line(img, tuple(segmentB[0]), tuple(segmentB[1]), (0, 0, 255), 2)

def point_is_inside_polygon(point, polygon):
    pass

def test_line_point():
    random_segment = np.array(np.random.rand(2, 2) * [width, height], np.int32)
    point = np.array([0, 0], np.int32)
    cv2.namedWindow('image')


    cv2.setMouseCallback('image', lambda event, x, y, flags, param: (point.__setitem__(0, x), point.__setitem__(1, y)))
    while True:
        global mouseX,mouseY
        img = np.zeros((height, width, 3), np.uint8)
        img.fill(255)
        cv2.line(img, tuple(random_segment[0]), tuple(random_segment[1]), (0, 0, 0), 2)
        cv2.imshow('image', img)
        key = cv2.waitKey(1)
        if key == 27:
            break
        elif key == ord('r'):
            random_segment = np.array(np.random.rand(2, 2) * [width, height], np.int32)
        
        print(point_segment_distance(point, random_segment))
        cv2.imshow('image', img)
def test_segment_intersection():
    for i in range(1000):
        draw_random_segments()
        cv2.imshow('image', img)
        cv2.waitKey(1)
        time.sleep(0.4)
        img.fill(255)

def test_triangle():
    for i in range(1000):
        triangle = np.array(np.random.rand(3, 2) * [width, height], np.int32)
        for i in range(3):
            cv2.line(img, tuple(triangle[i]), tuple(triangle[(i + 1) % 3]), (0, 0, 0), 2)
        point = np.array(np.random.rand(2) * [width, height], np.int32)
        if pointIsInTriangle(point, triangle):
            cv2.circle(img, tuple(point), 5, (0, 0, 0), -1)
        else:
            cv2.circle(img, tuple(point), 5, (0, 0, 255), -1)
        cv2.imshow('image', img)
        cv2.waitKey(1)
        time.sleep(0.4)
        img.fill(255)

    q
if __name__ == "__main__":
    test_triangle()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
        