from Screen import Screen, curses
from RayCast import RayCast
from Sampler import Sampler3D
from Texture import Texture, Colour

MAX_DEPTH = 8


class ColorPallete(Sampler3D):
    def __init__(self):
        
        # initiates colour pairs

        # this was fun to work out
        # 0-16 : 16 random colours
        # 16-232 : 6x6x6 color cube = 216
        # 232-256 : 24 greyscale gradient
        buffer = []
        for color_id in range(16, 232):
            curses.init_pair(color_id, 0, color_id) # creates a pairs of black text and the background colour
            buffer.append(color_id)

        Sampler3D.__init__(self, 6, 6, 6, buffer)

class Renderer:
    def init(): 
        Renderer.Color_Pallete = ColorPallete()
        Renderer.FloorColour = Colour(50, 150, 130, 8).getID()
        
        # some textures compress much better than others, the smily face one is suprisingly good, but the bricks are awful
        # the mipmap value needs to be chosen with per texture
        Renderer.Textures = [
            Texture.Load('Textures/tex_a.png', 3), 
            Texture.Load('Textures/tex_b.png', 2),
            Texture.Load('Textures/tex_c.png', 2),
            Texture.Load('Textures/tex_d.png', 2),
            Texture.Load('Textures/tex_e.png', 2),
            Texture.Load('Textures/tex_metal_2.png', 2)]



    def Render(cam, map):
        """Draws scene to the terminal"""
        Screen.Refresh()

        for x in range(Screen.Width):
            raycast = RayCast(cam.posX, cam.posY,                                   # send a ray, from player position
                              cam.dirX + cam.planeX * (2 * x / Screen.Width - 1),   # rotate ray relative to the middle of the screen
                              cam.dirY + cam.planeY * (2 * x / Screen.Width - 1))
            while True:
                mapvalue = map[raycast.Step()]                  # iterate raycast along line
                if (mapvalue > 0):                              # if collision with wall
                    raydepth, tex_u = raycast.IntersectData()   # get intersect data
                    break

            lineheight = int(Screen.Height / raydepth)                      # line height relative to the screens height
            start = int(Screen.Height // 2 - lineheight * (cam.height))     # start = middle minus half line height
            end   = int(Screen.Height // 2 + lineheight * (1 - cam.height)) # end   = middle plus half line height
            raydepth = (raydepth / MAX_DEPTH)                               # normalized raydepth 0-1
        
            for y in range(max(start, 0), min(end, Screen.Height - 1)): # clamps range
                Screen.scr.addch(y, x, ord(' '), curses.color_pair(
                    Renderer.Textures[mapvalue - 1]                     # render texture given by map value
                    .Get_Sampler(lineheight)                            # render at this scale (larger distances use shrunk textures)
                    .at_normalized(tex_u, (y - start) / lineheight)))   # render the pixel at the given uv

