import pygame
from pygame.locals import *

from RayCast import RayCast

   

class Window:
    def __init__(self, title = "doom", bkg = (0, 0, 0), canvas_size = (100, 75), screen_size = (800, 600)): # singleton
        self.closed = False
        
        self.background = bkg

        self.title = title
        pygame.display.set_caption(title)

        self.width, self.height = canvas_size
        self.canvas = pygame.Surface(canvas_size) 

        self.screenwidth, self.screenheight = screen_size
        self.screen = pygame.display.set_mode(screen_size)

        self.clock = pygame.time.Clock()

    def Refresh(self):
        self.screen.blit(pygame.transform.scale(self.canvas, (self.screenwidth, self.screenheight)), (0, 0))
        pygame.display.update()
        self.canvas.fill(self.background)
        return self.clock.tick() / 1000

    def SetPixel(self, x, y, colour):
        self.canvas.set_at((x, y), colour)

    def Draw_Wall(self, Tex_ID, x, intersectdata):
        depth, u = intersectdata
        lineheight = int(self.height / depth)

        for image in self.Textures[Tex_ID].images:
            if lineheight >= image.get_height():
                break
        
        self.canvas.blit(pygame.transform.scale(image.subsurface((u * image.get_width(), 0, 1, image.get_height())), (1, lineheight)), (x, int(self.height // 2 - lineheight * (self.cam.posZ))))
    
    def Draw_Scene(self):
        
        for x in range(self.width):
            raycast = RayCast(self.cam.posX, self.cam.posY,                 # send a ray, from player position
                self.cam.dirX + self.cam.planeX * (2 * x / self.width - 1), # rotate ray relative to the middle of the screen
                self.cam.dirY + self.cam.planeY * (2 * x / self.width - 1))
            
            for i in range(20):
                mapvalue = self.map[raycast.Step()] # iterate raycast along line
                if (mapvalue > 0):                  # if collision with wall
                    self.Draw_Wall(0, x, raycast.IntersectData())
                    break
                
        return self.Refresh()
            

def HandleInputs(wnd, delta = 1):
    for event in pygame.event.get():    
        if event.type == QUIT:
            pygame.quit()
            exit()

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_q]:   wnd.cam.Rotate(2 * delta)
    if pressed_keys[K_e]:   wnd.cam.Rotate(-2 * delta)

    if pressed_keys[K_w]:   wnd.cam.MoveForward(2 * delta)
    if pressed_keys[K_a]:   wnd.cam.MoveNormal(2 * delta)
    if pressed_keys[K_s]:   wnd.cam.MoveForward(-2 * delta)
    if pressed_keys[K_d]:   wnd.cam.MoveNormal(-2 * delta)

    if pressed_keys[K_r]:   wnd.cam.posZ -= 2 * delta
    if pressed_keys[K_f]:   wnd.cam.posZ += 2 * delta

    pygame.display.set_caption(str(int(1 / delta)))



