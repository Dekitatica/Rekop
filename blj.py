import time
import random
import pygame

pygame.init()

window = pygame.display.set_mode((800,800))

class Dugme:
    def __init__(self, tekst, rect, boja):
        self.tekst = tekst
        self.rect = rect
        self.boja = boja


fnt = pygame.font.Font(None, 60)

def nacrtaj_dugme_bez_centiranja(dugme : Dugme):
    pygame.draw.rect(window, dugme.boja, dugme.rect)
    window.blit(dugme.tekst, dugme.rect.topleft)

hit = Dugme(fnt.render("Hit", True, (255, 255, 255)),pygame.Rect(550,200,200,125),pygame.Color("Red"))

stand = Dugme(fnt.render("Stand", True, (255, 255, 255)),pygame.Rect(50,200,200,125),pygame.Color("Red"))


cards = ["a","a","a","a"]

for i in range(2,14):
    if i !=11:
        for j in range(4):
            cards.append(i)

Clock = pygame.time.Clock()

def pick_a_card():
    ind = random.randint(0,len(cards)-1)
    card = cards[ind]
    del cards[ind]
    return card

your_cards = []
dealer_cards = [int(str(pick_a_card()).replace("a","11"))]
while True:
    window.fill("Gray")
    events = pygame.event.get()             
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    
    mousePressed = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    
    nacrtaj_dugme_bez_centiranja(hit)
    nacrtaj_dugme_bez_centiranja(stand)
    
    if mousePressed[0]:
        if hit.rect.collidepoint(mousePos[0],mousePos[1]):
            print("hit")
            your_cards.append(pick_a_card())
            if your_cards[-1] == "a":
                if sum(your_cards[0:(len(your_cards)-1)]) > 10:
                    your_cards[-1] = 1
                else:
                    your_cards.append(11)
            time.sleep(0.5)
            print(your_cards)
            if sum(your_cards) >21:
                print("L")
                exit()
            pass
        if stand.rect.collidepoint(mousePos[0],mousePos[1]):
            print("stand")
            time.sleep(0.5)
            while True:
                window.fill("Gray")
                events = pygame.event.get()
                
                for event in events:
                    if event.type == pygame.QUIT:
                        exit()
                txt = str(dealer_cards[0])
                cnt = True
                for c in dealer_cards:
                    if cnt:
                        cnt = False
                        continue
                    txt+="+" + str(c)+""
                txt +=" = " + str(sum(dealer_cards))
                window.blit(fnt.render(txt, True, (255, 0,0)), (150,700))
                window.blit(fnt.render(str(sum(your_cards)), True, (255, 255, 255)), (150,600))
                pygame.display.update()
                time.sleep(0.5)
                if sum(dealer_cards) > sum(your_cards) and sum(dealer_cards)<22:
                    print("L")
                    print(dealer_cards)
                    exit()
                else:
                    window.fill("Gray")
                    dealer_cards.append(pick_a_card())
                    if dealer_cards[-1] == "a":
                        if 24-sum(dealer_cards[0:len(dealer_cards)-1]) >= 11:
                            dealer_cards[-1] = 11
                        else:
                            dealer_cards+=1
                    if sum(dealer_cards)>21:
                        print("W")
                        txt = str(dealer_cards[0])
                        cnt = True
                        for c in dealer_cards:
                            if cnt:
                                cnt = False
                                continue
                            txt+="+" + str(c)+""
                        txt +=" = " + str(sum(dealer_cards))
                        window.blit(fnt.render(txt, True, (255, 0,0)), (150,700))
                        pygame.display.update()
                        time.sleep(5)
                        exit()
                    time.sleep(0.5)
                pygame.display.update()

            pass
    if len(your_cards)>0:
        txt = str(your_cards[0])
        cnt = True
        for c in your_cards:
            if cnt:
                cnt = False
                continue
            txt+="+" + str(c)+""
        txt +=" = " + str(sum(your_cards))
        window.blit(fnt.render(txt, True, (255, 255, 255)), (150,600))
    Clock.tick(60)
    pygame.display.update()