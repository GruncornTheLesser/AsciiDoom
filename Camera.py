from math import sin, cos

class Camera:
    def __init__(self, posX : float, posY : float, posZ : float, rotation = 0):

        self.posX = posX
        self.posY = posY
        self.posZ = posZ
        self.dirX = -1
        self.dirY = 0
        self.planeX = 0.0
        self.planeY = 0.66
        self.Rotate(rotation)

    def Rotate(self, angle : float):
        """
        rotates the camera by 'angle'(radians).
        """
        olddirx = self.dirX
        self.dirX = cos(angle) * self.dirX - sin(angle) * self.dirY
        self.dirY = sin(angle) * olddirx + cos(angle) * self.dirY

        oldplaneX = self.planeX
        self.planeX = cos(angle) * self.planeX - sin(angle) * self.planeY
        self.planeY = sin(angle) * oldplaneX + cos(angle) * self.planeY

    def MoveForward(self, magnitude : float):
        """
        moves the position forward by 'magnitude'. 
        a positive 'magnitude' results in a movement forwards.\n
        a negative 'magnitude' results in a movement backwards.
        """
        self.posX += self.dirX * magnitude # posx += dirx
        self.posY += self.dirY * magnitude # posy += diry

    def MoveNormal(self, magnitude : float):
        """
        moves the position along the normal to the direction vector by 'magnitude'. \n
        a positive 'magnitude' results in a movement left.\n
        a negative 'magnitude' results in a movement right.
        """
        self.posX -= self.dirY * magnitude # posx -= diry
        self.posY += self.dirX * magnitude # posy += dirx
