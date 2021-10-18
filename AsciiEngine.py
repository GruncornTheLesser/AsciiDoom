from Render_Dep import Renderer, Screen
from Camera import Camera
from Map import Map

class Game:
    def __init__(self):
        self.closed = False
        self.cam = Camera(2, 2, -1, 0) # posx, posy, dirx, diry, planex, planey
        self.map = Map("test")

    def HandleInputs(self, screen):
        """gets the inputs and handles them appropriately"""
        
        event = screen.getch()  # dequeues an event from the queue 
        while (event != -1):    # while there are events to dequeue
            
            if event == ord('q'):   # rotate right
                self.cam.Rotate(0.05)
            
            elif event == ord('e'): # rotate left
                self.cam.Rotate(-0.05)
            
            elif event == ord('w'): # move forwards
                self.cam.MoveForward(0.05)
                if (self.map[int(self.cam.posX), int(self.cam.posY)] != 0):
                    self.cam.MoveForward(-0.05) # backwards

            elif event == ord('s'): # move backwards
                self.cam.MoveForward(-0.05)
                if (self.map[int(self.cam.posX), int(self.cam.posY)] != 0):
                    self.cam.MoveForward(0.05)

            elif event == ord('a'): # move left
                self.cam.MoveNormal(0.05)
                if (self.map[int(self.cam.posX), int(self.cam.posY)] != 0):
                    self.cam.MoveNormal(-0.05)
            
            elif event == ord('d'): # move right
                self.cam.MoveNormal(-0.05)
                if (self.map[int(self.cam.posX), int(self.cam.posY)] != 0):
                    self.cam.MoveNormal(0.05)
            elif event == ord('g'):
                self.cam.height += 0.05
            elif event == ord('b'):
                self.cam.height -= 0.05
            
            event = screen.getch() # dequeue the next event

    def main(self, screen):
        Renderer.init() # renderer is a singleton, it so it only needs to be intiated once and itll draw into the terminal
        while not self.closed:
            self.HandleInputs(screen)
            Renderer.Render(self.cam, self.map)
        
        Screen.terminate()
    
if __name__ == "__main__":
    game = Game()
    Screen.init()
    Screen.RunProgram(game.main)


"""
1>python -m cProfile -o <file>.profile AsciiEngine.py
2>python -m pstats <file>.profile
3>pstats <function name>
"""
