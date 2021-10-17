class RayCast:
    """
    A projection from a point along a direction vector.
    Used to find the collisions in an axis aligned grid.
    """
    # an enum -> this is how your supposed to do it apparently??? 
    class __WallSide: 
        EW = 1              
        """the ray last traveled through an east facing or west facing gridline"""
        NS = 2  
        """the ray last traveled through a north facing or south facing gridline"""            
    
    def __init__(self, posX, posY, dirX, dirY):
        # the '__' is how you do encapsulation
        # i think i might throw up
        self.__posX = posX
        self.__posY = posY
        
        self.__dirX = dirX
        self.__dirY = dirY

        self.__mapX = int(posX)
        self.__mapY = int(posY)

        self.__deltaX = 1e30 if dirX == 0 else abs(1 / dirX)   
        self.__deltaY = 1e30 if dirY == 0 else abs(1 / dirY)

        if (dirX < 0):                              # if ray direction left
            self.__stepX = -1
            self.__distX = (posX - self.__mapX) * self.__deltaX
        else:                                       # if ray direction right
            self.__stepX = 1
            self.__distX = (self.__mapX + 1.0 - posX) * self.__deltaX
        

        if (dirY < 0):                              # if ray direction down
            self.stepY = -1
            self.__distY = (posY - self.__mapY) * self.__deltaY
        else:                                       # if ray direction up
            self.stepY = 1
            self.__distY = (self.__mapY + 1.0 - posY) * self.__deltaY

        self.__Wall = 0
        

    def Step(self):
        """
        iterate along line. uses a dda algorithm to ensure no tiles are missed.\n
        returns the coordinates of thenext tile the ray travels through.
        """
        if (self.__distX < self.__distY):   # north south edge
            self.__mapX += self.__stepX     # hop left or right
            self.__distX += self.__deltaX   # accumulate x distance

            self.__Wall = RayCast.__WallSide.NS
        
        else:                               # south west edge
            self.__mapY += self.stepY       # hop up or down
            self.__distY += self.__deltaY   # accumulate Y distance 

            self.__Wall = RayCast.__WallSide.EW

        return (self.__mapX, self.__mapY)

    def IntersectData(self):
        """
        returns the depth and relative x value along the wall from the last intersection with the grid
        """
        if self.__Wall == RayCast.__WallSide.NS:                # north south side
            depth = max(self.__distX - self.__deltaX, 1e-16)    # non euclidean distance avoids fish eye effect  
            wallx = self.__posY - self.__mapY + depth * self.__dirY
            
            if (self.__dirX > 0): wallx = 1 - wallx             # maintains the texture orientation
                
        elif self.__Wall == RayCast.__WallSide.EW:              # east west side               
            depth = max(self.__distY - self.__deltaY, 1e-16)
            wallx = self.__posX - self.__mapX + depth * self.__dirX
            
            if (self.__dirY < 0): wallx = 1 - wallx

        return depth, wallx

    def IntersectDepth(self):
        """
        returns the depth from the starting point and last intersection with the grid
        """
        if self.__Wall == RayCast.__WallSide.NS:    
            return max(self.__distX - self.__deltaX, 1e-16)
        else:                                   
            return max(self.__distY - self.__deltaY, 1e-16)

    def IntersectTexPos(self):
        """
        returns the texture position from intersection with the grid, this requires calculating depth but 
        """
        if self.__Wall == RayCast.__WallSide.NS:
            depth = max(self.__distX - self.__deltaX, 1e-16)
            if (self.__dirX > 0):   
                return 1 - (self.__posY - self.__mapY + depth * self.__dirY)
            else:                   
                return self.__posY - self.__mapY + depth * self.__dirY

        else: 
            depth = max(self.__distY - self.__deltaY, 1e-16)     
            if (self.__dirX > 0):   
                return 1 - (self.__posX - self.__mapX + depth * self.__dirX)
            else:                   
                return self.__posX - self.__mapX + depth * self.__dirX                                
