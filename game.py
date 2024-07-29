import pygame
import sys


prozor = pygame.display.set_mode((1280 , 720))
sat = pygame.time.Clock()
def game():
    program_radi = True
    while program_radi:
        for dogadjaj in pygame.event.get():
            if dogadjaj.type == pygame.QUIT:
                program_radi = False
                sys.exit()
        prozor.blit(pygame.image.load("images\\grass.png") , (0,0))


        pygame.display.update()
game()
    
    