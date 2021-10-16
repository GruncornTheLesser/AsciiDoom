import math
"""
# pip install windows-curses automatically
try:
    from pip._internal import main as _pip_main
except ImportError:
    from pip import main as _pip_main
_pip_main(["install", "windows-curses"])
"""
import curses
screen = curses.initscr() # initiate curses
screenHeight, screenWidth = screen.getmaxyx()

# decreasing this makes better image quality but lower view distance
MAX_DEPTH = 4

from Textures import *
from RayCast import *
from Camera import *
from Map import *

class ColorPallete(Sampler3D):
    def __init__(self):
        buffer = []
        
        # there are already 16 defined colours
        # then its 6x6x6 rgb color cube
        for i in range(16, 232): # creates a buffer of the html color pallet
            curses.init_pair(i, curses.COLOR_BLACK, i) 
            buffer.append(i)
        
        buffer[0] = 234 # sets black to slightly not black

        Sampler3D.__init__(self, 6, 6, 6, buffer)

class ColorRamp(Sampler1D):
    def __init__(self, accuracy = 1):
        buffer = []
        
        # there are already 16 funky random colours
        # then its 6x6x6 rgb color cube
        # then theres 24 greyscale colors
        for i in range(233, 256, int(1 / accuracy)): # creates a buffer of the html color pallet
            curses.init_pair(i, curses.COLOR_BLACK, i) 
            buffer.append(i)
        
        buffer[0] = 234 # sets black to slightly not black

        Sampler1D.__init__(self, buffer)
    
class Game:
    
    def __init__(self):
        self.closed = False
        self.cam = Camera(2, 2, -1, 0) # posx, posy, dirx, diry, planex, planey
        self.map = Map("test")

    def Render_with_texture(self):
        """
        draws the to the terminal
        """
        screen.clear()

        for x in range(screenWidth):
            raycast = Ray(self.cam.posX, self.cam.posY,                       # send a ray, from player position
                        self.cam.dirX + self.cam.planeX * x / screenWidth,    # rotate ray by value through in camera plane 
                        self.cam.dirY + self.cam.planeY * x / screenWidth) 

            while True:
                mapx, mapy = raycast.Step()             # iterate along line
                if not self.map.inrange(mapx, mapy):    # if not in range, return big depth
                    mapvalue = 0        # collision with 0
                    raydepth = 1e30     # shortish                    
                    tex_u = 0
                    break

                mapvalue = self.map.at(mapx, mapy)
                if (mapvalue != 0):                             # if collision with wall
                    raydepth, tex_u = raycast.IntersectData()   # get intersect data
                    break
                    

            lineheight = int(screenHeight / raydepth)   # '//' is an integer division and '/' is a float division
            start = (screenHeight - lineheight) // 2    # adds half the lineheight from the screen height to find the start
            end =   (screenHeight + lineheight) // 2    # subtracts half the line height from half the screen height to find the end
            
            raydepth = 1 - (raydepth / MAX_DEPTH) # relative raydepth

            for y in range(max(start, 0), min(end, screenHeight - 1)): # makes sure start and end is within the range of the screen
                screen.addch(y, x, ord(' '), curses.color_pair(ColourTextures[mapvalue][tex_u, (y - start) / lineheight]))




    def Render_with_color(self):
        screen.clear()

        for x in range(screenWidth):
            raycast = Ray(self.cam.posX, self.cam.posY,                             # send a ray, from player position
                        self.cam.dirX + self.cam.planeX * (x / screenWidth - 1),    # rotate ray relative to screen x position
                        self.cam.dirY + self.cam.planeY * (x / screenWidth - 1)) 

            while True:
                mapx, mapy = raycast.Step()             # iterate along line
                if not self.map.inrange(mapx, mapy):    # if not in range, return big depth
                    raydepth = 1e30
                    break

                mapvalue = self.map.at(mapx, mapy)
                if (mapvalue != 0):                     # if collision with wall
                    raydepth = raycast.IntersectDepth() # get intersect data
                    break
                    
            
            lineheight = int(screenHeight / raydepth)
            start = (screenHeight - lineheight) // 2
            end =   (screenHeight + lineheight) // 2 
            raydepth = 1 - (raydepth / MAX_DEPTH) # relative raydepth

            for y in range(max(start, 0), min(end, screenHeight - 1)):
                screen.addch(y, x, ord(' '), curses.color_pair(self.colors[raydepth, raydepth, raydepth]))

    #def DrawPixel(self, x, y, char, r, g, b): 

    def HandleInputs(self):
        """
        gets the inputs and handles them appropriately
        """
        event = screen.getch() # refreshes the screen

        # -----------------------------Window events-------------------------------#
        if event == curses.KEY_EXIT: 
            self.closed = True
        
        if event == curses.KEY_RESIZE:
            # update screen height and width on terminal resize
            global screenHeight, screenWidth                
            screenHeight, screenWidth = screen.getmaxyx()

        if event == curses.ALL_MOUSE_EVENTS:
            return


        # -----------------------------Movement events-----------------------------#
        if event == ord('q'):
            self.cam.Rotate(0.05)
        
        elif event == ord('e'):
            self.cam.Rotate(-0.05)
        
        elif event == ord('w'): # move forwards
            self.cam.MoveForward(0.05)
            mapx = int(self.cam.posX)
            mapy = int(self.cam.posY)
            if (not self.map.inrange(mapx, mapy) or self.map.at(mapx, mapy) != 0):
                 self.cam.MoveForward(-0.05) # backwards

        elif event == ord('s'): # move backwards
            self.cam.MoveForward(-0.05)
            mapx = int(self.cam.posX)
            mapy = int(self.cam.posY)
            if (not self.map.inrange(mapx, mapy) or self.map.at(mapx, mapy) != 0):
                 self.cam.MoveForward(0.05)

        elif event == ord('a'): # move left
            self.cam.MoveNormal(0.05)
            mapx = int(self.cam.posX)
            mapy = int(self.cam.posY)
            if (not self.map.inrange(mapx, mapy) or self.map.at(mapx, mapy) != 0):
                self.cam.MoveNormal(-0.05)
        
        elif event == ord('d'): # move right
            self.cam.MoveNormal(-0.05)
            mapx = int(self.cam.posX)
            mapy = int(self.cam.posY)
            if (not self.map.inrange(mapx, mapy) or self.map.at(mapx, mapy) != 0):
                self.cam.MoveNormal(0.05)

    def main(self, _screen):
        """
        call with 'curses.wrapper(<this object>.main)'. sets up the terminal for curses to use and undoes it all when its finished.
        """
        global screen
        screen.keypad(True)
        screen.nodelay(True)
        screen.timeout(0)
        
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        
        # self.colors = ColorRamp(0.5) # 1 dimensional greyscale
        self.colors = ColorPallete() # rgb colors

        while not self.closed:           
            # self.Render_with_color()
            self.Render_with_texture()
            self.HandleInputs()

    
if __name__ == "__main__":
    game = Game()
    curses.wrapper(game.main)