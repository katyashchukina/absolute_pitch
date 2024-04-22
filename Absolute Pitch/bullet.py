import pygame
from global_variables import *
from pygame.sprite import Sprite
import math

class Bullet(Sprite):

    def __init__(self, color, center_x, center_y):

        super().__init__()

        #creates the bullet image as a 15 x 20 pixel, and fills it in with the specified bullet color and background
        self.image = pygame.Surface([15, 20]) 
        self.rotated = self.image
        self.image.fill(color) 
        self.rect = self.image.get_rect()

        self.image.set_colorkey(BLACK) #set background

        # Set the bullet's initial position to the center of the Player object
        self.x = center_x
        self.y = center_y

        #invisible box parameters used for collision detection
        self.width = 75
        self.height = 75

        
        self.speed = 10 #speed of the bullet

        self.viewer_angle = 90 # Starting angle at which the bullet is oriented to the viewer


    """
    Function: get the direction that the Bullet object is facing. Direction facing needed for move function
    """
    
    def get_direction_vector(self):
        #Convert angle to radians
        angle_rad = math.radians(self.viewer_angle)
        dx = math.cos(angle_rad)
        dy = -math.sin(angle_rad) #invert the y axis due to Pygames oritentation
        return dx, dy
    
    """
    Function: move the bullet (utilizes player orientation; see game.py)
    """
    
    def move(self): #function to move the Player along direction vector 
        # Calculate the direction vector
        dx, dy = self.get_direction_vector()

        # Update the position based on direction and speed
        self.x += dx * self.speed
        self.y += dy * self.speed

    
    """
    Function: draws the Bullet object onto the screen

    Parameters: 

    1. screen: the screen to draw the bullet onto

    """
    def draw(self, screen):
        
        #set rectangle position
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        #add image to the screen
        screen.blit(self.image, self.rect)

        


    
