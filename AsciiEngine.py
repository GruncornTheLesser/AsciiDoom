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
from Camera import *
from Map import * 

class Game:
    player : Camera 
    def __init__(self):
        self.closed = False
        self.cam = Camera(2, 2, -1, 0) # posx, posy, dirx, diry, planex, planey
        self.map = Map("test")

    def Render(self):
        """
        draws the to the terminal
        """
        screen.clear()

        for x in range(screenWidth):
            cameraX = x / float(screenWidth) * 2 - 1
            ray = Ray(self.cam.posX, self.cam.posY, 
                        self.cam.dirX + self.cam.planeX * cameraX, 
                        self.cam.dirY + self.cam.planeY * cameraX) 

            while True:
                mapx, mapy = ray.Step()             # iterate along line
                mapvalue = self.map.at(mapx, mapy)
                if (mapvalue != 0):  # if collision with wall
                    break                           

            raydepth, wallx = ray.IntersectData()   # get intersect data

            lineheight = int(screenHeight / raydepth)   # '//' is an integer division and '/' is a float division
            start = (screenHeight - lineheight) // 2    # adds half the lineheight from the screen height to find the start
            end =   (screenHeight + lineheight) // 2    # subtracts half the line height from half the screen height to find the end
            
            for y in range(max(start, 0), min(end, screenHeight - 1)):   
                wally =  (y - start) / lineheight       # gets the ypos in the wall texture 
                screen.addch(y, x, GradientTexture[raydepth * Textures[mapvalue][wallx, wally] / MAX_DEPTH])

    def HandleInputs(self):
        """
        gets the inputs and handles them appropriately
        """
        event = screen.getch() # refreshes the screen

        # -----------------------------Window events-------------------------------#
        # curses events arent mutually excusive with char keys char 
        # # keys = [0... 255]
        # curses = [256...  ]
        if event == curses.KEY_EXIT or event == ord('p'): 
            self.closed = True
        
        if event == curses.KEY_RESIZE:
            # update screen height and width on terminal resize
            global screenHeight, screenWidth                
            screenHeight, screenWidth = screen.getmaxyx()



        # -----------------------------Movement events-----------------------------#
        if event == ord('q'):
            self.cam.Rotate(0.05)
        
        elif event == ord('e'):
            self.cam.Rotate(-0.05)
        
        elif event == ord('w'): # move forwards
            self.cam.MoveForward(0.05)
            if (self.map.at(int(self.cam.posX), int(self.cam.posY)) != 0):
                 self.cam.MoveForward(-0.05) # backwards

        elif event == ord('s'): # move backwards
            self.cam.MoveForward(-0.05)
            if (self.map.at(int(self.cam.posX), int(self.cam.posY)) != 0):
                 self.cam.MoveForward(0.05)

        elif event == ord('a'): # move left
            self.cam.MoveNormal(0.05)
            if (self.map.at(int(self.cam.posX), int(self.cam.posY)) != 0):
                self.cam.MoveNormal(-0.05)
        
        elif event == ord('d'): # move right
            self.cam.MoveNormal(-0.05)
            if (self.map.at(int(self.cam.posX), int(self.cam.posY)) != 0):
                self.cam.MoveNormal(0.05)

    def main(self, _screen):
        """
        call with curses.wrapper(<this object>.main). sets up the terminal for curses to use and undoes it all when its finished
        """
        global screen
        screen.keypad(True)
        screen.nodelay(True)
        screen.timeout(0)
        
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        while not self.closed:
            self.Render()
            self.HandleInputs()

    
if __name__ == "__main__":
    game = Game()
    curses.wrapper(game.main)