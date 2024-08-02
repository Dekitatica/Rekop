import random
import time
import pygame
def rect_to_list(r : pygame.Rect) -> list:
    return [r.x,r.y,r.w,r.h]
def list_to_rect(l : list) -> pygame.Rect:
    return pygame.Rect(l[0],l[1],l[2],l[3])

def pick_a_card(available_cards,ur_cards):
    if len(available_cards)==0:
        return None
    ind = random.randint(0,len(available_cards)-1)
    card = available_cards[ind]
    if card+sum(ur_cards)>21 and card==11:
        card = 1
    del available_cards[ind]
    return card