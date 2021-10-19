
"""# sets up windows curses
will pip install windows-curses automatically
contains a Screen class which handles resizing
"""


"""
try:
    from pip._internal import main as _pip_main
except ImportError:
    from pip import main as _pip_main
_pip_main(["install", "windows-curses"])
"""
import curses, os
from PIL import Image

class _Colour:
    def __init__(self, r, g, b, accuracy = 255):
        self.r = int(6 * (r / accuracy))
        self.g = int(6 * (g / accuracy))
        self.b = int(6 * (b / accuracy))

    def FromID(ID): 
        """python doesnt allow multiple constructors so this'll do"""
        ID -= 16        # 0-216
        r = ID // 36     
        ID -= r * 36    # 0-36
        g = ID // 6
        ID -= g * 6     # 0-6
        b = ID
        return _Colour(r, g, b, 6)

    def __iadd__(self, other): 
        return _Colour(self.r + other.r, self.g + other.g, self.b + other.b, 6)
    def __isub__(self, other):
        return _Colour(self.r - other.r, self.g - other.g, self.b - other.b, 6)
    def __imul__(self, other):
        return _Colour(self.r * other, self.g * other, self.b * other, 6)
    def __ifloordiv__(self, other):
        r = self.r // other
        g = self.g // other
        b = self.b // other
        return _Colour(r, g, b, 6)


    def getID(self) -> int:
        """gets the weird renderer colour encoding"""
        return 16 + self.r * 36 + self.g * 6 + self.b

class Texture:
    """A collection of images at different levels of detail"""
    def __init__(self, images):
        self.images = images
        self.closed = False

    def GenMipMaps(image, mipmap):
        """Generates a Texture with from an image buffer"""
        mipmap += 1 # 1 mipmap = 2 samplers
        images = [[]]
        for y in range(len(image)): 
            images[0].append([])
            for x in range(len(image[0])):
                images[0][y].append(_Colour.FromID(image[y][x]).getID())

        for i in range(1, mipmap):
            sampler_w = len(image[0]) >> i # left shift is same as divide by 2^i
            sampler_h = len(image) >> i
            images.append([])
            for y in range(sampler_h): 
                images[i].append([])
                for x in range(sampler_w):
                    # compress 4 pixels into 1
                    col =  _Colour.FromID(images[i - 1][y * 2][x * 2])
                    col += _Colour.FromID(images[i - 1][y * 2][x * 2 + 1])
                    col += _Colour.FromID(images[i - 1][y * 2 + 1][x * 2])
                    col += _Colour.FromID(images[i - 1][y * 2 + 1][x * 2 + 1])
                    col //= 4   # average pixels together
                    images[i][y].append(col.getID())
                
        return Texture(images)
    
    def get_Pixel(self, lineheight : int, x : float, y : float):
        for image in self.images:
            if lineheight >= len(image):
                return image[int(y * len(image))][int(x * len(image[0]))]
        
        return image[int(y * len(image))][int(x * len(image[0]))]

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
        image = []
        for y in range(img.height):
            image.append([])
            for x in range(img.width):
                pixel = img.getpixel((x, y))
                image[y].append(_Colour(pixel[0], pixel[1], pixel[2], 256).getID())

       
        return Texture.GenMipMaps(image, mipmap)

class Window:
    def Refresh(self):
        self.scr.clear()
        self.height, self.width = self.scr.getmaxyx()
        if curses.is_term_resized(self.Height, self.Width):
            curses.resizeterm(self.Height + 1, self.Width + 1)
        return 1

    def SetPixel(self, x, y, color_id):
        self.scr.addch(y, x, ord(' '), curses.color_pair(color_id))

    def Run(self):
        curses.wrapper(self.main)

    def main(self, screen):
        # self.scr should be screen
        self.scr = curses.initscr() # initiate curses
        
        curses.start_color()
        for color_id in range(16, 256):
            curses.init_pair(color_id, 0, color_id) # creates a pairs of black text and the background colour

        self.height, self.width = self.scr.getmaxyx()
        self.scr.keypad(True)
        self.scr.nodelay(True)

        curses.noecho()
        curses.cbreak()


def HandleInputs(wnd, delta = 1):
    """gets the inputs and handles them appropriately"""
    
    event = wnd.scr.getch()  # dequeues an event from the queue 
    while (event != -1):    # while there are events to dequeue
        
        if event == ord('q'):   # rotate right
            wnd.cam.Rotate(0.05)
        
        elif event == ord('e'): # rotate left
            wnd.cam.Rotate(-0.05)
        
        elif event == ord('w'): # move forwards
            wnd.cam.MoveForward(0.05)
            if (wnd.map[int(wnd.cam.posX), int(wnd.cam.posY)] != 0):
                wnd.cam.MoveForward(-0.05) # backwards

        elif event == ord('s'): # move backwards
            wnd.cam.MoveForward(-0.05)
            if (wnd.map[int(wnd.cam.posX), int(wnd.cam.posY)] != 0):
                wnd.cam.MoveForward(0.05)

        elif event == ord('a'): # move left
            wnd.cam.MoveNormal(0.05)
            if (wnd.map[int(wnd.cam.posX), int(wnd.cam.posY)] != 0):
                wnd.cam.MoveNormal(-0.05)
        
        elif event == ord('d'): # move right
            wnd.cam.MoveNormal(-0.05)
            if (wnd.map[int(wnd.cam.posX), int(wnd.cam.posY)] != 0):
                wnd.cam.MoveNormal(0.05)
        
        elif event == ord('g'):
            wnd.cam.posZ += 0.05
            wnd.cam.posZ = max(0, min(wnd.cam.posZ, 1))
        elif event == ord('b'):
            wnd.cam.posZ -= 0.05
            wnd.cam.posZ = max(0, min(wnd.cam.posZ, 1))
        
        elif event == ord('p'):
            exit()

        event = wnd.scr.getch() # dequeue the next event