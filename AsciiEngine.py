""" add on export
# pip install windows-curses automatically
try:
    from pip._internal import main as _pip_main
except ImportError:
    from pip import main as _pip_main
_pip_main(["install", "windows-curses"])
"""
from curses import wrapper
from Screen import Screen
from Render_Tex import Renderer # can change to Render_Dep
from Camera import Camera
from Map import Map


class Game:
    
    def __init__(self):
        self.closed = False
        self.cam = Camera(2, 2, -1, 0) # posx, posy, dirx, diry, planex, planey
        self.map = Map("test")

    def HandleInputs(self, screen):
        """
        gets the inputs and handles them appropriately
        """
        event = screen.getch() # refreshes the screen
        while (event != -1):
            if event == ord('q'):
                self.cam.Rotate(0.05)
            
            elif event == ord('e'):
                self.cam.Rotate(-0.05)
            
            elif event == ord('w'): # move forwards
                self.cam.MoveForward(0.05)
                mapx = int(self.cam.posX)
                mapy = int(self.cam.posY)
                if (not self.map.inrange(mapx, mapy) or self.map[mapx, mapy] != 0):
                    self.cam.MoveForward(-0.05) # backwards

            elif event == ord('s'): # move backwards
                self.cam.MoveForward(-0.05)
                mapx = int(self.cam.posX)
                mapy = int(self.cam.posY)
                if (not self.map.inrange(mapx, mapy) or self.map[mapx, mapy] != 0):
                    self.cam.MoveForward(0.05)

            elif event == ord('a'): # move left
                self.cam.MoveNormal(0.05)
                mapx = int(self.cam.posX)
                mapy = int(self.cam.posY)
                if (not self.map.inrange(mapx, mapy) or self.map[mapx, mapy] != 0):
                    self.cam.MoveNormal(-0.05)
            
            elif event == ord('d'): # move right
                self.cam.MoveNormal(-0.05)
                mapx = int(self.cam.posX)
                mapy = int(self.cam.posY)
                if (not self.map.inrange(mapx, mapy) or self.map[mapx, mapy] != 0):
                    self.cam.MoveNormal(0.05)
            
            event = screen.getch()

    def main_depth(self, screen):
        Screen.init()
        Renderer.init() # render requires screen to be initiated
        while not self.closed:
            self.HandleInputs(screen)
            Renderer.Render(self.cam, self.map)
        
        Screen.terminate()
            


    
if __name__ == "__main__":
    game = Game()
    wrapper(game.main_depth)
    


"""
1>python -m cProfile -o <file>.profile AsciiEngine.py
2>python -m pstats <file>.profile
3>pstats <function name>
"""