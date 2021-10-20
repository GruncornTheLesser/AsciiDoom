from Window import Window
from Texture import Texture
import pygame
from pygame.locals import *
from Camera import Camera
from Map import Map

class Game(Window):
    
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
        if pressed_keys[K_r]:   wnd.cam.posZ = max(0, wnd.cam.posZ - 2 * delta)
        if pressed_keys[K_f]:   wnd.cam.posZ = min(1, wnd.cam.posZ + 2 * delta)

        pygame.display.set_caption(str(int(1 / delta)))



    def __init__(self):
        Window.__init__(self)
        self.Textures = [
            Texture.Load('Textures/tex_metal_1.png', 3),
            Texture.Load('Textures/tex_metal_2.png', 3),
            Texture.Load('Textures/tex_brick_1.png', 3),
            Texture.Load('Textures/tex_brick_2.png', 3),
            Texture.Load('Textures/tex_a.png', 2), 
            Texture.Load('Textures/tex_b.png', 3),
            Texture.Load('Textures/tex_c.png', 3),
            Texture.Load('Textures/tex_d.png', 2),
            Texture.Load('Textures/tex_e.png', 2),
            ]
        self.closed = False
        self.cam = Camera(2, 2, 0.5) # posx, posy, dirx, diry
        self.map = Map("test")
    
    def main(self):
        while not self.closed:
            delta = self.Draw_Scene()
            self.HandleInputs(delta)
            

    
if __name__ == "__main__":
    game = Game()
    game.main()
    



