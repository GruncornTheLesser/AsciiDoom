import math

class Sampler3D:
    def __init__(self, width : int, height : int, depth : int, buffer : list):
        self.buffer = buffer
        self.width = width
        self.height = height
        self.depth = depth
        if depth * height * width > len(buffer):
            raise Exception("buffer not long enough")
    
    def __getitem__(self, pos): # takes normalized floats from 0-1
        xi, yi, zi = pos
        # multiply normalised value then clamp to 0 <= x <= sidelength - 1
        return self.buffer[int(max(min(zi * self.depth, self.depth - 1), 0)) * (self.height * self.width) + 
                           int(max(min(yi * self.height, self.height - 1), 0)) * (self.width) + 
                           int(max(min(xi * self.width, self.width - 1), 0))]
    
    def at(self, xi : int, yi : int, zi : int):
        return self.buffer[zi * self.height * self.width + yi * self.width + xi]

    def inrange(self, xi : int, yi : int, zi : int) -> bool:
        return  0 <= zi and zi < self.depth and \
                0 <= yi and yi < self.height and \
                0 <= xi and xi < self.width
    
class Sampler2D:
    def __init__(self, width, height, buffer):
        self.buffer = buffer
        self.width = width
        self.height = height
        if height * width > len(buffer):
            raise Exception("buffer not long enough")


    def __getitem__(self, pos): # takes normalized floats from 0-1

        xi, yi = pos
        # multiply normalised value then clamp to 0 <= x <= sidelength - 1
        return self.buffer[int(max(min(yi * self.height, self.height - 1), 0)) * (self.width) + 
                           int(max(min(xi * self.width, self.width - 1), 0))]
    
    def at(self, xi : int, yi : int):
        return self.buffer[yi * self.width + xi]
    
    def inrange(self, xi : int, yi : int) -> bool:
        return  0 <= yi and yi < self.height and \
                0 <= xi and xi < self.width

class Sampler1D:
    def __init__(self, buffer):
        self.width = len(buffer) - 1
        self.buffer = buffer
        
    def __getitem__(self, xi : float) -> str:
        return self.buffer[int(max(min(xi * self.width, self.width - 1), 0))]

    def at(self, xi : int):
        return self.buffer[xi]

    def inrange(self, xi : int) -> bool:
        return  0 <= xi and xi < self.width

