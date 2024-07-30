import pygame
import sys
from Player import player

prozor = pygame.display.set_mode((1280, 720))
sat = pygame.time.Clock()
txt_trava = pygame.image.load("images\\grass.png")
txt_kuca = pygame.image.load("images\\kuca.png")
txt_kuca = pygame.transform.scale(
    txt_kuca, (txt_kuca.get_width() * 0.69, txt_kuca.get_height() * 0.69)
)


def nacrtaj_mapu():
    for i in range(3):
        for j in range(4):
            prozor.blit(txt_trava, (j * 320, i * 320))
    prozor.blit(txt_kuca, (120, 60))
    prozor.blit(txt_kuca, (500, 60))


def game():
    program_radi = True
    while program_radi:
        for dogadjaj in pygame.event.get():
            if dogadjaj.type == pygame.QUIT:
                program_radi = False
                sys.exit()
        nacrtaj_mapu()
        player.move()
        player.draw(prozor)
        pygame.display.update()
        

game()
