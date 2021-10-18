class Sampler3D:
    """a 3D collection that can be index with a normalized x, y and z"""
    def __init__(self, width : int, height : int, depth : int, buffer : list):
        self.buffer = buffer
        self.width = width
        self.height = height
        self.depth = depth
        if depth * height * width > len(buffer):
            raise Exception("buffer not long enough for height and width provided")
    
    def __getitem__(self, pos):
        """takes un-normalized ints to index directly in sampler buffer"""
        xi, yi, zi = pos
        return self.buffer[zi * self.height * self.width + yi * self.width + xi]
        
    
    def at_normalized(self, xi, yi, zi):
        """takes normalized floats from 0-1 to index in sampler"""
        return self.buffer[int(max(min(zi * self.depth, self.depth - 1), 0)) * (self.height * self.width) + 
                           int(max(min(yi * self.height, self.height - 1), 0)) * (self.width) + 
                           int(max(min(xi * self.width, self.width - 1), 0))]
    
    def at(self, xi : float, yi : float, zi : float):
        """takes un-normalized floats to index in sampler"""
        return self.buffer[int(max(min(zi, self.depth - 1), 0)) * (self.height * self.width) + 
                           int(max(min(yi, self.height - 1), 0)) * (self.width) + 
                           int(max(min(xi, self.width - 1), 0))]

    def inrange(self, xi : int, yi : int, zi : int) -> bool:
        return  0 <= zi and zi < self.depth and \
                0 <= yi and yi < self.height and \
                0 <= xi and xi < self.width
    
class Sampler2D:
    """a 2D collection that can be index with a normalized x and y"""
    def __init__(self, width, height, buffer):
        self.buffer = buffer
        self.width = width
        self.height = height
        if height * width > len(buffer):
            raise Exception("buffer not long enough")


    def __getitem__(self, pos): 
        """takes un-normalized ints to index directly in sampler buffer"""
        xi, yi = pos
        return self.buffer[yi * self.width + xi]
        
    def at_normalized(self, xi : float, yi : float):
        """takes normalized floats from 0-1 to index in sampler"""
        # multiply normalised value then clamp to 0 <= x <= sidelength - 1
        return self.buffer[int(max(min(yi * self.height, self.height - 1), 0)) * (self.width) + 
                           int(max(min(xi * self.width, self.width - 1), 0))]
    
    def at(self, xi : float, yi : float):
        """takes un-normalized floats to index in sampler"""
        return self.buffer[int(max(min(yi, self.height - 1), 0)) * (self.width) + 
                           int(max(min(xi, self.width - 1), 0))]
    
    def inrange(self, xi : int, yi : int) -> bool:
        return  0 <= yi and yi < self.height and \
                0 <= xi and xi < self.width

class Sampler1D:
    """a 1D collection that can be index with a normalized value"""
    def __init__(self, buffer):
        self.width = len(buffer)
        self.buffer = buffer
        
    def __getitem__(self, xi : int):
        """takes un-normalized ints to index directly in sampler buffer"""
        return self.buffer[xi]

    def at_normalized(self, xi : float):
        """takes normalized float from 0-1 to index in sampler"""
        return self.buffer[int(max(min(xi * self.width, self.width - 1), 0))]
    def at(self, xi : float):
        """takes un-normalized float to index in sampler"""
        return self.buffer[int(max(min(xi, self.width - 1), 0))]
    def inrange(self, xi : int) -> bool:
        return  0 <= xi and xi < self.width
