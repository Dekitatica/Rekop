import pygame
def getworld() -> dict:
    d1 = dict()
    d1["walls"] = [
        pygame.Rect(165, 120, 5, 250),
        pygame.Rect(165, 370, 110, 5),
        pygame.Rect(165, 120, 250, 5),
        pygame.Rect(415, 120, 5, 250),
        pygame.Rect(555 , 120 , 5 , 250),
        pygame.Rect(555 , 370 , 110 ,5 ),
        pygame.Rect(555 , 120 , 250 , 5 ),
        pygame.Rect(805 , 120 , 5 , 250 )
]
    return d1