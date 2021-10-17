from Sampler import Sampler2D 

Levels = {
    "empty" : [0, (1, 1)],
    "test" : [
        1, 1, 2, 3, 4, 5, 1, 
        1, 0, 0, 0, 0, 0, 6, 
        2, 0, 0, 0, 0, 0, 7, 
        3, 0, 0, 2, 0, 0, 8, 
        4, 0, 0, 0, 0, 0, 1, 
        5, 0, 0, 0, 0, 0, 1, 
        1, 6, 7, 8, 1, 1, 1, 
        (7, 7)],
}

class Map(Sampler2D):
    def __init__(self, levelid = "test"):
        buffer = Levels[levelid]
        width, height = buffer.pop(len(buffer) - 1)
        Sampler2D.__init__(self, width, height, buffer)