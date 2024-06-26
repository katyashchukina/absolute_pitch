import os, json
import pygame
from global_variables import *
from game import Game
import time

#Things to add: octave functionaltiy with tones, consistent tone playing during movement, auto saving and reloading in level, score decreasing while time elapses,
#  updating score more continuously, fix rotation origin of plane,
#  moving back down speed?
#Want a sound toolbox that has sub latency of 500 ms, and jitter sub 1 ms
#PTB library has lowest latencies, most recommended, with different latency settings
#Psychtoolbox in general is ideal for psychology/neuroscience research
#Psychtoolbox might have a hard time integrating into Pygame

exit_game = False

counter = 1

#Sets first trial boolieans for block text

first_trial_shoot = True 
first_trial_capture = True
first_trial_both = True

start_game_dict = {"Speed":1, "Score":0, "Level":1, "Note Types": [], 
             "Octave Variance": "low", 
             "Number Correct":0, "Total Aliens":2, "Total Trials":0, 
             "New Speed": False, "New Level": False,
             } #starting dictionary

block_type = "shoot" #starting block type

welcome_text1 = "Welcome to the Battle Star Game!"
shoot_block_text = "You are starting the shoot block."
shoot_block_text2 = "All Aliens you see will be enemy Aliens."
shoot_block_text3 = "Use the arrows to rotate your player to face the enemy Alien"
shoot_block_text4 = "Press S to shoot and kill the enemy."
shoot_block_text5 = "The faster you shoot the Alien,the more points you gain."
shoot_block_text6 = "Move your player and shoot before the Alien comes on screen." 
shoot_block_text7 = "Remember you have only one shot, so make it count!"
capture_block_text = "You are starting the capture block. All Aliens you will see will be friendly Aliens. Use the arrows to rotate your player to face the friendly Alein, and press C to use your Player to Capture the Alien"
capture_block_text2 = "The longer the Alien is on the screen, the more points you will lose."
capture_block_text3 = "You can move your player and capture before the Alien comes on screen. Just remember you have only one capture, so make it count!"
both_block_text = "Now, Aliens will be either friendly or enemy. Use the arrows to rotate your player, and press S to shoot enemy aliens, or C to capture friendly aliens"
new_speed_text = "Now, there will be the same number of Aliens, but their speed will increase"
new_level_text = "New level unlocked. Adding new Alien. Speed will go back down"

level_dict = {1: ["A", "D#"],
              2: ["A", "D#", "C#"],
              3: ["A", "D#", "C#", "G"],
              4: ["A", "D#", "C#", "G", "B"],
              5: ["A", "D#", "C#", "G", "B", "F"],
              6: ["A#", "E"],
              7: ["A#", "E", "D"],
              8: ["A#", "E", "D", "G#"],
              9: ["A#", "E", "D", "G#", "C"],
              10: ["A#", "E", "D", "G#", "C", "F#"],
              11: ["A#", "A", "D", "E#"],
              12: ["D", "C#", "G", "G#"],
              13: ["C", "B", "F", "F#"],
              14: ["A#", "A", "D#", "E", "C", "B", "F#", "F"],
              15: ["C", "B", "F", "F#", "D", "C#", "G", "G#"],
              16: ["A", "A#", "D#", "E", "D", "C#", "G", "G#"],
              17: ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
              }


"""
Function: load in data based on username
"""
def load_data(username):
    filename = f"{username}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        
    else:
        data = start_game_dict

    return data

"""
Function: save data based on username
"""
def save_data(username, data, type):
    if type == "dict":
        filename = f"{username}.json"
    elif type == "test":
        filename = f"{username}_{type}.json"
    
    #Want to save all test data but most recent dicitonary data
    if type =="dict":
        existing_data = data

    elif type=="test": 

        # If the file already exists, read the existing data
        if os.path.exists(filename):
            with open(filename, "r") as file:
                existing_data = json.load(file)
                # Update the existing data with the new data
                existing_data = existing_data + data #combine the two lists
        else:
            # If the file doesn't exist, use the new data as the existing data
            existing_data = data

    # Write the existing (updated) data back to the file
    with open(filename, "w") as file:
        json.dump(existing_data, file)


def run_game(username):
    exit_game=False
    game_dict = load_data(username)
    #reset number correct and total number
    game_dict["Number Correct"] = 0
    game_dict["Total Trials"] = 0

    #reset to medium speed so participants are not bombarded
    if game_dict["Speed"] == 3:
        print("Changing speed")
        game_dict["Speed"] = 2 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    exit_game = True

        if exit_game: #breaks while loop
            break
                    
        #Update our dictionary notes based on level
        level = game_dict["Level"]
        new_notes = level_dict[level]
        new_speed = game_dict["New Speed"]
        new_level = game_dict["New Level"]
        
        game = Game(updateGame=game_dict, alien_notes=new_notes)

        #new block text
        global first_trial_shoot, first_trial_capture, first_trial_both
        if level == 1 and first_trial_shoot:
            game.render_text(welcome_text1)
            time.sleep(2)
            game.render_text(shoot_block_text)
            time.sleep(2)
            game.render_text(shoot_block_text2)
            time.sleep(2)
            game.render_text(shoot_block_text3)
            #break
            time.sleep(2)
            game.render_text(shoot_block_text4)
            time.sleep(2)
            game.render_text(shoot_block_text5)
            time.sleep(2)
            game.render_text(shoot_block_text6)
            time.sleep(2)
            game.render_text(shoot_block_text7)
            time.sleep(2)
            first_trial_shoot = False 
        elif level == 6 and first_trial_capture:
            game.render_text(capture_block_text)
            time.sleep(2)
            game.render_text(capture_block_text2)
            time.sleep(2)
            game.render_text(capture_block_text3)
            time.sleep(2)
            first_trial_capture = False
        elif level == 11 and first_trial_both:
            game.render_text(both_block_text)
            first_trial_both = False
        

        #new speed and new level text
        if new_level:
            game.render_text(new_level_text)
        if new_speed and not new_level:
            game.render_text(new_speed_text)

        #run the update game function
        continue_game, current_dict = game.update_frame()

        current_score = current_dict["Score"]

        game.render_text(f"Your current score is {current_score}", time_delay=1000)


        #save our dictionary data to the file 
        run_game.save_data(username, current_dict, type="dict")

        
        if not continue_game: #break out of while loop if hit exit during update frame function
            break

        pygame.time.delay(2000) #wait before next trial
    
