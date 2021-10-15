
from Textures import *

class Map(Sampler2D):
    Levels = {
        "empty" : [0, (1, 1)],
        "test" : [
            1, 1, 1, 1, 1, 1, 1, 
            1, 0, 0, 0, 0, 0, 1, 
            1, 0, 0, 0, 0, 0, 1, 
            1, 0, 0, 1, 0, 0, 1, 
            1, 0, 0, 0, 0, 0, 1, 
            1, 0, 0, 0, 0, 0, 1, 
            1, 1, 1, 1, 1, 1, 1, 
            (7, 7)],
    }

    def __init__(self, levelid = "test"):
        buffer = self.Levels[levelid]
        width, height = buffer.pop(len(buffer) - 1)
        Sampler2D.__init__(self, width, height, buffer)





class Ray:
    """
    A projection from a point along a direction vector.
    Used to find the collisions in an axis aligned grid.
    """
    # an enum -> this is how your supposed to do it apparently??? 
    class WallSide: 
        Undetermined = -1 
        EastWest = 0
        NorthSouth = 1
    
    def __init__(self, posX, posY, dirX, dirY):
        self.posX = posX
        self.posY = posY
        
        self.dirX = dirX
        self.dirY = dirY

        self.mapX = int(posX)
        self.mapY = int(posY)

        self.deltaX = abs(1 / dirX) 
        self.deltaY = abs(1 / dirY)

        if (dirX < 0):                              # if ray direction left
            self.stepX = -1
            self.distX = (posX - self.mapX) * self.deltaX
        else:                                       # if ray direction right
            self.stepX = 1
            self.distX = (self.mapX + 1.0 - posX) * self.deltaX
        

        if (dirY < 0):                              # if ray direction down
            self.stepY = -1
            self.distY = (posY - self.mapY) * self.deltaY
        else:                                       # if ray direction up
            self.stepY = 1
            self.distY = (self.mapY + 1.0 - posY) * self.deltaY

        self.Wall = Ray.WallSide.Undetermined
        

    def Step(self):
        if (self.distX < self.distY):   # north south edge
            self.mapX += self.stepX     # hop left or right
            self.distX += self.deltaX   # accumulate x distance

            self.Wall = Ray.WallSide.NorthSouth
        
        else:                           # south west edge
            self.mapY += self.stepY     # hop up or down
            self.distY += self.deltaY   # accumulate Y distance 

            self.Wall = Ray.WallSide.EastWest

        return (self.mapX, self.mapY)

    def IntersectData(self):
        """
        returns depth, wallx
        """
        if self.Wall == Ray.WallSide.NorthSouth:
            depth = max(self.distX - self.deltaX, 1e-16)         # non euclidean distance avoids fish eye effect  
            wallx = self.posY - self.mapY + depth * self.dirY
            
            if (self.dirX > 0):                                 
                wallx = 1 - wallx
                
        elif self.Wall == Ray.WallSide.EastWest:                   
            depth = max(self.distY - self.deltaY, 1e-16)
            wallx = self.posX - self.mapX + depth * self.dirX
            
            if (self.dirY < 0):                                 
                wallx = 1 - wallx

            
        
        return depth, wallx
