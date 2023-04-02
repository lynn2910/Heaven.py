import pygame
from typing import List, Dict

from mod.assets import Assets
from entities.mod import Entity, EntityType
from mod.camera import *
from entities.player import Player
from mod.collisions import *


class EntitiesContainer:
    def __init__(self):
        self.dict = {}
        # chaque clé sera un type d'entité

    def add(self, entity_type: EntityType, entity: Entity):
        if not (entity_type in self.dict.keys()):
            self.dict[entity_type] = [entity]
        else:
            self.dict[entity_type].append(entity)

    def get(self, entity_type: EntityType, coords: Tuple[int, int]) -> Entity | None:
        if entity_type in self.dict.keys():
            for ent in self.dict[entity_type]:
                if (ent.x, ent.y) == coords:
                    return ent

    def get_all(self) -> dict[List[Entity]]:
        return self.dict


class Tile:
    def __init__(self, asset: str) -> None:
        self.asset = asset


class Layer:
    def __init__(self, y: int) -> None:
        self.map = {}
        self.entities = EntitiesContainer()
        self.y = y

    def insert(self, coords: Tuple[int, int], tile: Tile):
        if not (coords in self.map.keys()):
            self.map[coords] = tile

    def replace(self, coords: Tuple[int, int], tile: Tile):
        if coords in self.map.keys():
            self.map[coords] = tile

    def add_or_replace(self, coords: Tuple[int, int], tile: Tile):
        self.map[coords] = tile

    def remove(self, coords: Tuple[int, int]):
        del self.map[coords]

    def try_remove(self, coords: Tuple[int, int]):
        if coords in self.map.keys():
            self.remove(coords)


class ZoneType(Enum):
    TUTO = 0


