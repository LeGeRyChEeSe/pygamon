import pygame
import animation

class Player(animation.AnimateSprite):

    def __init__(self, x, y):
        super().__init__("player")
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 6)
        self.old_position = self.position.copy()
        self.speed = 2

    def save_location(self): self.old_position = self.position.copy()

    def move_right(self): 
        self.position[0] += self.speed
        self.way = [6, 7, 8]
        self.animation()

    def move_left(self): 
        self.position[0] -= self.speed
        self.way = [3, 4, 5]
        self.animation()

    def move_up(self): 
        self.position[1] -= self.speed
        self.way = [9, 10, 11]
        self.animation()

    def move_down(self): 
        self.position[1] += self.speed
        self.way = [0, 1, 2]
        self.animation()

    
    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    