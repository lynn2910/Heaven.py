from entities.mod import Entity, EntityType, Movement
import pygame
from constants import *
from typing import Tuple
from mod.inventory import *
from math import *
from mod.camera import Camera
from mod.utils import *
from mod.assets import *

class Player(Entity):
    def __init__(
            self,
            coords: Tuple[int, int] = PLAYER_START_COORDS,
            layer: int = 0,
            name: str = "Player",
            defense: int = DEFAULT_PLAYER_DEFENSE,
            life: int = DEFAULT_PLAYER_LIFE
        ) -> None:
            super().__init__(coords, life, EntityType.PLAYER, "")

            self.layer = 0
            self.DEFAULT_LAYER = 0
            
            self.DEFAULT_LIFE = life
            self.DEFAULT_DEFENSE = defense
            
            self.layer = layer
            self.name = name
            self.defense = defense
    
            self.idling = True
            self.ticks = 0
            self.fps = -1

            self.animation_frame = 0.0
            self.MAX_ANIMATION_FRAME = 3.0
            self.last_movement_tick = 0.0
            self.animation_ticks = 0.0

            self.inventory = Inventory()
            self.current_item = WoodSword()
            self.inventory_open = False

    def get_movement_animation(self) -> str:
        if self.idling or self.inventory_open:
            if self.movement == Movement.LEFT:
                return "player_left"
            elif self.movement == Movement.RIGHT:
                return "player_right"
            elif self.movement in [Movement.UP, Movement.UP_LEFT, Movement.UP_RIGHT]:
                return "player_top"
            else:
                return "player_bottom"
        elif not self.inventory_open:
            if self.movement == Movement.LEFT:
                return f"player_left_{floor(self.animation_frame)}"
            elif self.movement == Movement.RIGHT:
                return f"player_right_{floor(self.animation_frame)}"
            elif self.movement in [Movement.UP, Movement.UP_LEFT, Movement.UP_RIGHT]:
                return f"player_top_{floor(self.animation_frame)}"
            else:
                return f"player_bottom_{floor(self.animation_frame)}"
            
    def is_health_bars_needed(self, map, coords: Tuple[int, int]) -> bool:
        return True
    
    def draw_remaining_defense(self, x: int, y: int, screen: pygame.Surface, mid_adder: int):
        pygame.draw.rect(
            screen,
            (0,0,0),
            (
                x - 35 + mid_adder,
                y + 17 - 34 - mid_adder,
                70,
                9
            )
        )
        pygame.draw.rect(
            screen,
            PLAYER_SHIELD_COLOR,
            (
                x - 34 + mid_adder,
                y + 18 - 34 - mid_adder,
                floor(68 * (self.defense / self.DEFAULT_DEFENSE)),
                7
            )
        )
    
    def draw_remaining_life(self, x: int, y: int, screen: pygame.Surface, mid_adder: int):
        pygame.draw.rect(
            screen,
            (0,0,0),
            (
                x - 35 + mid_adder,
                y + 5 - 35 - mid_adder,
                70,
                9
            )
        )
        pygame.draw.rect(
            screen,
            PLAYER_LIFE_COLOR,
            (
                x - 34 + mid_adder,
                y + 6 - 35 - mid_adder,
                floor(68 * (self.life / self.DEFAULT_LIFE)),
                7
            )
        )

    def draw_current_item(self, screen: pygame.Surface, assets: Assets):
        return;
        # TODO

        # dessiner le cadre
        in_hand_asset = assets.get("in_hand")
        if not(in_hand_asset is None):
            screen.blit(
                in_hand_asset,
                (10, screen.get_height() - 10 - (in_hand_asset.get_height()))
            )

        # dessiner l'item
        if not(self.current_item is None):
            current_item_surface = assets.get(self.current_item.asset)
            if not(current_item_surface is None):
                
                #pygame.draw.rect(
                #    screen,
                #    (255, 0, 0),
                #    (
                #    10 + (124 - in_hand_asset.get_width()) + (in_hand_asset.get_width() // 4),
                #    screen.get_height() - 10 - (124 - in_hand_asset.get_height()) - (in_hand_asset.get_height()) - (124 // -4),
                #    64, 64
                #    )
                #)

                screen.blit(
                    current_item_surface,(
                        10 + (124 - in_hand_asset.get_width()) + (in_hand_asset.get_width() // 4),
                        screen.get_height() - 10 - (124 - in_hand_asset.get_height()) - (in_hand_asset.get_height()) - (124 // -4)
                    )
                )

    def draw(self, screen: pygame.Surface, assets: Assets, camera: Camera, map):
        player_surface = assets.get(self.get_movement_animation())
        if not (player_surface is None):
            x = (screen.get_width() // 2) - (CASE_SIZE // 2) + (player_surface.get_width() // 2)
            y = (screen.get_height() // 2) - (CASE_SIZE // 2) - (player_surface.get_height() // 2)
            if player_surface.get_height() > CASE_SIZE:
                # Joueur plus grand
                # Il faut le décaler sur la hauteur
                y += CASE_SIZE - (player_surface.get_height() // 4)
            screen.blit(player_surface, (x, y))
    
    def move(self, movement: Movement, vector: Tuple[int, int], camera: Camera, delta: float):
        if self.inventory_open:
            return

        self.last_movement_tick = self.ticks + delta

        if movement != self.movement:
            self.movement = movement
        
        if self.idling:
            self.idling = False
        
        self.x += vector[0]
        camera.x += vector[0]
        
        self.y += vector[1]
        camera.y += vector[1]
    
    def update(self, frequence: pygame.time.Clock, delta: float):
        self.fps = frequence.get_fps()
        
        self.animation_ticks += delta
        
        if not self.idling:
            self.ticks += delta

        if self.animation_ticks >= PLAYER_ANIMATION_RATE: # On vérifie que c'est un nombre entier
            self.animation_frame = (self.animation_frame + 1) % self.MAX_ANIMATION_FRAME
            self.animation_ticks = 0

        if (self.ticks - self.last_movement_tick >= PLAYER_ANIMATION_RATE) and (not self.idling):
            self.idling = True
            self.ticks = 0