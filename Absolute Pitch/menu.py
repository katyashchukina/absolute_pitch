import pygame
import sys
import run_game
import os, json
from global_variables import *
from game import Game
import time

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Set font
font = pygame.font.SysFont(None, 50)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def main_menu():
    bgimage=pygame.image.load("Images/planet.bmp") #background image
    #bgimage = pygame.transform.scale(bgimage, (screen_width, screen_height))
    username = input("Enter Username: ")
    while True:
        screen.blit(bgimage, (0,0)) 
        draw_text("Main Menu", font, BLACK, screen, screen_width // 2, 50)
        
        # Draw buttons
        play_button = pygame.Rect(150, 150, 100, 50)
        quit_button = pygame.Rect(150, 220, 100, 50)
        pygame.draw.rect(screen, GRAY, play_button)
        pygame.draw.rect(screen, GRAY, quit_button)

        
        draw_text("Play", font, BLACK, screen, play_button.centerx, play_button.centery)
        draw_text("Quit", font, BLACK, screen, quit_button.centerx, quit_button.centery)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_button.collidepoint(mouse_pos):
                    # Call function to start the game
                    run_game.run_game(username)
                elif quit_button.collidepoint(mouse_pos):
                    return



    

if __name__ == "__main__":
    main_menu()