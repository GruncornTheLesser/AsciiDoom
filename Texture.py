import pygame, os
from pygame.locals import *

dir_path = __file__.removesuffix(os.path.basename(__file__))

class Texture:
    """A collection of images at different levels of detail"""
    def __init__(self, images):
        self.images = images

    def Load(filepath, mipmaps = 0):
        image = pygame.image.load(dir_path + filepath).convert(24)
        if int(min(image.get_height(), image.get_width()) * 0.5**mipmaps) == 0: raise Exception("cant generate mipmaps of size 0x0")
        images = [pygame.transform.smoothscale(image, (int(image.get_width() * 0.5**i), int(image.get_height() * 0.5**i))) for i in range(0, mipmaps + 1)]
        return Texture(images)
