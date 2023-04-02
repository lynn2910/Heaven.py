from math import *
from typing import List, Tuple
from enum import Enum

import pygame

from mod.assets import Assets
from mod.camera import *
from constants import *
from mod.utils import *

class Movement(Enum):
    UP = 0
    UP_RIGHT = 1
    UP_LEFT = 2
    LEFT = 3
    RIGHT = 4
    BOTTOM_RIGHT = 5
    BOTTOM_LEFT = 6
    BOTTOM = 7

class EntityType(Enum):
    PLAYER = 0
    SPIRIT = 1
    COMPANION = 2

def determine_collision_move(movement: Movement, axe: 0 | 1) -> Movement | None:
    """
    permet de savoir si l'axe demandé est dans le mouvement
    0 = x
    1 = y
    """
    if (movement in [Movement.UP, Movement.BOTTOM]):
        if axe == 0: return None
        else: return movement
    elif (movement in [Movement.RIGHT, Movement.LEFT]):
        if axe == 0: return movement
        else: return None
    elif (movement == Movement.UP_RIGHT):
        if axe == 0: return Movement.RIGHT
        else: return Movement.UP
    elif (movement == Movement.UP_LEFT):
        if axe == 0: return Movement.LEFT
        else: return Movement.UP
    elif (movement == Movement.BOTTOM_LEFT):
        if axe == 0: return Movement.LEFT
        else: return Movement.BOTTOM
    elif (movement == Movement.BOTTOM_RIGHT):
        if axe == 0: return Movement.RIGHT
        else: return Movement.BOTTOM

def determine_move(vec: Tuple[int, int]) -> Movement:
    if vec[0] > 0 and vec[1] == 0:
        return Movement.RIGHT
    elif vec[0] < 0 and vec[1] == 0:
        return Movement.LEFT
    elif vec[0] == 0 and vec[1] > 0:
        return Movement.UP
    elif vec[0] == 0 and vec[1] < 0:
        return Movement.BOTTOM
    elif vec[0] < 0 and vec[1] < 0:
        return Movement.BOTTOM_LEFT
    elif vec[0] > 0 and vec[1] < 0:
        return Movement.BOTTOM_RIGHT
    elif vec[0] < 0 and vec[1] > 0:
        return Movement.UP_LEFT
    elif vec[0] > 0 and vec[1] < 0:
        return Movement.UP_RIGHT
    else:
        return Movement.BOTTOM

class Entity:
    def __init__(self, coords: Tuple[int, int], life: int,  type: EntityType, asset: str = "") -> None:
        self.x = coords[0]
        self.y = coords[1]

        self.life = life
        self.type = type
        self.asset = asset

        self.movement = Movement.BOTTOM

    def move_x(self, x: int) -> None:
        self.x += x

    def move_y(self, y: int) -> None:
        self.y += y

    def draw(self, screen: pygame.Surface, assets: Assets, camera: Camera):
        coords = (
            self.x + (screen.get_width() // 2) - (CASE_SIZE // 2) + camera.x,
            self.y + (screen.get_height() // 2) - (CASE_SIZE // 2) + camera.y
        )

        pygame.draw.rect(screen, (255, 255, 255), (coords[0], coords[1], CASE_SIZE, CASE_SIZE))