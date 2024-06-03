import pygame 
from bullet import Bullet
from enemy import Alien, Port
from player import Player
from button import Button
from global_variables import *
from random import shuffle
from break_generator import generator
import threading
import time
from tone_clouds import play_repeated_tone, toneCloud
import random
import json
import thorpy as tp



class Game(object): 

    def __init__(self, updateGame, alien_notes):

        self.first_trial = True #first trial ever

        #create a notes dictionary, which maps alien information for each note in a tuple, including:
        #alien type (friendly vs unfriently), base frequency, alien image filepath, and port number
        self.alien_info = {"A": ("enemy", 440.00, "Images/Enemies/EnemyA/5LightGreenAlien.bmp",1),
                      "D#": ("enemy", 311.13, "Images/Enemies/EnemyA/3YellowAlien.bmp",4),
                      "C#": ("enemy", 277.18, "Images/Enemies/EnemyA/6LightBlueAlien.bmp",3),
                      "G": ("enemy", 392.00, "Images/Enemies/EnemyA/1RedAlien.bmp",6), 
                      "B": ("enemy", 493.88, "Images/Enemies/EnemyA/2Alien.bmp",2),
                      "F": ("enemy", 349.23, "Images/Enemies/EnemyA/4GreenAlien.bmp",5),
                      "A#": ("friendly", 466.16, "Images/Enemies/EnemyB/7BlueAlien.bmp",1),
                      "E": ("friendly", 329.63, "Images/Enemies/EnemyB/9PinkAlien.bmp",4),
                      "D": ("friendly", 293.66, "Images/Enemies/EnemyB/12PurpleAlien.bmp",3),
                      "G#": ("friendly", 415.30, "Images/Enemies/EnemyB/11BrownAlien.bmp",6),
                      "C": ("friendly", 261.63, "Images/Enemies/EnemyB/10MagentaAlien.bmp",2),
                      "F#": ("friendly", 369.99, "Images/Enemies/EnemyB/8LightPurpleAlien.bmp",5)}
        
        self.port_locations = ["lower left", "middle left", "upper left", "upper right", "middle right", "lower right"]

        self.alien_notes = alien_notes #notes for our different Aliens

        #sequence of notes to add

        self.updateGame = updateGame
        
        self.capture = False #Whether we are in a capture state or not (as in c has been pressed)

        self.played_alien_sound = False #has the Alien starting sound been played?

        self.post_sound_timer = False #has enough time passed after the sound has been played? 

        self.shoot = False #whether we want to shoot

        self.score = 0 #current score of the game

        self.collision = False #was there a collision between the two objects

        self.center_collision = False #was there a collision at the center? I.e no decision made

        self.alien_created = False #was an Alien created during the trial?

        self.miss = False #did the player miss the target?

        self.exit_game = False #whether we want to exit the game or not

        self.reached_highspeed = False #whether participant has reached highest speed for level

        self.correct = self.updateGame["Number Correct"] #tracker for number of correct 

        self.continue_toneCloud = True #shared flag for sound running

        self.numCorect = 0 #number of correct

        self.totalAlien = updateGame["Total Aliens"] #total number of aliens

        self.numCorect = updateGame["Number Correct"] #keeps track of the number of correct over a speed or level

        self.totalTrials = updateGame["Total Trials"] #total trials played in a given level/speed

        self.octave_variance = updateGame["Octave Variance"]

       #initalize list for storing various objects

        self.port_object_list = [] #list for ports
        self.alien_list = [] #list for aliens
        self.player_list = [] #list for player
        self.bullet_list = [] #list for bullets
        self.object_list = [] #list that stores all objects needed to be drawn 

        #Initialize various screen conditions

        pygame.init() #initialize pygame

        self.display_info = pygame.display.Info()
        self.screen_width = self.display_info.current_w
        self.screen_height = self.display_info.current_h
        self.screen_origin = (self.screen_width // 2, self.screen_height // 2)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)

        self.bgimage = pygame.image.load("Images/planet.bmp") #background image
        self.bgimage = pygame.transform.scale(self.bgimage, (self.screen_width, self.screen_height)) #transform our image to fit screen

    """
    Function: render text onto the Pygame screen

    Parameters:
    1. text: the text string to render
    """
    
    
    def render_text(self, text, time_delay = 3000): #function to render text onto the pygame screen
        font = pygame.font.Font('kongtext/kongtext.ttf', 20)
        text_surface = font.render(text, True, WHITE) #creates text

        # Text dimensions
        text_width, text_height = text_surface.get_size()

        # Calculating the position
        x = (self.screen_width - text_width) // 2  # Horizontal center
        y = (self.screen_height - text_height) // 2 #Vertical center

        self.screen.blit(self.bgimage, (0,0)) #draw in background image
        self.screen.blit(text_surface, (x, y)) #draw text onto center of screen
  
        pygame.display.flip() #update the display

        pygame.time.delay(time_delay)

        
    def exit_button_(self):
        exit_img = pygame.image.load('Images/button.png').convert_alpha()
        exit_button = Button(20,20,exit_img)
        if exit_button.draw():
            exit_game = True

    """
    Function: create a list of Alien objects for each note in level
    """
    
    def create_alien_list(self): #function to create alien objects


        alien_speed = self.updateGame["Speed"] #get alien_speed from dictionary
        notes = self.alien_notes
        self.alien_list = [] #initialize a list to plot with our aliens


        for note in notes:
            enemy_type, base_freq, image_filepath, port_number = self.alien_info[note]
            alien = Alien(enemy_type, base_freq, image_filepath, note, port_number)

            #setting Alien speed based on level speed
            
            if alien_speed == 1:
                alien.speed = 0.5
            elif alien_speed == 2:
                alien.speed = 1
            elif alien_speed == 3:
                alien.speed = 5
                self.reached_highspeed = True #reached the high speed

            self.alien_list.append(alien)
            
    """
    Function: create a list of ports
    """
    
    def create_ports(self): #function to create port objects

        #initialize pygame screen
        pygame.init() 
        pygame.display.init() 
        pygame.font.init()
        pygame.mixer.init() 

        #Get screen dimensions
        display_info = pygame.display.Info() #gets info for screen

        screen_width = display_info.current_w
        screen_height = display_info.current_h
        size = (screen_width, screen_height)

        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)


        for location in self.port_locations:
            new_port = Port(screen_dimensions= (screen_width, screen_height), color = GREEN, size = 50, location= location)
            self.port_object_list.append(new_port)
            self.object_list.append(new_port)

    """
    Function: create a list to store the Player object. Useful if we want more than one player
    """
    
    def create_player(self):

        #initialize pygame conditions
        pygame.init()
        pygame.display.init()

        #Get screen dimensions
        display_info = pygame.display.Info() #gets info for screen

        screen_width = display_info.current_w
        screen_height = display_info.current_h

        player = Player(screen_width, screen_height)
        player.origin_point = (screen_width // 2, screen_height // 2)
        self.player_list.append(player)
    
    """
    Function: creates a list of Bullet objects
    
    """
    
    def create_bullet(self): #creates a bullet object and saves to a list

        #initialize pygame conditions
        pygame.init()
        pygame.display.init()

        #Get screen dimensions
        display_info = pygame.display.Info() #gets info for screen

        screen_width = display_info.current_w
        screen_height = display_info.current_h

        bullet = Bullet(RED, screen_width // 2, screen_height // 2)
        self.bullet_list.append(bullet)



    """
    Function: return various values given a Pygame event
    """
    
    def handle_events(self): #function to handle getting pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "running false"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:  # Press ESC to exit
                    self.exit_game = True
                    return "running false"
                elif event.key == pygame.K_LEFT:
                    return "start left"
                elif event.key == pygame.K_RIGHT:
                    return "start right"
                elif event.key == pygame.K_c:
                    return "capture"
                elif event.key == pygame.K_s:
                    return "shoot"
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    return "end left"
                elif event.key == pygame.K_RIGHT:
                    return "end right"
                
    """
    Function: check to see if an object has collided with the screen
    """
    
    def check_boundary_collision(self, object):

        if (object.x < 0 or object.x > self.screen_width
            or object.y < 0 or object.y > self.screen_height):
            return False
        else:
            return True
        
    """
    Function: check if two objects have collided with one another
    """
                
    def check_object_collision(self, obj1, obj2):  

        #Function to check if there was a collision between two objects

        #Check for collisions
        if (obj1.x < obj2.x + obj2.width and 
            obj2.x < obj1.x + obj1.width and
            obj1.y < obj2.y + obj2.height and 
            obj2.y < obj1.y + obj1.height):

            collisions_occured = True
        
        else:
            collisions_occured = False


        return collisions_occured
    
    """
    Function: based on collisions and participant choices, calculate score for the current frame
    """
    
    def return_score(self, alien):

        score = 0

        if self.shoot: #if participant selected to shoot

            if alien.type == "enemy": #chose correct condition

                if self.collision: #if there was a collision
                    score += 50
                    self.correct += 1
                else: #miseed target
                    score -= 5
                    #subtract from correct in a row, unless less than 0, and set it equal to 0
                    if self.correct > 0:
                        self.correct -= 1
                    else:
                        self.correct = 0


            else: #alien was friendly
                score -= 10
                #subtract from correct in a row, unless less than 0, and set it equal to 0
                if self.correct > 0:
                    self.correct -= 1
                else:
                    self.correct = 0

        elif self.capture: #if participant chose to capture

            if alien.type == "friendly":
                
                if self.collision: #if there was a collision
                    score +=50
                    self.correct += 1
                else: #missed target
                    score -= 5
                     #subtract from correct in a row, unless less than 0, and set it equal to 0
                    if self.correct > 0:
                        self.correct -= 1
                    else:
                        self.correct = 0
            
            else: #alien was enemy
                score -= 10
                #subtract from correct in a row, unless less than 0, and set it equal to 0
                if self.correct > 0:
                    self.correct -= 1
                else:
                    self.correct = 0

        else: #no choice was made
            score -= 15
            self.center_collision = True
            #subtract from correct in a row, unless less than 0, and set it equal to 0
            if self.correct > 0:
                self.correct -= 1
            else:
                self.correct = 0

        return score
    
    """
    Function: move both the Player and Alien
    """
    
    def total_movement(self, alien, player, screen):
        player.update_position() #update player position
        player.draw(screen)
        alien.move() #might be extra
        alien.draw(screen)

    """
    Functions to play different sounds throughout the game
    """
    
    def play_sounds(self, sounds, duration): #Function to play pygame sounds
        for sound in sounds:
            sound.play()
            pygame.time.delay(int(duration)) #Delay between sounds

    
    def display_aliens_test(self, aliens): #displays alien images for testing

        alien_positions = []

        for alien in aliens:
            print(f"Port number is {alien.port_number}")
            alien.set_starting_position(self.screen_width, self.screen_height, alien.port_number)
            alien_surface = alien.image
            x = alien.x
            y = alien.y
            

        #return a tuple for determing correct mouse click. Tuple includes:
        #starting x coordinate, starting y coordinate, Alien image width and height
        return alien_positions


    def alien_test(self):

        # user_name = input("Please input username: ")
        # print(user_name)

        alien_list = []

        notes = self.alien_notes

        for note in notes:
            enemy_type, base_freq, image_filepath, port_number = self.alien_info[note]
            alien = Alien(enemy_type, base_freq, image_filepath, note, port_number)
            alien.set_starting_position(self.screen_width, self.screen_height, alien.port_number)
            alien_list.append(alien)

        alien_options = alien_list
        
        #create a list of alien images
        alien_surfaces = [alien.image for alien in alien_options]


        alien_selected = False
        correct_alien = random.choice(alien_options) #selects correct Alien from options

        displayed_aliens = False

        #Main loop
        while not alien_selected:

            if not displayed_aliens:

                self.screen.blit(self.bgimage, (0, 0))

                self.render_text("Choose correct Alien that matches sound")

                #play our tone cloud
                sounds = generator(200, 10, [correct_alien.freq,correct_alien.freq])
                self.play_sounds(sounds, 200)

                alien_positions = {}


                # Display all aliens
                counter = 0
                for i, surface in enumerate(alien_surfaces):
                    x = 0
                    y = 0
                    counter += 1
                    if counter == 1:
                        y += self.screen_height * (19/20)
                        self.screen.blit(surface, (x,y))
                        #update our dictionary
                        alien_positions[alien_options[i]] = (x,y)
                    elif counter == 2:
                        x += self.screen_width * (1/8)
                        y += self.screen_height * (19/20)
                        self.screen.blit(surface, (x, y))
                        alien_positions[alien_options[i]] = (x,y)
                    elif counter == 3:
                        y += self.screen_height * (1/2)
                        self.screen.blit(surface, (x,y))
                        alien_positions[alien_options[i]] = (x,y)
                    elif counter == 4:
                        x += self.screen_width * (1/8)
                        y += self.screen_height * (1/2)
                        self.screen.blit(surface, (x, y))
                        alien_positions[alien_options[i]] = (x,y)
                    elif counter == 5:
                        self.screen.blit(surface, (x, y))
                        alien_positions[alien_options[i]] = (x,y)
                    elif counter == 6:
                        x += self.screen_width * (1/8)
                        self.screen.blit(surface, (x, y))
                        alien_positions[alien_options[i]] = (x,y)
                    elif counter == 7:
                        x += self.screen_width * (19/20)
                        self.screen.blit(surface, (x, y))
                        alien_positions[alien_options[i]] = (x,y)
                    elif counter == 8:
                        x += self.screen_width * (17/20)
                        self.screen.blit(surface, (x, y))
                        alien_positions[alien_options[i]] = (x,y)
                    elif counter == 9:
                        x += self.screen_width * (19/20)
                        y += self.screen_height * (1/2)
                        self.screen.blit(surface, (x, y))
                        alien_positions[alien_options[i]] = (x,y)
                    elif counter == 10:
                        x += self.screen_width * (17/20)
                        y += self.screen_height * (1/2)
                        self.screen.blit(surface, (x, y))
                        alien_positions[alien_options[i]] = (x,y)
                    elif counter == 11:
                        x += self.screen_width * (19/20)
                        y += self.screen_height * (19/20)
                        self.screen.blit(surface, (x, y))
                        alien_positions[alien_options[i]] = (x,y)
                    elif counter == 12:
                        x += self.screen_width * (17/20)
                        y += self.screen_height * (19/20)
                        self.screen.blit(surface, (x, y))
                        alien_positions[alien_options[i]] = (x,y)


                pygame.display.flip()
                    

                displayed_aliens = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    alien_selected = True


                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:  # Press ESC to exit
                        alien_selected = True
                        break
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for alien, (target_x, target_y) in alien_positions.items():
                        width = alien.width
                        height = alien.height
                        if (target_x - width) <= mouse_x <= (target_x + width) and (target_y - height) <= mouse_y <= (target_y + height):
                            selected_alien = alien
                            break

                    # Check if the selected alien is the correct alien
                    correct_selection = (selected_alien == correct_alien)

                    # Get the color (or other property) of the selected alien
                    selected_alien_note = selected_alien.note  # Replace 'color' with the actual attribute

                    alien_selected = True

        #save data to json
        user_name = "test"
        file_name = str(user_name) + ".json"

        try:
            with open(file_name, "r") as file:
                #Load in existing file
                existing_data = json.load(file) 
        except FileNotFoundError:
            existing_data = []


        # Update our dictionary
        new_data = (f"Correct note was {correct_alien.note}, but Alien selected was {selected_alien_note}, which was {correct_selection}", correct_alien.note, selected_alien_note, correct_selection)
        existing_data.append(new_data)

        # Write to our json file
        with open(file_name, "w") as file:
            json.dump(existing_data, file, indent = 2)  # Using indent for better readability of JSON file

    
    def full_test(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:  # Press ESC to exit
                        running = False
                        break

            self.alien_test()


    
    """
    Function: iterate through a single trial
    """
    
    def update_frame(self):

        #initialize pygame screen
        pygame.init() 
        pygame.display.init() 
        pygame.font.init()
        pygame.mixer.init() 
        
        #Getting screen dimensions
        display_info = pygame.display.Info() #gets info for screen

        screen_width = display_info.current_w
        screen_height = display_info.current_h
        size = (screen_width, screen_height)

        #setting up backdrop image
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

        #Create ports and adds them to a list
        self.create_ports()

        #create aliens
        self.create_alien_list()
        
        #create our player 
        self.create_player()
        player = self.player_list[0]

        #create our bullet
        self.create_bullet()
        bullet = self.bullet_list[0]

        #Parameters to delay Alien after sound has been played
        delay_duration = 2000 #number of ms to delay before sending in Alien

        
        
        #step 4: main loop time!
        running = True
        while running and not self.exit_game:

            #Resetting 
            self.shoot = False
            self.capture = False
            self.collision = False

            #check to see if we should quit
            event = self.handle_events
            if event == "running false":
                running = False
                break
            
            # Draw the background
            screen.blit(self.bgimage, (0, 0))

            #update pygame screen once all ports are drawn
            pygame.display.flip()

            #pick a random alien to send out
            shuffle(self.alien_list)

            alien = self.alien_list[0] #pull our Alien object from the alien list
            alien.target = player.origin_point

            x,y,z, port_number = self.alien_info[alien.note] #extract port number for setting starting position

            alien_last_draw = 0 #last time the alien was drawn
            alien_draw_interval = 10 #number of ms to wait before redrawing screen

            
            while not alien.targetReached and not self.exit_game: #keep iterating and moving Alien until it has reached its target
                #check to see if we should quit
                
                event = self.handle_events
                if event == "running false":
                    running = False
                    alien.targetReached = True
                    break

                #check events and handle cases
                event = self.handle_events()

                if event == "start left":
                    player.turnLeft = True
                    bullet.turnLeft = True
                elif event == "start right":
                    player.turnRight = True
                    bullet.turnRight = True
                elif event == "end left":
                    player.turnLeft = False
                    bullet.turnRight = False
                elif event == "end right":
                    player.turnRight = False
                    bullet.turnRight = False
                elif event == "capture":
                    self.capture = True
                elif event == "shoot":
                    self.shoot = True

                # Play sound once at beginning of the trial
                if not self.played_alien_sound:
                    for port in self.port_object_list:
                        port.draw_port(screen)
                    player.draw(screen)
                    pygame.display.flip()
                    break_noise = generator(100, 10, [100,1300]) #generate our break noise
                    self.play_sounds(break_noise, 100)

                    time.sleep(3) #wait before playing Alien noise

                    alien_sound_thread = threading.Thread(
                        target=play_repeated_tone, args=(5, 2, alien.freq, lambda: alien.targetReached, self.octave_variance))
                    alien_sound_thread.start()
     

                    self.played_alien_sound = True

                if not alien.started_timer: #if we have not started timer before
                    start_time = pygame.time.get_ticks() #set start time
                    alien.started_timer = True
                elapsed_time = pygame.time.get_ticks() - start_time #get elapsed time
            

                # if the timer is running, you can still update and draw the player
                if elapsed_time < delay_duration: #if timer is still running

                    # Update player's position (including rotation)
                    player.update_position()

                    # Redraw the screen, ports, and player
                    screen.blit(self.bgimage, (0,0))
                    for port in self.port_object_list:
                        port.draw_port(screen)
                    player.draw(screen)
                    pygame.display.flip()


                else:

                    current_time = pygame.time.get_ticks()

                    if not alien.initialized: #if Alien has not been put at its starting position
                        alien.set_starting_position(screen_width, screen_height, port_number) #update Alien starting position

                    # After sound is played, handle alien's movement and drawing
                    if self.played_alien_sound:
                        #Creating threads
                        self.total_movement(alien = alien, player = player, screen = screen)
                       
                    
                    if self.capture: #if we want to capture
                        player.get_viewer_angle()
                        player.move()
                        self.collision = self.check_object_collision(alien, player)

                        if self.collision:
                            alien.targetReached = True
                            break


                    elif self.shoot: #if we want to shoot
                        player.get_viewer_angle()
                        bullet.viewer_angle = player.viewer_angle #sets the bullet facing in the same direction as player
                        bullet.move()
                        self.collision = self.check_object_collision(alien, bullet)

                        if self.collision:
                            alien.targetReached = True
                            break
 
                    
                    if current_time - alien_last_draw > alien_draw_interval: #if enough time has elapsed

                        screen.blit(self.bgimage, (0,0)) #reset screen as background image 
                        if self.check_boundary_collision(player): #checks if player is still on the screen 
                            #Draw in each port
                            for port in self.port_object_list:
                                port.draw_port(screen)
                            player.draw(screen) #draw in our player
                            alien.draw(screen) #draw in our Alien at the current position
                            self.alien_created = True #Alien was created
                            if self.shoot: #if we are in the shoot condition
                                bullet.draw(screen)


                            alien_last_draw = current_time #set last draw to current time
                        
                    if not self.check_boundary_collision(player) or not self.check_boundary_collision(bullet): #if either the player or bullet have left the screen
                        self.miss = True 

                    

                    pygame.display.flip() #update our screen

                    alien_current_position = alien.move()

                if alien.targetReached:
                    self.exit_game = True #to break out of a while loop
                    break

            
            
            #updating our score and dictionary for next iteration
            
            score = self.return_score(alien = alien)

            #increase Total trials
            self.totalTrials += 1

            
            #if we get the number of correct in a row = to our value, update level, update speed. If at highest speed, update level

            #update different variables and save into dictionary
            current_score = self.updateGame["Score"]
            current_score += score
            self.updateGame["Score"] = current_score

            self.updateGame["Note Types"] = self.alien_notes
            self.updateGame["Number Correct"] = self.correct
            self.updateGame["Total Trials"] = self.totalTrials
            
            #Make sure these get reset to False, and only set to True if below conditions are met
            self.updateGame["New Speed"] = False
            self.updateGame["New Level"] = False
            

            self.octave_variance = self.updateGame["Octave Variance"]
            total_trials = self.updateGame["Total Trials"] #total aliens seen thus far, meaning total possible correct answers

            #Get the number of trials required per level/speed
            notes = self.updateGame["Note Types"]
            num_notes = len(notes)
            trials_req = num_notes * 2 #number of trials required

            
            
            #if we have seen enough Aliens, and gotten enough accurate, we can move on
            if ((self.correct) / (total_trials)) > 0.9 and (self.totalTrials == trials_req):

                #if we have already hit high speed at the high octave variance, add Alien, reset speed and octave variance
                if self.reached_highspeed and self.octave_variance == "high": 

                    self.render_text("Adding Alien")

                    #update level
                    current_level = self.updateGame["Level"]
                    current_level += 1 #increase level by 1
                    self.reached_highspeed = False #reset booliean tracker
                    
                    #update our dictionary
                    self.updateGame["Speed"] = 1 #reset speed
                    self.octave_variance = "low" #reset octave variance
                    self.updateGame["Level"] = current_level 

                    #reset number correct and total trials
                    self.updateGame["Number Correct"] = 0
                    self.updateGame["Total Trials"] = 0

                    #update new level to be True
                    self.updateGame["New Level"] = True

                    #increase total Aliens in dictionary by 1
                    self.updateGame["Total Aliens"] = 0

                    #reset speed
                    self.updateGame["Speed"] = 1

                    #reset octave variance to low
                    self.octave_variance = "low"

                #if we reached high speed and at low octave variance, increase octave variance and reset speed

                elif self.reached_highspeed and self.octave_variance == "low": 
                    self.render_text("Dropping speed back down")
                    self.octave_variance = "high"
                    self.updateGame["Speed"] = 1

                    #Reset total trials and number correct
                    self.updateGame["Total Trials"] = 0
                    self.updateGame["Number Correct"] = 0

                else: #increase speed and update dictionary, but don't add new Aliens or change octave
                    self.render_text("Increasing speed")

                    current_speed = self.updateGame["Speed"]
                    current_speed += 1 #increase speed by 1
                    self.updateGame["Speed"] = current_speed

                    #reset values 
                    self.updateGame["Number Correct"] = 0
                    self.updateGame["Total Trials"] = 0
                    
                    self.updateGame["New Speed"] = True

                
            elif self.totalTrials == trials_req: #if we have hit the total number of trails, but there was not enough accuracy to move on
                #Decrease the speed
                print("Here :)")
                
                self.render_text("Unfortunately, you did not get enough correct to move to next level. Decreasing speed")
                
                current_speed = self.updateGame["Speed"]

                if current_speed == 1: #ensures speed will not go below 1
                    self.updateGame["Speed"] = 1
                else:
                    self.updateGame["Speed"] = current_speed - 1

                #reset values
                self.updateGame["Number Correct"] = 0
                self.updateGame["Total Trials"] = 0

            #update dictionary values
            self.updateGame["Octave Variance"] = self.octave_variance
 
            
            if self.exit_game:
                if self.miss: #if there was a miss, keep it rollling
                    return True, self.updateGame
                elif self.alien_created and self.center_collision : #keep it rolling if we have an alien and there was no choice made
                    return True, self.updateGame
                else:
                    return False, self.updateGame
            else:
                return True, self.updateGame #returns True because we want to run another instance of the frame
                

if __name__ == "__main__":
    game_dict = {"Speed":1, "Score":0, "Level":1, "Note Types": [], 
             "Octave Variance": "low", 
             "Number Correct":0, "Total Aliens":2, "Total Trials":0, 
             "New Speed": False, "New Level": False,
             } #starting dictionary
    
    pygame.init()
    pygame.mixer.init()
    new_notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

    
    game = Game(updateGame=game_dict, alien_notes=new_notes)
    game.full_test()