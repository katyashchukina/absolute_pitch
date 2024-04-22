import pygame 
from bullet import Bullet
from enemy import Alien, Port
from player import Player
from global_variables import *
from random import shuffle
from break_generator import generator
import threading
import time
from tone_clouds import play_repeated_tone

pygame.init()
pygame.mixer.init()