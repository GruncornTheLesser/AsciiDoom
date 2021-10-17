import math

class Sampler3D:
    """a 3D collection that can be index with a normalized x, y and z"""
    def __init__(self, width : int, height : int, depth : int, buffer : list):
        self.buffer = buffer
        self.width = width
        self.height = height
        self.depth = depth
        if depth * height * width > len(buffer):
            raise Exception("buffer not long enough")
    
    def __getitem__(self, pos):
        xi, yi, zi = pos
        return self.buffer[zi * self.height * self.width + yi * self.width + xi]
        
    
    def at(self, xi : int, yi : int, zi : int):
        """
        takes normalized floats from 0-1 to index in sampler
        """
        return self.buffer[int(max(min(zi * self.depth, self.depth - 1), 0)) * (self.height * self.width) + 
                           int(max(min(yi * self.height, self.height - 1), 0)) * (self.width) + 
                           int(max(min(xi * self.width, self.width - 1), 0))]
        

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
        xi, yi = pos
        return self.buffer[yi * self.width + xi]
        
    def at(self, xi : int, yi : int):
        """
        takes normalized floats from 0-1 to index in sampler
        """
        # multiply normalised value then clamp to 0 <= x <= sidelength - 1
        return self.buffer[int(max(min(yi * self.height, self.height - 1), 0)) * (self.width) + 
                           int(max(min(xi * self.width, self.width - 1), 0))]
    
    def inrange(self, xi : int, yi : int) -> bool:
        return  0 <= yi and yi < self.height and \
                0 <= xi and xi < self.width

class Sampler1D:
    """a 1D collection that can be index with a normalized value"""
    def __init__(self, buffer):
        self.width = len(buffer)
        self.buffer = buffer
        
    def __getitem__(self, xi : float) -> str:
        return self.buffer[xi]

    def at(self, xi : int):
        return self.buffer[int(max(min(xi * self.width, self.width - 1), 0))]

    def inrange(self, xi : int) -> bool:
        return  0 <= xi and xi < self.width


class Colour:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def FromID(ID): 
        """python doesnt allow multiple constructors so this'll do"""
        ID -= 16        # 0-216
        r = ID // 36     
        ID -= r * 36    # 0-36
        g = ID // 6
        ID -= g * 6     # 0-6
        b = ID
        return Colour(r, g, b)

    def __iadd__(self, other): 
        return Colour(self.r + other.r, self.g + other.g, self.b + other.b)
    def __isub__(self, other):
        return Colour(self.r - other.r, self.g - other.g, self.b - other.b)
    def __imul__(self, other):
        return Colour(self.r * other, self.g * other, self.b * other)
    def __ifloordiv__(self, other):
        r = self.r // other
        g = self.g // other
        b = self.b // other
        return Colour(r, g, b)


    def getID(self) -> int:
        return 16 + self.r * 36 + self.g * 6 + self.b

        

class Texture(Sampler1D):
    """A collection of sampler2Ds at different levels of detail"""
    def __init__(self, buffer):
        Sampler1D.__init__(self, buffer)

    def GenFrom(width, height, mipmap, buffer):        
        sampler_buffer = [Sampler2D(width, height, buffer)]
        for i in range(1, mipmap):
            sampler_w = width >> i
            sampler_h = height >> i
            buffer = []
            for y in range(sampler_h): # left shift divide by 2^i
                for x in range(sampler_w):
                    col =  Colour.FromID(sampler_buffer[i - 1][x * 2, y * 2])
                    col += Colour.FromID(sampler_buffer[i - 1][x * 2 + 1, y * 2])
                    col += Colour.FromID(sampler_buffer[i - 1][x * 2, y * 2 + 1])
                    col += Colour.FromID(sampler_buffer[i - 1][x * 2 + 1, y * 2 + 1])
                    col //= 4   # average colours together
                    buffer.append(col.getID())
                    
            sampler_buffer.append(Sampler2D(sampler_w, sampler_h, buffer))
        sampler_buffer.reverse()
        return Texture(sampler_buffer)
        
