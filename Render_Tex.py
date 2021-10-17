from Screen import Screen
from curses import init_pair, color_pair
from RayCast import RayCast
from Camera import Camera
from Map import Map


from Textures import *
from Sampler import Sampler3D


MAX_DEPTH = 4


class ColorPallete(Sampler3D):
    def __init__(self):
        
        # initiates colour pairs

        # this was fun to work out
        # 0-16 : 16 random colours
        # 16-232 : 6x6x6 color cube
        # 232-256 : 24 greyscale gradient
        buffer = []
        for color_id in range(16, 232):
            init_pair(color_id, 0, color_id) # creates a pairs of black text and the background colour
            buffer.append(color_id)

        Sampler3D.__init__(self, 6, 6, 6, buffer)

class Renderer:

    def init(): 
       Renderer.Color_Pallete = ColorPallete()

    def Render(cam : Camera, map : Map):
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
                    raydepth, tex_u = raycast.IntersectData()   # get intersect data
                    break

            lineheight = int(Screen.Height / raydepth)
            start = (Screen.Height - lineheight) // 2   # start = middle minus half line height
            end   = (Screen.Height + lineheight) // 2   # end   = middle plus half line height
            raydepth = 1 - (raydepth / MAX_DEPTH)       # normalized raydepth 0-1
        
            for y in range(max(start, 0), min(end, Screen.Height - 1)): # clamps range
                Screen.scr.addch(y, x, ord(' '), color_pair(BrickWallTexture.at(raydepth).at(tex_u, (y - start) / lineheight)))