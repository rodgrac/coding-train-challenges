import cv2
import numpy as np
import collections
import pyautogui


# Star class: manage star atributes and contain depth update (z) and star draw methods
class Star:
    def __init__(self, width, height) -> None:
        self.w = width
        self.h = height
        
        # Spatial
        self.x = np.random.uniform(-width/2, width/2)
        self.y = np.random.uniform(-height/2, height/2)

        # Depth
        self.z = np.random.uniform(width/2)
        
        # Store previous history of z in queue (len: 5) to be used for line draw
        self.pz = collections.deque(5 * [self.z], 5)
        
        # Initial star radius
        self.r = 2

    def update(self, speed):
        self.pz.append(self.z)
        
        # Reduce z by speed
        self.z -= speed
        
        # Handle boundaries
        if (self.z < 1 or self.sx == 0 or self.sx == self.w or self.sy == 0 or self.sy == self.h):
            self.z = np.random.uniform(self.w/2)
            self.x = np.random.uniform(-self.w/2, self.w/2)
            self.y = np.random.uniform(-self.h/2, self.h/2)
            self.pz = collections.deque(5 * [self.z], 5)
        

    def show(self, space):
        
        # Calculate perspective position of x, y w.r.t z and remap to w, h
        self.sx = int(np.interp(self.x / self.z, [-1, 1], [0, self.w]))
        self.sy = int(np.interp(self.y / self.z, [-1, 1], [0, self.h]))
        
        # Star radius mapping with z
        self.r = int(np.interp(self.z, [0, self.w/2], [3, 0]))
        cv2.circle(space, (self.sx, self.sy), self.r, (255, 255, 255), self.r)
        
        # Calculate previous x,y based on z history and draw lines
        self.psx = int(np.interp(self.x / self.pz[0], [-1, 1], [0, self.w]))
        self.psy = int(np.interp(self.y / self.pz[0], [-1, 1], [0, self.h]))
        
        cv2.line(space, (self.psx, self.psy), (self.sx, self.sy), (255, 255, 255), 1)


# StarField class: Create/manage stars, empty space, assign speed and render the starfield window
class StarField:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

        self.num_stars = 0
        self.stars = []

        # Empty space
        self.space = np.zeros((self.height, self.width), dtype=np.float32)

    def create(self, num_stars):
        self.num_stars = num_stars

        for i in range(self.num_stars):
            self.stars.append(Star(self.width, self.height))

    def draw(self):
        while (True):
            # Get speed from mouseX position
            speed = np.interp(pyautogui.position()[0], [0, self.width], [0, 10])
            for star in self.stars:
                star.show(self.space)
                star.update(speed)

            cv2.imshow('StarField', self.space)

            # Reset space for next frame
            self.space.fill(0)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()


if __name__ == '__main__':
    num_stars = 100
    
    sf = StarField(800, 800)

    sf.create(num_stars)

    sf.draw()
