import sys
import cv2
import numpy as np
import os
import math
import time
WIDTH = 800
HEIGHT = 400

def get_random_color():
    return (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))

class ball:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.color = get_random_color()
        self.mass = r**3*3.14*4/3

    def draw(self, img):
        cv2.circle(img, (round(self.x), round(self.y)), self.r, self.color, -1)
        
    def set_speed(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def update (self):
        self.x += self.dx
        self.x = self.x
        self.y += self.dy
        self.y = self.y
        
        if self.x - self.r <= 0:
            self.dx = abs(self.dx)
        if self.x + self.r >= WIDTH:
            self.dx = -abs(self.dx)
        if self.y - self.r <= 0:
            self.dy = abs(self.dy)
        if self.y + self.r >= HEIGHT:
            self.dy = -abs(self.dx)
            
        for other in balls:
            if other != self:
                if (self.x - other.x)**2 + (self.y - other.y)**2 <= (self.r + other.r)**2:
                    #calculate the new speed perfect elastic collision proporsional to the mass
                    mass_self = self.mass
                    mass_other = other.mass
                    self.dx, other.dx = other.dx, self.dx
                    self.dy, other.dy = other.dy, self.dy
                    self.dx *= mass_other/mass_self
                    self.dy *= mass_other/mass_self
                    other.dx *= mass_self/mass_other
                    other.dy *= mass_self/mass_other
                    #move the balls so they don't overlap
                    while (self.x - other.x)**2 + (self.y - other.y)**2 <= (self.r + other.r)**2:
                        self.x += self.dx
                        self.y += self.dy
                        other.x += other.dx
                        other.y += other.dy
                    
                    self.color = get_random_color()
                    
    
n_balls = 100
min_r = 5
max_r = 10
min_speed = -2
max_speed = 2
        
#create random balls
balls = [ball(np.random.randint(0, WIDTH), np.random.randint(0, HEIGHT), np.random.randint(min_r, max_r)) for i in range(n_balls)]

def draw_balls(img, balls):
    for b in balls:
        b.draw(img)
        
def move_balls(balls, dx, dy):
    for b in balls:
        b.move(dx, dy)
        
        
def main():
    img = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
    for b in balls:
        #random float
        b.set_speed(np.random.uniform(min_speed, max_speed), np.random.uniform(min_speed, max_speed))
    while True:
        img.fill(0)
        draw_balls(img, balls)
        cv2.imshow('image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        for b in balls:
            b.update()
        # time.sleep(0.01)
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()

