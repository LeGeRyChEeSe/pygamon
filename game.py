from player import Player
import pygame
import pygame.key as key
import pytmx
import pyscroll

class Game:
    def __init__(self):
        # Créer la fenêtre du jeu
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pygamon - Aventure")

        # Charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        self.map = 'world'

        # Générer un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # Définir une liste qui va stocker les rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        self.group.add(self.player)

        # Définir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

    def handle_input(self):
        pressed = key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
        if pressed[pygame.K_DOWN]:
            self.player.move_down()
        if pressed[pygame.K_LEFT]:
            self.player.move_left()
        if pressed[pygame.K_RIGHT]:
            self.player.move_right()
        
    def switch_house(self):
        # Charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Définir une liste qui va stocker les rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        self.group.add(self.player)

        # Définir le rectangle de collision pour sortir de la maison
        enter_house_rect = tmx_data.get_object_by_name('exit_house')
        self.enter_house_rect = pygame.Rect(enter_house_rect.x, enter_house_rect.y, enter_house_rect.width, enter_house_rect.height)

        # Récupérer le point de spawn dans la maison
        spawn_house_point = tmx_data.get_object_by_name('spawn_house')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 20

    def switch_world(self):
        # Charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Définir une liste qui va stocker les rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        self.group.add(self.player)

        # Définir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # Récupérer le point de spawn devant la maison
        spawn_house_point = tmx_data.get_object_by_name('enter_house_exit')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y + 20
    
    def update(self):
        self.group.update()

        # Vérifier l'entrée dans la maison
        if self.map == 'world' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = 'house'

        # Vérifier la sortie de la maison
        elif self.map == 'house' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()
            self.map = 'world'

        # Vérification des collisions
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()


    def run(self):

        clock = pygame.time.Clock()


        # Boucle du jeu
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()