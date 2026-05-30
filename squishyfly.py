
import pygame
import random

init = pygame.init()

# configuracion de la pantalla 
ancho = 400
alto = 600

pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Squishy Fly")

fds = 60
reloj = pygame.time.Clock()

# colores

blanco = (255, 255, 255)
negro = (0, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)
