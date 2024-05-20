import numpy as np
import cv2

WIDTH = 800
HEIGHT = 600

N = 100

points = np.array(np.random.rand(N, 2) * [WIDTH, HEIGHT], np.int32)


def jarvis_martch(points):
    most_left = np.argmin(points[:, 0])
    #sort clockwise
    hull = [most_left]
    while True:
        end = hull[-1]
        next = (end + 1) % N
        for i in range(N):
            if np.cross(points[next] - points[end], points[i] - points[end]) < 0:
                next = i
        if next == most_left:
            break
        hull.append(next)
        
    return hull
    

def graham_scan(points):
    most_left = np.argmin(points[:, 0])
    #sort clockwise
    other_points = np.delete(points, most_left, 0)
    other_points = sorted(other_points, key=lambda x: np.arctan2(x[1] - points[most_left][1], x[0] - points[most_left][0]))
    stack = [points[most_left]]
    for point in other_points:
        while len(stack) > 1 and np.cross(stack[-1] - stack[-2], point - stack[-2]) < 0:
            stack.pop()
        stack.append(point)
    return stack
        


def monotone_chain(points):
    points = sorted(points, key=lambda x: (x[0], -x[1]))
    lower = []
    upper = []
    for point in points:
        while len(lower) > 1 and np.cross(lower[-1] - lower[-2], point - lower[-2]) < 0:
            lower.pop()
        lower.append(point)
    for point in reversed(points):
        while len(upper) > 1 and np.cross(upper[-1] - upper[-2], point - upper[-2]) < 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]

# hull = graham_scan(points)
hull = monotone_chain(points)

while True:
    img = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
    img.fill(255)
    
    for point in points:
        cv2.circle(img, point, 3, (0, 0, 255), -1)
        
    for i in range(len(hull)):
        cv2.line(img, hull[i], hull[(i + 1) % len(hull)], (0, 255, 0), 2)
        
        
    
    cv2.imshow('image', img)
    if cv2.waitKey(ord('q')) == 113:
        break