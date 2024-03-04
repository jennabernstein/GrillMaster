from . import Animated
from utils import vec, magnitude, scale
import numpy as np

class Mobile(Animated):
    def __init__(self, position, fileName="", scale=1):
        super().__init__(position, fileName, scale)
        self.velocity = vec(0,0)
        self.maxVelocity = 200
    
    def update(self, seconds):
        super().update(seconds)
        if magnitude(self.velocity) > self.maxVelocity:
            self.velocity = scale(self.velocity, self.maxVelocity)
        self.position = tuple(np.array(self.position) + (self.velocity * seconds).astype(int))

