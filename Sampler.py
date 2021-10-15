import math

class Sampler2D:
    def __init__(self, width, height, buffer):
        self.buffer = buffer
        self.width = width
        self.height = height
        if height * (height - 1) + width - 1 > len(buffer) - 1:
            raise Exception("buffer not long enough")


    def __getitem__(self, pos): # takes normalized floats from 0-1
        xi, yi = pos
        return self.buffer[math.floor(max(min(yi * self.height, self.height), 0)) * self.width + # clamp then expand to length 
                           math.floor(max(min(xi * self.width, self.width - 1), 0))]
    
    def at(self, xi : int, yi : int):
        return self.buffer[yi * self.width + xi]

class Sampler1D:
    def __init__(self, buffer):
        self.width = len(buffer) - 1
        self.buffer = buffer
        
    def __getitem__(self, xi : float) -> str:
        return self.buffer[int(max(min(xi * self.width, self.width - 1), 0))]

    def at(self, xi : int):
        return self.buffer[xi]
