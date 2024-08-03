import time
import random
import pygame

pygame.init()

window = pygame.display.set_mode((800,800))

rects = []
for i in range(36):
    col = pygame.Color("Red")
    if i%2==0:
        col = pygame.Color("Black")  
    if i == 0:
        col = pygame.Color("Green")
    rects.append([i,pygame.Rect(i*30+400,20,30,40),col])

font = pygame.font.Font(None,30)

dx = random.randint(800,1500)/100
clock = pygame.time.Clock()
frame_count = 0
while True:
    window.fill("White")
    frame_count+=1
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
    
    for i,r in enumerate(rects):
        rects[i][1].x-=dx
        pygame.draw.rect(window,r[2],r[1])
        txt = font.render(
            str(r[0]),
            False,
            pygame.Color("white"),
        )
        window.blit(txt, (r[1].x+5, 30))
    dx-=0.01
    dx = max(0,dx)
    clock.tick(60) #tests
    for i in range(36):
        if rects[i][1].x <= -100:
            rects[i][1].x = rects[i][1].x+(36*30)
            rects.append(rects[i])
            del rects[i]
    pygame.draw.polygon(window,pygame.Color("Green"),((375,2),(425,2),(400,15)))
    pygame.display.update()