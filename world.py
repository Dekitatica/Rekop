import pygame
def getworld() -> dict:
    d1 = dict()
    d1["walls"] = [
    pygame.Rect(165, 120, 5, 250),
    pygame.Rect(165, 370, 120, 5),
    pygame.Rect(165, 120, 260, 5),
    pygame.Rect(415, 120, 5, 250),
]
    return d1