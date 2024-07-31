import pygame
import sys
pygame.init()

dugme_font = pygame.font.SysFont('Consolas', 60)
prozor = pygame.display.set_mode((1280 , 720))
sat = pygame.time.Clock()
class Dugme():
    def __init__(self , tekst , rect ,boja):
        self.tekst = tekst
        self.rect = rect
        self.boja = boja

main_menu_dugme_quit = Dugme(dugme_font.render("EXIT", True, (255, 255, 255)) , pygame.Rect(560, 465 , 150 ,60) , pygame.Color("black"))
main_menu_dugme_credits = Dugme(dugme_font.render("CREDITS", True, (255, 255, 255)) ,pygame.Rect(520, 300 , 245 ,60)  , pygame.Color("black"))
credits_to_main_menu_button = Dugme(dugme_font.render("BACK", True, (255, 255, 255)) ,pygame.Rect(22, 470 , 200 ,60)  , pygame.Color("black"))
main_menu_play_button = Dugme(dugme_font.render("PLAY", True, (255, 255, 255)) ,pygame.Rect(560, 180 , 150 ,60)  , pygame.Color("black"))
def nacrtaj_dugme_bez_centiranja(dugme):
    pygame.draw.rect( prozor, dugme.boja, dugme.rect)
    prozor.blit(dugme.tekst, dugme.rect.topleft)
def main_menu():
    program_radi = True
    while program_radi:
        for dogadjaj in pygame.event.get():
            if dogadjaj.type == pygame.QUIT:
                program_radi = False
                sys.exit()
            if dogadjaj.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_dugme_quit.rect.collidepoint(dogadjaj.pos):
                    program_radi = False
                    pygame.quit()
                    sys.exit()
                if main_menu_dugme_credits.rect.collidepoint(dogadjaj.pos):
                    credits()

        prozor.fill((pygame.Color("cyan")))
        
        nacrtaj_dugme_bez_centiranja(main_menu_dugme_quit)
        nacrtaj_dugme_bez_centiranja(main_menu_dugme_credits)
        nacrtaj_dugme_bez_centiranja(main_menu_play_button)
        pygame.display.flip()
        sat.tick(30)
if __name__ == "main":

    main_menu()