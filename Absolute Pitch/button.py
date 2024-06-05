
import pygame
import sys

# Initialize pygame
pygame.init()

font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

display_info = pygame.display.Info() #gets info for screen

screen_width = display_info.current_w
screen_height = display_info.current_h
size = (screen_width, screen_height)

class ExitButton:
    def __init__(self):
        self.width = 80
        self.height = 40
        self.x = screen_width - self.width - 10
        self.y = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = RED
        self.text = "Exit"
        self.font = font

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        draw_text(self.text, self.font, WHITE, screen, self.rect.centerx, self.rect.centery)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Button:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
        
