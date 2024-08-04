import pygame

class NPC:
    def __init__(self, x, y, atm_x, atm_y):
        self.x = x
        self.y = y
        self.atm_x = atm_x
        self.atm_y = atm_y
        self.speed = 2
        self.state = "walking_to_atm"

    def update(self):
        if self.state == "walking_to_atm":
            if self.x < self.atm_x:
                self.x += self.speed
            elif self.x > self.atm_x:
                self.x -= self.speed
            if self.y < self.atm_y:
                self.y += self.speed
            elif self.y > self.atm_y:
                self.y -= self.speed
            if abs(self.x - self.atm_x) < 5 and abs(self.y - self.atm_y) < 5:
                self.state = "at_atm"
        elif self.state == "at_atm":
            pygame.time.wait(2000)  # wait 2 seconds
            self.state = "walking_back"
        elif self.state == "walking_back":
            if self.x > self.initial_x:
                self.x -= self.speed
            elif self.x < self.initial_x:
                self.x += self.speed
            if self.y > self.initial_y:
                self.y -= self.speed
            elif self.y < self.initial_y:
                self.y += self.speed
            if abs(self.x - self.initial_x) < 5 and abs(self.y - self.initial_y) < 5:
                self.state = "walking_to_atm"

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 20, 20))



