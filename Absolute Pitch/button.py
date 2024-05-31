import pygame, math, os
from pygame.locals import *
from global_variables import *
from pygame.sprite import Sprite

class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    def draw (self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouseget_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked == False
        return action


        screen.blit(self.image, (self.rect.x,self.rect.y))
