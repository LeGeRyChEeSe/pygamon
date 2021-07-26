import pygame
import copy

class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name):
        super().__init__()
        self.sprite_sheet = sprite_sheet
        self.image = get_image(self.sprite_sheet, 32, 0)
        self.default_image = self.image
        self.current_image = 0
        self.way = True
        self.images = animations
        self.timer = 0
        self.clock = pygame.time.get_ticks()

    def animation(self, direction: str):
        print(self.clock, self.timer)

        if self.timer < 250:
            self.timer += pygame.time.get_ticks() - self.clock
        else:
            self.clock = pygame.time.get_ticks()
            self.timer = 0
            if self.way:
                self.current_image += 1
            else:
                self.current_image -= 1
            
            if direction == "down":
                image = self.images.get("player_down")
            elif direction == "left":
                image = self.images.get("player_left")
            elif direction == "right":
                image = self.images.get("player_right")
            elif direction == "up":
                image = self.images.get("player_up")

            if self.current_image == 2:
                self.way = False
            elif self.current_image == 0:
                self.way = True

            self.default_image = image[1]
            self.current_image = self.current_image % len(image)
            self.image = image[self.current_image]


def load_sprite_sheet(name):
    sprite_sheet = pygame.image.load(f"{name}.png")
    return sprite_sheet

def get_image(sprite_sheet, x, y):
    image = pygame.Surface([32, 32])
    image.blit(sprite_sheet, (0, 0), (x, y, 32, 32))
    image.set_colorkey((0, 0, 0))
    return image

def load_animation_images(sprite_sheet, x:int, y:int, step:int):
    images = []
    for _x in range(0, x, step):
        images.append(get_image(sprite_sheet, _x, y))
    return images

sprite_sheet = load_sprite_sheet("player")

animations = {
    "player_down": load_animation_images(sprite_sheet, 96, 0, 32),
    "player_left": load_animation_images(sprite_sheet, 96, 32, 32),
    "player_right": load_animation_images(sprite_sheet, 96, 64, 32),
    "player_up": load_animation_images(sprite_sheet, 96, 96, 32),
}

print(animations)