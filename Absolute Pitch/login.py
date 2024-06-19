import pygame
import sys
import os, json
from menu import main_menu


# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up the display
display_info = pygame.display.Info()
WIDTH = display_info.current_w
HEIGHT = display_info.current_h
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Login Screen")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# Input box properties
input_box = pygame.Rect((WIDTH // 2) - 100, (HEIGHT // 2) - 16, 200, 32)
color_inactive = GREY
color_active = BLACK
color = color_inactive
active = False
#username = ''

# Define font and music
font = pygame.font.Font('kongtext/kongtext.ttf', 20)
music = pygame.mixer.music.load(os.path.join('sound', 'background_music.mp3'))
click = pygame.mixer.Sound(os.path.join('sound', 'click_sound.wav'))

# Input box properties
input_box = pygame.Rect(100, 200, 440, 32)
color_inactive = GREY
color_active = BLACK
color = color_inactive
active = False
username = ''

# Placeholder text
placeholder_text = 'enter username'
placeholder_surface = font.render(placeholder_text, True, color_inactive)


# Function to call when login is attempted
#def login_function():
#    print("Login function called with username:", username)

# Main loop
def run_login():
    running = True
    pygame.mixer.music.play(-1)
    username=""
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                #if active:
                    if event.key == pygame.K_RETURN:
                        main_menu(username)
                        username = ''
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
        bgimage=pygame.image.load("Images/planet.bmp") #background image
        bgimage = pygame.transform.scale(bgimage, (WIDTH,HEIGHT))
        screen.blit(bgimage, (0,0))

        # Render the current text or placeholder text
        if username == '':
            txt_surface = placeholder_surface
        else:
            txt_surface = font.render(username, True, WHITE)

        # Resize the box if the text is too long
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        input_box.x = (WIDTH // 2) - (width // 2)
        input_box.y = (HEIGHT // 2)

        # Blit the text
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect
        pygame.draw.rect(screen, WHITE, input_box, 2)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_login()