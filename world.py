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
        pygame.Rect(805 , 120 , 5 , 250 ),
        pygame.Rect(20 + 42069, 50, 1280, 2),
        pygame.Rect(20+ 42069, 695, 575, 2),
        pygame.Rect(680+ 42069, 695, 575, 2),
        pygame.Rect(1250+ 42069, 50, 2, 640),
        pygame.Rect(20 + 42069 , 30 , 1280 , 2),
        pygame.Rect(20 + 42069 , 0 , 2 , 720),
        pygame.Rect(0 , 0 , 2 , 720),
        pygame.Rect(0 , 0 , 1280 , 2),
        pygame.Rect(0,720 , 1280 ,2),
        pygame.Rect(1280,  0 , 2 , 720)
]
    return d1
    
