import pygame
def rect_to_list(r : pygame.Rect) -> list:
    return [r.x,r.y,r.w,r.h]
def list_to_rect(l : list) -> pygame.Rect:
    return pygame.Rect(l[0],l[1],l[2],l[3])