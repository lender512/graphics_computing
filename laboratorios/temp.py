import matplotlib.pyplot as plt
import numpy as np
import heapq

N = 10
WIDTH = 800
HEIGHT = 600

class Event:
    point = None
    t = None
    def __init__(self, point, t):
        self.point = point
        self.t = t

class Node:
    left = None
    right = None
    lp = None
    rp = None
    def __init__(self, lp, rp, left, right):
        self.lp = lp
        self.rp = rp
        self.left = left
        self.right = right
        
class Leaf:
    p = None
    alpha_l = None
    alpha_r = None
    def __init__(self, p):
        self.p = p
        self.alpha_l = p[0]
        self.alpha_r = p[0]

class StatusStructure:
    head = None
    
    def push (self, p):
        if self.head == None:
            self.head = Leaf(p)
        else:
            self.head = Node(p, self.head)
    
    def searchLeftArc(self, p):
        head = self.head
        if self.head == None:
            return None
        else:
            if p == head.lp:
                head = head.left
                while head.right != None:
                    head = head.right
                return head
            elif p == head.rp:
                

points = np.array(np.random.rand(N, 2) * [800, 600], np.int32)
events = [Event(p, 'site') for p in points] 




def draw_parabola(focus, directrix):
    x = np.linspace(0, WIDTH, 1000)
    h, k = (focus[0], (focus[1] + directrix[1]) / 2)
    p = abs(directrix[0] - k)
    y = (x-h)**2 / (4*p) + k
    plt.plot(x, y, color='red')

parabolas = []

def get_max_y(events):
    points = np.array([e.point for e in events])
    max_y = 0
    max_i = 0
    for i, p in enumerate(points):
        if p[1] > max_y:
            max_y = p[1]
            max_i = i
    return max_i, points[max_i]

point_copy = points.copy()

T = StatusStructure()

counter = 0
while len(events) > 0:
    #get minimum value x from points
    i, point = get_max_y(events)
    events = np.delete(events, i, 0)
    
    if events[0].t == 'circle':
        print('circle')
    else:
     if len(T) == 0:
         T.push(point)
     else:
         T.searchLeftArc(point)
         
    
    #####
    
    plt.pause(0.5)
    plt.clf()
    
    plt.xlim(0, WIDTH)
    plt.ylim(0, HEIGHT)

    
    
    sweep_line = point
    plt.axhline(y=sweep_line[1])

    parabolas.append(sweep_line)
    
    for p in point_copy:
        plt.scatter(p[0], p[1], color='blue')

    for p in parabolas:
        draw_parabola(p, (p[0], sweep_line[1]))
        


    

plt.show()