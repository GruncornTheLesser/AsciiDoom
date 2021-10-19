import pygame
from pygame.locals import *

class Texture:
    """A collection of images at different levels of detail"""
    def __init__(self, images):
        self.images = images
        self.closed = False

    def GenMipMaps(image : pygame.Surface, mipmaps : int):
        """Generates a Texture with from an image buffer"""
        images = [image]
        for i in range(mipmaps):
            images.append(pygame.transform.smoothscale(images[i], (images[i].get_width() >> i, images[i].get_height() >> i)))

                
        return Texture(images)
    def Load(filepath, mipmaps = 0):
        image = pygame.image.load("Textures/tex_stones_2.png")
        return Texture.GenMipMaps(image, mipmaps)

    def get_Pixel(self, lineheight : int, u : float, v : float):
        for i in range(len(self.images)):
            if lineheight >= self.images[i].get_height():
                break
        return self.images[i].get_at((
            int(u * (self.images[i].get_width() - 1)), 
            int(v * (self.images[i].get_height() - 1))))

    

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

    def main(self, screen = None):
        pass

    def Run(self):
        self.main(None)
            




def HandleInputs(wnd, delta = 1):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_q]:
        wnd.cam.Rotate(2 * delta)
    if pressed_keys[K_e]:
        wnd.cam.Rotate(-2 * delta)
    if pressed_keys[K_w]:
        wnd.cam.MoveForward(2 * delta)
    if pressed_keys[K_a]:
        wnd.cam.MoveNormal(2 * delta)
    if pressed_keys[K_s]:
        wnd.cam.MoveForward(-2 * delta)
    if pressed_keys[K_d]:
        wnd.cam.MoveNormal(-2 * delta)
    if pressed_keys[K_r]:
        wnd.cam.posZ -= 2 * delta
    if pressed_keys[K_f]:
        wnd.cam.posZ += 2 * delta