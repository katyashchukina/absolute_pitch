import pygame
from pygame.sprite import Sprite
from global_variables import *

class Port(Sprite):
    
    def __init__(self, screen_dimensions, color, size, location):
        
        self.location = (0,0)
        self.color = color
        self.screen_width, self.screen_height = screen_dimensions

        self.x = 0
        self.y = 0

        self.size = size #sets port size

        self.location = location
        

    def draw_port(self, screen):

        #setting coordinates based on location 
        if "left" in self.location:
            self.x_coord = 0
            if "lower" in self.location:
                self.y_coord = self.screen_height
            elif "middle" in self.location:
                self.y_coord = (self.screen_height) // 2
            else:
                self.y_coord = 0

        else:
            self.x_coord = self.screen_width
            if "lower" in self.location:
                self.y_coord = self.screen_height
            elif "middle" in self.location:
                self.y_coord = (self.screen_height) // 2
            else:
                self.y_coord = 0

        #recalculate x and y coordinate so they are top left of square 

        self.x_coord = int(self.x_coord - (self.size / 2))
        self.y_coord = int(self.y_coord - (self.size / 2))
    
        pygame.draw.rect(screen, self.color, (self.x_coord, self.y_coord, self.size, self.size))


class Alien(Sprite): #Enemy is a sublcass of Sprite class, and inhereits pygame functionality

    def __init__(self, enemy_type, base_freq, image_filepath, note, port_number):
        
        pygame.sprite.Sprite.__init__(self) #initializes enemy as pygame Sprite object

        self.targetReached = False #initialized enemey has not reached target yet

        self.speed = 0 #initialize speed

        self.offscreen_time = 6 #seconds before enemy appears

        self.freq = base_freq #note freq

        self.type = enemy_type #initialize whether alien is friend or enemy

        self.image_filepath = image_filepath #initializes image path for alien

        self.starting_position = 0 #starting location for alien

        self.note = note #what note the alien corresponds with

        self.target = True #boolean to see if the alien has a target value

        self.initialized = False #Alien has not been initialized yet

        self.x = 0 #updating x position
        self.y = 0 #updating y position

        #setting parameters for an invisible box around Alien for collision detection
        self.width = 75
        self.height = 75

        self.started_timer = False #has Alien timer been started?

        #initialize popping sound
        pygame.mixer.init()

        #create alien image
        self.image = pygame.image.load(image_filepath) #load in our image
        self.image = pygame.transform.smoothscale(self.image, (40,40)) #rescale image
        self.image.set_colorkey(WHITE) #hides background
        self.rect = self.image.get_rect() #gets image dimensions

        self.port_number = port_number

        
        #offset timing for positioning purposes
        self.offsetTime = self.speed*FPS*self.offscreen_time #multiply by FPS for fps-->s (FPS should be 60 and in global_variables file)

        #list of points for enemy position
        self.offset_points = [(-self.offsetTime,-self.offsetTime),(SCREEN_WIDTH+self.offsetTime,-self.offsetTime),
        (SCREEN_WIDTH+self.offsetTime,SCREEN_HEIGHT//2),(SCREEN_WIDTH+self.offsetTime, SCREEN_HEIGHT+self.offsetTime), (-self.offsetTime, SCREEN_HEIGHT+self.offsetTime), (-self.offsetTime, SCREEN_HEIGHT//2)]
        
    """
    Function: draw the Alien

    Parameters:
    1. screen: the screen to draw the Alien onto
    """
    
    def draw(self, screen): 

        #load in alien bmp image
        self.image

        #create a backdrop rect to control image location
        alien_rect = self.image.get_rect()

        #set rectangle position
        alien_rect.center = [self.x, self.y]

        #add image to the screen
        screen.blit(self.image, alien_rect)

    
    """
    Function: sets the alien starting position based on a designated port

    Parameters:
    1.screen_width: width of screen
    
    2.screen_height: screen height

    3.port_number: the port at which to initialize the alien's location to 

    """
        
    def set_starting_position(self, screen_width, screen_height, port_number): #sets alien starting position

        self.targetReached = False #reset target position
        self.initialized = True #initializing alien position

        #setting alien starting position based on port number
        if port_number == 1:
            self.x, self.y = (0, screen_height)
        elif port_number == 2:
            self.x, self.y = (0,(screen_height // 2))
        elif port_number == 3:
            self.x, self.y = (0, 0)
        elif port_number == 4:
            self.x, self.y = (screen_width, 0)
        elif port_number == 5:
            self.x, self.y = (screen_width, (screen_height // 2))
        elif port_number == 6:
            self.x, self.y = (screen_width, screen_height)

    
    """
    Function: move the Alien towards the Player at the center of the screen
    """
    
    def move(self): #function to move alien
        """ Automatically called when we need to move the enemy. """
        """ Set Vector towards player"""
        if self.target: #checks if there is a target position set

            #Get current position
            position_x, position_y = self.x, self.y

            #get target position
            target_x, target_y = self.target

            #calculate distance between current position and target
            dist_x, dist_y = target_x - position_x, target_y - position_y

            #calculate magnitude of distance vector
            dist_length = (dist_x ** 2 + dist_y ** 2) ** 0.5

            #normalize distance vector to get unit vector
            if dist_length > 0:
                direction_x = dist_x / dist_length
                direction_y = dist_y / dist_length
            else:
                direction_x, direction_y = 0,0
            
            #Move the alien
            self.x += direction_x * self.speed
            self.y += direction_y * self.speed

            #check if alien has reached the target within a margin of error equal to the speed
            if abs(dist_x) < self.speed and abs(dist_y) < self.speed:
                self.target = None
                self.targetReached = True
            
            return self.rect.topleft
        



        


