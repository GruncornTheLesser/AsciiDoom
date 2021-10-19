from WrapperPygame import Window, Texture, HandleInputs
from Render_Tex import Render
from Camera import Camera
from Map import Map

class Game(Window):
    Textures = [
        Texture.Load('Textures/tex_a.png', 3), 
        Texture.Load('Textures/tex_b.png', 2),
        Texture.Load('Textures/tex_c.png', 2),
        Texture.Load('Textures/tex_d.png', 2),
        Texture.Load('Textures/tex_e.png', 2),
        Texture.Load('Textures/tex_metal_2.png', 2)]

    def __init__(self):
        Window.__init__(self)
        self.closed = False
        self.cam = Camera(2, 2, 0.5) # posx, posy, dirx, diry, planex, planey
        self.map = Map("test")
   
    def main(self, screen = None):
        Window.main(self, screen)

        while not self.closed:
            delta = Render(self, self.cam, self.map)
            HandleInputs(self, delta)
            

    
if __name__ == "__main__":
    game = Game()
    game.Run()


