import pygame


class Player:
    def __init__(self  , x , y ):
        self.x = x
        self.y = y
        self.speed = 5
        self.pravac = "desno"
        self.txt_player_left = pygame.image.load("images\\player.png")
        self.txt_player_right =pygame.image.load("images\\playerright.png")
        self.txt_player_left = pygame.transform.scale(self.txt_player_left , (45 , 65))
        self.txt_player_right = pygame.transform.scale(self.txt_player_right , (45 , 65))
        self.picture = self.txt_player_right
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
            self.pravac = "desno"
        if keys[pygame.K_a]:
            self.x -= self.speed
            self.pravac = "levo"
        if(self.pravac == "desno"):
            self.picture = self.txt_player_right
        if(self.pravac == "levo"):
            self.picture = self.txt_player_left
    def draw(self , surface):
        surface.blit(self.picture , (self.x , self.y))


player = Player(50 , 50 )