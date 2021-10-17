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
        # 16-232 : 6x6x6 color cube
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
        SmileyFaceTexture = Texture.GenMipMaps(9, 9, 2, [
            227, 227, 227, 227, 227, 227, 227, 227, 227, 
            227, 227, 195, 195, 227, 195, 195, 227, 227, 
            227, 227, 195, 16,  227, 16,  195, 227, 227, 
            227, 227, 195, 16,  227, 16,  195, 227, 227, 
            227, 227, 227, 227, 227, 227, 227, 227, 227, 
            227, 227, 227, 227, 227, 227, 227, 227, 227, 
            227, 16,  227, 227, 227, 227, 227, 16,  227, 
            227, 16,  16,  16,  16,  16,  16,  16,  227, 
            227, 227, 227, 227, 227, 227, 227, 227, 227]
            )
        BrickWallTexture = Texture.GenMipMaps(16, 16, 2, [
            60,  60,  60,  16,  60,  60,  60,  60,  60,  60,  60,  16,  60,  60,  60,  60,  
            60,  60,  60,  16,  60,  60,  60,  60,  60,  60,  60,  16,  60,  60,  60,  60,  
            60,  60,  60,  16,  60,  60,  60,  60,  60,  60,  60,  16,  60,  60,  60,  60,  
            16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  
            60,  60,  60,  60,  60,  60,  60,  16,  60,  60,  60,  60,  60,  60,  60,  16,  
            60,  60,  60,  60,  60,  60,  60,  16,  60,  60,  60,  60,  60,  60,  60,  16,  
            60,  60,  60,  60,  60,  60,  60,  16,  60,  60,  60,  60,  60,  60,  60,  16,  
            16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  
            60,  60,  60,  16,  60,  60,  60,  60,  60,  60,  60,  16,  60,  60,  60,  60,  
            60,  60,  60,  16,  60,  60,  60,  60,  60,  60,  60,  16,  60,  60,  60,  60,  
            60,  60,  60,  16,  60,  60,  60,  60,  60,  60,  60,  16,  60,  60,  60,  60,  
            16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  
            60,  60,  60,  60,  60,  60,  60,  16,  60,  60,  60,  60,  60,  60,  60,  16,  
            60,  60,  60,  60,  60,  60,  60,  16,  60,  60,  60,  60,  60,  60,  60,  16,  
            60,  60,  60,  60,  60,  60,  60,  16,  60,  60,  60,  60,  60,  60,  60,  16,  
            16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16,  16])
        Renderer.Textures = [
            BrickWallTexture, 
            SmileyFaceTexture, 
            Texture.Load('Textures/tex_bricks_1.png', 3), 
            Texture.Load('Textures/tex_bricks_2.png', 3),
            Texture.Load('Textures/tex_stones_1.png', 3),
            Texture.Load('Textures/tex_stones_2.png', 3),
            Texture.Load('Textures/tex_metal_1.png', 3),
            Texture.Load('Textures/tex_metal_2.png', 3)]



    def Render(cam, map):
        """
        Draws to the terminal with the distance from the camera to the wall
        """
        Screen.Refresh()

        for y in range(Screen.Height // 2, Screen.Height):
            Screen.scr.addstr(y, 1, ' ' * (Screen.Width - 2), curses.color_pair(Renderer.FloorColour))

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
                Screen.scr.addch(y, x, ord(' '), curses.color_pair(Renderer.Textures[mapvalue - 1].at(raydepth).at(tex_u, (y - start) / lineheight)))
                pass