class Zone:
    def __init__(self,
            map_background: pygame.Surface,
            layers: List[Tuple[int, pygame.Surface]] = [],
            collisions: List[Collision] = [],
            entities: Dict[int, List[Entity]] = []
        ) -> None:
        self.map = map_background
        self.layers = layers
        self.layers.sort(key=lambda l: l[0])
        self.collisions = collisions
        self.entities = entities

    def draw(self, screen: pygame.Surface, camera: Camera, player: Player, zone_decals: Tuple[int, int], assets: Assets, map) -> None:
        coords = (
            camera.x + (zone_decals[0] // 2),
            camera.y + (zone_decals[1] // 2)
        )

        # Dessin de la carte en fond
        screen.blit(self.map, coords)

        player_drawn = False

        if 0 in self.entities:
            # entities on this layer
            for entity in self.entities[0]:
                try:
                    entity.draw(screen, assets, camera)
                except:
                    pass

        for i, layer in self.layers:
            if (not player_drawn) and player.layer == i:
                player.draw(screen, assets, camera, map)
                # companion.draw(screen, assets, camera, map)
                player_drawn = True
            screen.blit(layer, coords)

            print(i, i in self.entities)
            # draw entities on this layer
            if i in self.entities:
                print(self.entities[i])
                # entities on this layer
                for entity in self.entities[i]:
                    try:
                        entity.draw(screen, assets, camera)
                    except:
                        pass

        if not player_drawn:
            player.draw(screen, assets, camera, map)
            # companion.draw(screen, assets, camera, map)

        player_x = (screen.get_width() // 2)
        player_y = (screen.get_height() // 2)

        player.draw_remaining_defense(player_x, player_y, screen, (CASE_SIZE // 2))
        player.draw_remaining_life(player_x, player_y, screen, (CASE_SIZE // 2))

        player.draw_current_item(screen, assets)


class Map:
    def __init__(self) -> None:
        self.layers = {}
        self.centered_assets = []  # ["rock1", "rock2"] # Place name of assets wich need to be drawed centered from the coordinates given

        self.zones: Dict[ZoneType, Zone] = {
            ZoneType.TUTO: Zone(
                pygame.transform.scale(pygame.image.load("assets/map/tuto_back_zone.png"), (400 * 4, 400 * 4)).convert_alpha(),
                [
                    (0, pygame.transform.scale(pygame.image.load("assets/map/tuto_top_zone.png"), (400 * 4, 400 * 4)).convert_alpha())
                ],
                collisions=[
                    # Murs
                    WallCollision(0, 0, CASE_SIZE, CASE_SIZE * 25), # Gauche
                    WallCollision(0, 0, CASE_SIZE * 8, CASE_SIZE), # Haut (partie gauche)
                    WallCollision(CASE_SIZE * 12, 0, CASE_SIZE * 13, CASE_SIZE), # Haut (partie droite)
                    WallCollision(CASE_SIZE * 24, 0, CASE_SIZE, CASE_SIZE * 25), # Droite
                    WallCollision(CASE_SIZE, CASE_SIZE * 24, CASE_SIZE * 25, CASE_SIZE), # Bas

                    # Cailloux
                    RockCollision(CASE_SIZE * 6 + 25, CASE_SIZE * 12.5 + 17),
                    RockCollision(CASE_SIZE * 6 + 25, CASE_SIZE * 17.5 + 17),
                    RockCollision(CASE_SIZE * 15 + 25, CASE_SIZE * 19.5 + 17),
                    RockCollision(CASE_SIZE * 17 + 25, CASE_SIZE * 13.5 + 17),
                    RockCollision(CASE_SIZE * 12 + 25, CASE_SIZE * 7.5 + 17),

                    # Troncs
                    TreeCollision(CASE_SIZE * 3 + (CASE_SIZE * 0.75), CASE_SIZE * 16), # Droite Milieu
                    TreeCollision(CASE_SIZE * 4 + (CASE_SIZE * 0.75), CASE_SIZE * 5), # Haut coin Gauche
                    TreeCollision(CASE_SIZE * 6 + (CASE_SIZE * 0.75), CASE_SIZE * 10), # Gauche Milieu
                    TreeCollision(CASE_SIZE * 22 + (CASE_SIZE * 0.75), CASE_SIZE * 13), # Droite extrème Milieu
                ],
                entities={
                    0: [
                        Entity((CASE_SIZE * 5, CASE_SIZE * 5), 10, EntityType.SPIRIT, "")
                    ]
                }
            )
        }

        self.actual_zone: Zone = self.zones[ZoneType.TUTO]
        self.zone_decals = ()
        self.DEFAULT_ZONE_DECALS = ()

    def add_layer(self, y: int) -> None:
        if not (y in self.layers.keys()):
            self.layers[y] = Layer(y)

    def remove_layer(self, y: int) -> None:
        if y in self.layers.keys():
            del self.layers[y]

    def get(self, y: int) -> Layer:  # | None
        if y in self.layers.keys():
            return self.layers[y]

    def get_layers(self):  # -> list[Layer]
        l = list(self.layers.values())
        l.sort()
        return l

    def get_available_layers(self):  # list[Layer]
        l = list(self.layers.values())
        l.sort(key=lambda l: l.y)
        return l

    def insert_tile(self, layer: int, coords: Tuple[int, int], tile: Tile):
        if layer in self.layers.keys():
            return self.layers[layer].insert(coords, tile)

    def add_entity(self, layer: int, type: EntityType, entity: Entity):
        if layer in self.layers.keys():
            return self.layers[layer].entities.add(type, entity)

    def replace_tile(self, layer: int, coords: Tuple[int, int], tile: Tile):
        if layer in self.layers.keys():
            return self.layers[layer].replace(coords, tile)

    def add_or_replace(self, layer: int, coords: Tuple[int, int], tile: Tile):
        if layer in self.layers.keys():
            return self.layers[layer].replace(coords, tile)

    def remove(self, layer: int, coords: Tuple[int, int]):
        if layer in self.layers.keys():
            return self.layers[layer].replace(coords)

    def try_remove(self, layer: int, coords: Tuple[int, int]):
        if layer in self.layers.keys():
            return self.layers[layer].replace(coords)

    def draw_grid(self, screen: pygame.Surface, camera: Camera) -> pygame.Surface:
        if not DRAW_DEBUG_GRID:
            return

        screen_width, screen_height = screen.get_size()

        for x_index in range(-CASE_SIZE, ((screen_width % CASE_SIZE) + CASE_SIZE)):
            x = x_index * CASE_SIZE + camera.x + (CASE_SIZE // 2)
            for y_index in range(-CASE_SIZE, ((screen_height % CASE_SIZE) + CASE_SIZE)):
                y = y_index * CASE_SIZE + camera.y + (CASE_SIZE // 4) - 4
                pygame.draw.line(
                    screen,
                    (20, 20, 20),
                    (x, y),
                    (x + screen_width, y),
                    2
                )
                pygame.draw.line(
                    screen,
                    (20, 20, 20),
                    (x, y),
                    (x, y + screen_height),
                    2
                )

    # def draw_zone(self, screen: pygame.Surface, assets: Assets, camera: Camera) -> None:
    #    asset = None
    #    if self.actual_zone == Zones.TUTO:
    #        asset = assets.get("map_tuto")
    #    
    #    if asset is None: return;

    #    screen.blit(
    #        asset,
    #        (
    #            camera.x + (self.zone_decals[0] // 2),
    #            camera.y + (self.zone_decals[1] // 2) 
    #        )
    #    )

    def draw(self, screen: pygame.Surface, assets: Assets, camera: Camera, player: Player) -> None:
        # self.draw_grid(screen, camera)
        # self.draw_zone(screen, assets, camera)

        self.actual_zone.draw(screen, camera, player, self.zone_decals, assets, self)
        return

        # test
        # rock = assets.get("rock1")
        # screen.blit(rock, (32, 32))
        screen_width, screen_height = screen.get_size()

        for layer in self.get_available_layers():
            # draw tiles
            items = layer.map.items()
            for (x, y), tile in items:
                # Nous calculons la coordonnée relative de la tuile
                x_pos, y_pos = (
                    x + camera.x + (screen_width // 2) - (CASE_SIZE // 2),
                    y + camera.y + (screen_height // 2) - (CASE_SIZE // 2) + (CASE_SIZE * layer.y)
                )

                # Cette valeur permettront de savoir si l'élément est affiché DANS l'écran
                #  x_encadrement = [camera.x, camera.x + (screen_width // 2)]
                #  y_encadrement = [camera.y, camera.y + (screen_height // 2)]

                # Si la surface est clairement en dehors de l'écran, on ne dessine pas pour optimiser les performances
                # if (y > y_encadrement[0] and y < y_encadrement[1]) and (x > x_encadrement[0] and x < x_encadrement[1]):
                # if  self.is_on_screen(camera.x, camera.y, screen_width, screen_height, x_pos, y_pos, CASE_SIZE, CASE_SIZE):
                if True:
                    surface = assets.get(tile.asset)
                    # Si la surface existe, alors on la dessine aux coordonnées calculées plus haut
                    if not (surface is None):
                        if DRAW_DEBUG_BACKGROUND:
                            pygame.draw.rect(screen, (0, 255, 0),
                                             (x_pos, y_pos, surface.get_width(), surface.get_height()))

                        if tile.asset in self.centered_assets:
                            assets.draw_centered(screen, surface, (x_pos, y_pos))
                        else:
                            screen.blit(surface, (x_pos, y_pos))

            # draw entities
            entities_layer = layer.entities.get_all().items()
            for _entity_type, entities in entities_layer:
                for entity in entities:
                    entity.draw(screen, assets, camera)
