import pygame
import sys
import operate_game
import os, json
from global_variables import *
from game import Game
import time
from button import Button
#from login import run_login

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up the screen
screen_width = 750
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Alien Game!!!!")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (235, 150, 23)

# Set font
font = pygame.font.Font('kongtext/kongtext.ttf', 20)
music = pygame.mixer.music.load(os.path.join('sound', 'background_music.mp3'))
click = pygame.mixer.Sound(os.path.join('sound', 'click_sound.wav'))

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def main_menu(username):
    bgimage=pygame.image.load("Images/planet.bmp") #background image
    music=False
    pygame.mixer.music.play(-1)
    music = True
    #bgimage = pygame.transform.scale(bgimage, (screen_width, screen_height))
    #username = input("Enter Username: ")
    while True:
        screen.blit(bgimage, (0,0)) 
        draw_text("Main Menu", font, BLACK, screen, screen_width // 2, 50)
        #draw_text("Main Menu", font, BLACK, screen, screen_width // 2, 50)
        if not music:
            pygame.mixer.music.play(-1)
        # Calculate button positions based on screen size
        button_width = 100
        button_height = 50
        button_spacing = 20
        button_y = screen_height // 2 - (button_height + button_spacing) // 2
        play_button_x = (screen_width - button_width) // 2
        quit_button_x = (screen_width - button_width) // 2
        
        # Draw buttons
        # play_button = pygame.Rect(play_button_x, button_y, button_width, button_height)
        # quit_button = pygame.Rect(quit_button_x, button_y + button_height + button_spacing, button_width, button_height)
        # pygame.draw.rect(screen, BLACK, play_button)
        # pygame.draw.rect(screen, BLACK, quit_button)

        
        exit_button = Button(350, 200, 100, 50, BLACK, "Exit")
        new_game_button = Button(350, 300, 100, 50, BLACK, "New Game")
        keep_going_button = Button(350, 400, 150, 50, BLACK, "Keep Going")


        # Draw buttons
        exit_button.draw(screen)
        new_game_button.draw(screen)
        keep_going_button.draw(screen)

        
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.is_clicked(event.pos):
                    pygame.mixer.Sound.play(click)
                    pygame.quit()
                    sys.exit()
                elif new_game_button.is_clicked(event.pos):
                    #print("New Game button clicked!")
                    pygame.mixer.Sound.play(click)
                    music=False
                    pygame.mixer.music.stop()
                    operate_game.run_game(username,True)
                    

                    # You can call your new game function here
                elif keep_going_button.is_clicked(event.pos):
                    #print("Keep Going button clicked!")
                    pygame.mixer.Sound.play(click)
                    music=False
                    pygame.mixer.music.stop()
                    operate_game.run_game(username,False)
   



    

