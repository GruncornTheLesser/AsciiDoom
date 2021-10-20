from math import cos, sin
import pygame, sys
from pygame.locals import *

class Camera:
	def __init__(self, posX, posY, posZ, rotation = 0):
		self.posX = posX
		self.posY = posY
		self.posZ = posZ
		self.dirX = -1
		self.dirY = 0
		self.planeX = 0.0
		self.planeY = 0.66
		self.Rotate(rotation)

	def Rotate(self, angle : float):
		"""rotates the camera by angle(radians)."""
		olddirx = self.dirX
		self.dirX = cos(angle) * self.dirX - sin(angle) * self.dirY
		self.dirY = sin(angle) * olddirx + cos(angle) * self.dirY

		oldplaneX = self.planeX
		self.planeX = cos(angle) * self.planeX - sin(angle) * self.planeY
		self.planeY = sin(angle) * oldplaneX + cos(angle) * self.planeY
	
	def MoveForward(self, magnitude):
		"""
		moves the position forward by 'magnitude'. 
		a positive 'magnitude' results in a movement forwards.\n
		a negative 'magnitude' results in a movement backwards.
		"""
		self.posX += self.dirX * magnitude # posx += dirx
		self.posY += self.dirY * magnitude # posy += diry

	def MoveNormal(self, magnitude):
		"""
		moves the position along the normal to the direction vector by 'magnitude'. \n
		a positive 'magnitude' results in a movement left.\n
		a negative 'magnitude' results in a movement right.
		"""
		self.posX -= self.dirY * magnitude
		self.posY += self.dirX * magnitude







class Map:
	def __init__(self):
		self.buffer = [
			[1, 1, 1, 1, 1, 1, 1, 1],
			[1, 0, 0, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 0, 0, 1],
			[1, 0, 0, 0, 0, 0, 0, 1],
			[1, 1, 1, 1, 1, 1, 1, 1],
		]

	def __getitem__(self, pos):
		x, y = pos
		return self.buffer[y][x]

class RayCast:
	class __WallSide: 
		EW = 1              
		"""the ray last traveled through an east facing or west facing gridline"""
		NS = 2  
		"""the ray last traveled through a north facing or south facing gridline"""            
	
	def __init__(self, posX, posY, dirX, dirY):
		# set the pos in this object
		self.__posX = posX
		self.__posY = posY
		# the rays current position in the map
		self.__mapX = int(posX)
		self.__mapY = int(posY)
		
		# set the dir in this object
		self.__dirX = dirX  
		self.__dirY = dirY

		self.__deltaX = 1e30 if dirX == 0 else abs(1 / dirX) # the amount to change per single tile in y
		self.__deltaY = 1e30 if dirY == 0 else abs(1 / dirY) # the amount to change per single tile in x

		if (dirX < 0):                              # if ray direction left
			self.__stepX = -1                       # the step is negative 1
			# this line gets the starting distance offset to the first edge
			self.__distX = (self.__posX - self.__mapX) * self.__deltaX          
		else:                                       # if ray direction right
			self.__stepX = 1                        # the step is positive 1
			# this line gets the starting distance offset to the first edge
			self.__distX = (self.__mapX + 1.0 - self.__posX) * self.__deltaX    

		if (dirY < 0):                              # if ray direction down
			self.stepY = -1                         # the step is negative 1
			# this line gets the starting distance offset to the first edge
			self.__distY = (posY - self.__mapY) * self.__deltaY
		else:                                       # if ray direction up
			self.stepY = 1                          # the step is positive 1
			# this line gets the starting distance offset to the first edge
			self.__distY = (self.__mapY + 1.0 - posY) * self.__deltaY

		self.__Wall = 0

	def Step(self):
		"""iterate along line. uses a dda algorithm to ensure no tiles are missed.\n
		returns the coordinates of the next tile the ray travels through."""
		if (self.__distX < self.__distY):   # north south edge
			self.__mapX += self.__stepX     # hop left or right
			self.__distX += self.__deltaX   # accumulate x distance

			self.__Wall = RayCast.__WallSide.NS # store that it hit a north south edge
        
		else:                               # south west edge
			self.__mapY += self.stepY       # hop up or down
			self.__distY += self.__deltaY   # accumulate Y distance 

			self.__Wall = RayCast.__WallSide.EW # store that it hit a east west edge

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
		"""returns the depth from the starting point and last intersection with the grid"""
		if self.__Wall == RayCast.__WallSide.NS:    
			return max(self.__distX - self.__deltaX, 1e-16)
		else:                                   
			return max(self.__distY - self.__deltaY, 1e-16)

	def IntersectTexPos(self):
		"""the texture position from intersection with the grid, this requires calculating depth but """
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









