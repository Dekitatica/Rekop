import pygame


class Player:
    def __init__(self  , x , y,id,money):
        self.x = x
        self.y = y
        self.money = money
        self.speed = 5
        self.pravac = "desno"
        self.txt_player_left = pygame.image.load("images//player.png")
        self.txt_player_right =pygame.image.load("images//playerright.png")
        self.txt_player_left = pygame.transform.scale(self.txt_player_left , (45 , 65))
        self.txt_player_right = pygame.transform.scale(self.txt_player_right , (45 , 65))
        self.picture = self.txt_player_right
        self.id = id
        self.collision = False
        self.rect = pygame.Rect(self.x , self.y , 35 , 65)
    def move(self):
        zidovi = [
            pygame.Rect(165, 120, 5, 250),
            pygame.Rect(165, 370, 120, 5),
            pygame.Rect(165, 120, 260, 5),
            pygame.Rect(415, 120, 5, 250),
        ]
        keys = pygame.key.get_pressed()
        if False:
            pass
        else:
        
            self.rect.x = self.x
            self.rect.y = self.y
            if keys[pygame.K_w]:
                clear = 0
                for i in range(4):
                    zid = zidovi[i]
                    if pygame.Rect(self.rect.x,self.rect.y-self.speed,self.rect.width,self.rect.height).colliderect(zid) == False:
                        clear+=1
                if clear==4:
                    self.y-=self.speed
                
            if keys[pygame.K_s]:
                clear = 0
                for i in range(4):
                    zid = zidovi[i]
                    if pygame.Rect(self.rect.x, self.rect.y + self.speed , self.rect.width , self.rect.height).colliderect(zid) == False:
                        clear +=1
                if clear == 4:

                    self.y += self.speed
                
            if keys[pygame.K_d]:
                clear = 0
                for i in range(4):
                    zid = zidovi[i]
                    if pygame.Rect(self.rect.x + self.speed , self.rect.y, self.rect.width , self.rect.height).colliderect(zid) == False:
                        clear +=1
                if clear == 4:

                    self.x += self.speed
                
                self.pravac = "desno"
            if keys[pygame.K_a]:
                clear = 0
                for i in range(4):
                    zid = zidovi[i]
                    if pygame.Rect(self.rect.x -self.speed , self.rect.y , self.rect.width , self.rect.height).colliderect(zid) == False:
                        clear +=1
                if clear == 4:

                    self.x -= self.speed
                
                self.pravac = "levo"
            if(self.pravac == "desno"):
                self.picture = self.txt_player_right
            if(self.pravac == "levo"):
                self.picture = self.txt_player_left
    def draw(self , surface):
        surface.blit(self.picture , (self.x , self.y))


player = Player(50 , 50 ,-1,-1)