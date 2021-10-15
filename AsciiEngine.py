import math
from random import randrange
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

MAX_DEPTH = 10




class Camera:
    def __init__(self, posX : float, posY : float, dirX : float, dirY : float, planeX : float, planeY : float):
        self.posX = posX
        self.posY = posY
        self.dirX = dirX
        self.dirY = dirY
        self.planeX = planeX
        self.planeY = planeY

    def Rotate(self, a : float):
        olddirx = self.dirX
        self.dirX = math.cos(a) * self.dirX - math.sin(a) * self.dirY
        self.dirY = math.sin(a) * olddirx + math.cos(a) * self.dirY

        oldplaneX = self.planeX
        self.planeX = math.cos(a) * self.planeX - math.sin(a) * self.planeY
        self.planeY = math.sin(a) * oldplaneX + math.cos(a) * self.planeY


class Player(Camera):
    def __init__(self, posX, posY):
        Camera.__init__(self, posX, posY, -1, 0, 0, 0.66)
        


class Map:
    def __init__(self, width, data):
        self.data = data
        self.width = width
        self.height = int(len(data) / width)

    def __getitem__(self, pos) -> int:
        xi, yi = pos
        if (0 <= xi and xi < self.width and 0 <= yi and yi < self.height):
            return self.data[yi * self.height + xi]
        else:
            return -1

class GradientSampler:
    data = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1[]?-_+~<>i!lI;:,"^`'. """
    def __getitem__(self, index : float) -> str:
        return self.data[min(math.floor(abs(index * len(self.data))), len(self.data) - 1)]

class Game:
    player : Player 
    Grad : GradientSampler
    map : Map
    def __init__(self):
        global screen
        screen.keypad(True)
        screen.nodelay(True)
        
        curses.noecho()
        curses.cbreak()
        
        self.player = Player(3, 3)
        self.map = Map(9, [
            5, 1, 1, 1, 1, 1, 1, 1, 5,
            4, 0, 0, 0, 0, 0, 0, 0, 2,
            4, 0, 0, 0, 0, 0, 0, 0, 2,
            4, 0, 0, 1, 0, 0, 0, 0, 2,
            4, 0, 0, 1, 1, 1, 0, 0, 2,
            4, 0, 0, 1, 0, 0, 0, 0, 2,
            4, 0, 0, 0, 0, 0, 0, 0, 2,
            4, 0, 0, 0, 0, 0, 0, 0, 2,
            5, 3, 3, 3, 3, 3, 3, 3, 5])
        self.Grad = GradientSampler()


    def CastRay(self, posX, posY, dirX, dirY) -> tuple: # return the depth, map value
        
        mapX = int(posX)
        mapY = int(posY)

        if dirX == 0:   deltaX = 1e30
        else:           deltaX = abs(1 / dirX)
        
        if dirY == 0:   deltaY = 1e30
        else:           deltaY = abs(1 / dirY)
        
        if (dirX < 0):  
            stepX = -1
            distX = (posX - mapX) * deltaX
        else:
            stepX = 1
            distX = (mapX + 1.0 - posX) * deltaX
        
        if (dirY < 0):
            stepY = -1
            distY = (posY - mapY) * deltaY
        else:
            stepY = 1
            distY = (mapY + 1.0 - posY) * deltaY
        
        hit = 0

        # dda algorithm
        while not hit: 
            # jump to next map square, either in x-direction, or in y-direction
            northsouth = distX < distY # north south edge or south west edge
            if (northsouth):
                distX += deltaX 
                mapX += stepX
            else:
                distY += deltaY
                mapY += stepY
            
            hit = self.map[mapX, mapY]      
       
        # calculate distance of ray(eucildean gives fish eye)
        if northsouth:  distance = distX - deltaX
        else:           distance = distY - deltaY

        return max(distance, 1e-16), hit

    def Render(self):
        screen.clear()

        for x in range(screenWidth):
            cameraX = 2.0 * x / float(screenWidth) - 1
            rayDirX = self.player.dirX + self.player.planeX * cameraX
            rayDirY = self.player.dirY + self.player.planeY * cameraX

            raydepth, mapvalue = self.CastRay(self.player.posX, self.player.posY, rayDirX, rayDirY)
            
            for y in range(
                int(max((screenHeight - int(screenHeight / raydepth)) / 2, 0)), 
                int(min((screenHeight + int(screenHeight / raydepth)) / 2, screenHeight - 1))):
                
                screen.addch(y, x, ord(self.Grad[raydepth / MAX_DEPTH]))

        screen.addstr(0, 0, str(self.player.posX) + ", " + str(self.player.posY))
        screen.addstr(1, 0, str(self.player.dirX) + ", " + str(self.player.dirY))

    
    def HandleInputs(self):
        ch = screen.getch()

        if ch == ord('q'):
            self.player.Rotate(0.05)
        elif ch == ord('e'):
            self.player.Rotate(-0.05)
        
        elif ch == ord('w'):
            self.player.posX += self.player.dirX * 0.05
            self.player.posY += self.player.dirY * 0.05
        elif ch == ord('s'):
            self.player.posX -= self.player.dirX * 0.05
            self.player.posY -= self.player.dirY * 0.05
        
        elif ch == ord('a'):
            self.player.posX -= self.player.dirY * 0.05
            self.player.posY += self.player.dirX * 0.05
        elif ch == ord('d'):
            self.player.posX += self.player.dirY * 0.05
            self.player.posY -= self.player.dirX * 0.05

        
    def main(self, value): 
        while True:
            self.HandleInputs()
            self.Render()
    
    def Play(self):
        curses.wrapper(self.main)

game = Game()
game.Play()

print("!!!")