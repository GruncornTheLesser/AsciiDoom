import curses
from Screen import Screen, curses
from Sampler import Sampler1D
from RayCast import RayCast
MAX_DEPTH = 4

class ColorRamp(Sampler1D):
    def __init__(self, precision = 1):
        buffer = []
        
        # initiates colour pairs

        # this was fun to work out
        # 0-16 : 16 random colours
        # 16-232 : 6x6x6 color cube
        # 232-256 : 24 greyscale gradient

        # skips absolute black -> it was very dark
        # there are three blacks that defined by this encoding: 0, 16, 232 -> why?
        for color_id in range(232 + 1, 256, int(1 / precision)): # creates a buffer of the html color pallet
            curses.init_pair(color_id, 0, color_id)                     # creates a pairs of black text and the background colour
            buffer.append(color_id)

        Sampler1D.__init__(self, buffer)

class Renderer:
    def init(): # singleton
        Renderer.Color_Ramp = ColorRamp(0.5) # requires curses to be setup

    def Render(cam, map): 
        """
        Draws to the terminal with the distance from the camera to the wall
        """
        Screen.Refresh()
        for x in range(Screen.Width):
            raycast = RayCast(cam.posX, cam.posY,                                   # send a ray, from player position
                              cam.dirX + cam.planeX * (2 * x / Screen.Width - 1),   # rotate ray relative to the middle of the screen
                              cam.dirY + cam.planeY * (2 * x / Screen.Width - 1))

            while True:
                mapvalue = map[raycast.Step()]          # iterate raycast along line
                if (mapvalue > 0):                      # if collision with wall
                    raydepth = raycast.IntersectDepth() # get intersect data
                    break                               

            lineheight = int(Screen.Height / raydepth)
            for y in range(max((Screen.Height - lineheight) // 2, 0),                   # start = middle minus half line height
                           min((Screen.Height + lineheight) // 2, Screen.Height - 1)):  # end   = middle plus half line height
                Screen.scr.addch(y, x, ord(' '), curses.color_pair(Renderer.Color_Ramp.at(1 - (raydepth / MAX_DEPTH))))