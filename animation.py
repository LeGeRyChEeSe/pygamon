import pygame

class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name):
        super().__init__()
        self.sprite_sheet = load_sprite_sheet(name)
        self.image = get_image(self.sprite_sheet, 32, 0)
        self.current_image = 0
        self.direction = True
        self.way = []
        self.images = animations.get(name)

    def animation(self):
        if self.direction:
            self.current_image += 1
        else:
            self.current_image -= 1

        if self.current_image not in self.way:
            self.current_image = self.way[1]

        if self.current_image == self.way[2]:
            self.direction = False
        elif self.current_image == self.way[0]:
            self.direction = True

        self.image = self.images[self.current_image]
            

def load_sprite_sheet(name):
    sprite_sheet = pygame.image.load(f"{name}.png")
    return sprite_sheet

def get_image(sprite_sheet, x, y):
    image = pygame.Surface([32, 32])
    image.blit(sprite_sheet, (0, 0), (x, y, 32, 32))
    image.set_colorkey((0, 0, 0))
    return image


def load_animation_images(sprite_sheet):
    images = []
    for y in range(0, 128, 32):
        for x in range(0, 96, 32):
            images.append(get_image(sprite_sheet, x, y))
    return images

animations = {
    "player": load_animation_images(load_sprite_sheet("player"))
}