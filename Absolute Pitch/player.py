import pygame, math, os
from pygame.locals import *
from global_variables import *
from pygame.sprite import Sprite

class Player(Sprite):

    def __init__(self, screen_width, screen_height):

        self.image = pygame.image.load("Images/ship.bmp") # load image of player
        self.rotated = pygame.image.load("Images/ship.bmp") #variable for rotating image
        self.rect = self.image.get_rect()

        self.image.set_colorkey(BLACK) #set background?
        self.radius = 500 #define radius for tracking objects near player

        self.speed = 10 # movement speed of the player when capturing
        self.degree = 0 #used for rotation 

        self.rotationSpeed = 1 #rotation speed of player
        self.turnLeft = False
        self.turnRight = False

        self.target = None # starts off with no target

        self.targetReached = False #tells us when we've reached the target, if it's True, target returns to origin point
        self.atCenter = True #tells us if player is still in the middle (i.e. not capturing)
        
        #start our target in middle of screen
        self.x = screen_width // 2 #updating x position
        self.y = screen_height // 2 #updating y position

        #invisible box parameters for collision detection 
        self.width = 75
        self.height = 75

        self.viewer_angle = 90 #angle at which the viewer sees the player


    """
    Function: get the angle of orientation that the participant sees the Player object
    """

    def get_viewer_angle(self): #gets the angle at which viewer sees Player oriented
        #Adjusts for viewers perspective
        viewer_angle = (self.degree + 90) 
        self.viewer_angle = viewer_angle #store our value into the viewer angle

    """
    Function: given the viewer angle, give the direction vector for Player movement
    """

    def get_direction_vector(self):
        #Convert angle to radians
        angle_rad = math.radians(self.viewer_angle)
        dx = math.cos(angle_rad)
        dy = -math.sin(angle_rad) #invert the y axis due to Pygames oritentation
        return dx, dy
    

    """
    Function: using the direction vector, move the Player
    """

    def move(self): #function to move the Player along direction vector 
        # Calculate the direction vector
        dx, dy = self.get_direction_vector()

        # Update the position based on direction and speed
        self.x += dx * self.speed
        self.y += dy * self.speed

    """
    Function: rotate the Player using left and right arrow key
    """
    
    def update_position(self): #function to rotate Player

        #get center of rectangle and reset its center to origin point; keeps rectangle in cetner while rotating
        self.rect = self.rotated.get_rect()
        #self.rect.center = self.origin_point

        #turn left or right:
        if self.turnRight:
            self.degree -= self.rotationSpeed
        if self.turnLeft:
            self.degree += self.rotationSpeed

        # Reset angle if it passes 360 degrees in either direction
        self.degree %= 360

        # Rotate the image
        self.rotated = pygame.transform.rotate(self.image, self.degree)

        # Get a new rect with the center of the old rect
        # This line ensures that the player rotates around its center
        self.rect = self.rotated.get_rect(center=self.rect.center)
        

    """
    Function: draw the Player on the screen, including resetting center position to center of screen after rotation
    """
    
    def draw(self, screen): #function to draw the alien at a given position

        # Save original position
        original_x, original_y = self.x, self.y

        # Set position to screen center
        screen_center_x = screen.get_width() // 2
        screen_center_y = screen.get_height() // 2
        self.x = screen_center_x
        self.y = screen_center_y
        self.rect.center = (self.x, self.y)

        # Draw the player
        rotated_image = pygame.transform.rotate(self.image, self.degree)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)

        # Restore original position if necessary
        self.x, self.y = original_x, original_y


    