class Window:
	def init(title, bkg, canvas_size, screen_size = (800, 600)):
		Window.background = bkg

		Window.title = title
		pygame.display.set_caption(title)

		Window.canvaswidth,	Window.canvasheight	= canvas_size
		Window.canvas = pygame.Surface(canvas_size) 

		Window.screenwidth, Window.screenheight = screen_size
		Window.screen = pygame.display.set_mode(screen_size)

		
	def Refresh():
		Window.screen.blit(pygame.transform.scale(Window.canvas, (Window.screenwidth, Window.screenheight)), (0, 0))
		pygame.display.update()
	
	def Clear():
		Window.canvas.fill(Window.background)

	def SetTitle(title):
		pygame.display.set_caption(str(title))



MAX_DEPTH = 5
def Render(cam, map):
	Window.Clear()
	for x in range(Window.canvaswidth):
		raycast = RayCast(cam.posX, cam.posY, cam.dirX + cam.planeX * (2 * x / Window.canvaswidth - 1), cam.dirY + cam.planeY * (2 * x / Window.canvaswidth - 1))

		while True:
			mv = map[raycast.Step()]
			if mv > 0:
				depth = raycast.IntersectDepth()
				break

		lineheight = int(Window.canvasheight / depth)
		start = int(Window.canvasheight // 2 - lineheight * (cam.posZ))
		end = 	int(Window.canvasheight // 2 + lineheight * (1 - cam.posZ))
		colour = min(255, depth / MAX_DEPTH * 255)

		pygame.draw.line(Window.canvas, (colour, colour, colour), (x, max(0, start)), (x, min(end, Window.canvasheight)), 1)

		#for y in range(max(0, start), min(end, Window.canvasheight)):
		#	Window.canvas.set_at((x, y), (colour, colour, colour))
	Window.Refresh()


Textures = [
	pygame.image.load("Textures/tex_stones_2.png"), 


]

def Render_tex(cam, map):
	Window.Clear()
	for x in range(Window.canvaswidth):
		raycast = RayCast(cam.posX, cam.posY, cam.dirX + cam.planeX * (2 * x / Window.canvaswidth - 1), cam.dirY + cam.planeY * (2 * x / Window.canvaswidth - 1))

		while True:
			mapvalue = map[raycast.Step()]
			if mapvalue > 0:
				depth, texU = raycast.IntersectData()
				break

		lineheight = int(Window.canvasheight / depth)
		start = int(Window.canvasheight // 2 - lineheight * (cam.posZ))
		end = 	int(Window.canvasheight // 2 + lineheight * (1 - cam.posZ))

		#pygame.draw.line(Window.canvas, (colour, colour, colour), (x, max(0, start)), (x, min(end, Window.canvasheight)), 1)

		for y in range(max(0, start), min(end, Window.canvasheight)):
			texV = (y - start) / lineheight
			Window.canvas.set_at((x, y), Textures[mapvalue - 1].get_at((int(texU * 15), int(texV * 15))))
	Window.Refresh()


Window.init("", (128,64,128), (100, 75))

Cam = Camera(4, 4, 0.5)
Map = Map()

FPS = 60
Clock = pygame.time.Clock()

def main():
	while True:# Get inputs
		delta = Clock.tick() / 1000.0

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[K_q]:
			Cam.Rotate(2 * delta)
		if pressed_keys[K_e]:
			Cam.Rotate(-2 * delta)


		if pressed_keys[K_w]:
			Cam.MoveForward(2 * delta)
		if pressed_keys[K_a]:
			Cam.MoveNormal(2 * delta)
		if pressed_keys[K_s]:
			Cam.MoveForward(-2 * delta)
		if pressed_keys[K_d]:
			Cam.MoveNormal(-2 * delta)
		if pressed_keys[K_r]:
			Cam.posZ += -2 * delta
		if pressed_keys[K_f]:
			Cam.posZ -= -2 * delta
				
		Render_tex(Cam, Map)
		
		Window.SetTitle(int(Clock.get_fps()))
 
main()
