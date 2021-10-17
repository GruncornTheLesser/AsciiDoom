from Sampler import Sampler1D, Sampler2D
import os
class Colour:
    def __init__(self, r, g, b, bitdepth = 2):
        # we are losing the top 2 numbers of colour which is easily fixed
        # but this looks really clean so ima keep it
        self.r = min(r >> (bitdepth - 2), 6) 
        self.g = min(g >> (bitdepth - 2), 6)
        self.b = min(b >> (bitdepth - 2), 6)

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
        """gets the weird renderer colour encoding"""
        return 16 + self.r * 36 + self.g * 6 + self.b


from PIL import Image
class Texture(Sampler1D):
    """A collection of sampler2Ds at different levels of detail"""
    def __init__(self, mipmaps):
        Sampler1D.__init__(self, mipmaps)

    def GenMipMaps(width, height, mipmap, buffer):
        """Generates a Texture with from an image buffer"""
        mipmap += 1 # 1 mipmap = 2 samplers
        sampler_buffer = [Sampler2D(width, height, buffer)]
        for i in range(1, mipmap):
            sampler_w = width >> i # left shift is same as divide by 2^i
            sampler_h = height >> i
            buffer = []
            for y in range(sampler_h): 
                for x in range(sampler_w):
                    # compress 4 pixels into 1
                    col =  Colour.FromID(sampler_buffer[i - 1][x * 2, y * 2]) 
                    col += Colour.FromID(sampler_buffer[i - 1][x * 2 + 1, y * 2])
                    col += Colour.FromID(sampler_buffer[i - 1][x * 2, y * 2 + 1])
                    col += Colour.FromID(sampler_buffer[i - 1][x * 2 + 1, y * 2 + 1])
                    col //= 4   # average pixels together
                    buffer.append(col.getID())
                    
            sampler_buffer.append(Sampler2D(sampler_w, sampler_h, buffer))
        sampler_buffer.reverse()
        return Texture(sampler_buffer)

    def Load(filepath, mipmap = 0):
        """loads image from local file in the same folder as the script"""
        dir_path = __file__.removesuffix(os.path.basename(__file__))

        """the weird extra long way to access the directory path is because when you run a script the files get copied into
        a different place to run the program. that means the directory doesnt have all the necessary things to run. in this
        case its the textures file. To fix that we get the path to the original file location with '__file__', removesuffix
        its of to get rid of the files name with the path to the original directory folder. then we add the local 'filepath'
        to get the file we want.
        """

        img = Image.open(dir_path + filepath).convert('RGB')
        buffer = []
        for y in range(img.height):
            for x in range(img.width):
                pixel = img.getpixel((x, y)) 
                buffer.append(Colour(pixel[0], pixel[1], pixel[2], 8).getID())

       
        return Texture.GenMipMaps(img.width, img.height, mipmap, buffer)