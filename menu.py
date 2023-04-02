import pygame
from math import *
from constants import *
from enum import Enum
from categories.options import options


class GameStatus(Enum):
    MENU = 0
    GAME = 1


class Menu:
    def __init__(self):
        self.MENU_FONT = pygame.font.Font("./RetroGaming.ttf", 40)

        self.text = self.MENU_FONT.render("Menu", True, (240, 240, 240))
        self.text_surface = self.text.get_rect()

        # self.START_FONT = pygame.font.Font("./RetroGaming.ttf", 30)
        # self.start = self.START_FONT.render("[press 'space' to start]", True, (240, 240, 240))
        # self.start_surface = self.start.get_rect()

        self.category = 0
        self.space_between = 75
        self.key_cooldown = 0

        self.ctg_open = MenuCategories.NO_ONE

        self.background = pygame.image.load("assets/ui/menu_background.png").convert_alpha()

    def draw_background(self, screen: pygame.Surface):
        surface = pygame.transform.scale(self.background, screen.get_size())
        screen.blit(surface, (0, 0))

    def draw(self, screen: pygame.Surface):
        # screen.fill("#1c1e26")
        self.draw_background(screen)

        if self.ctg_open == MenuCategories.OPTIONS:
            return options.draw(screen)
        # elif self.ctg_open == MenuCategories.COMMANDS:
        #    return commands.draw(screen)
        # elif self.ctg_open == MenuCategories.SUCCES:
        #    return success.draw(screen)

        (display_width, display_height) = screen.get_size()

        if self.category == 0:
            new_game_ctg = self.MENU_FONT.render("Nouvelle partie", True, (240, 0, 0))
            screen.blit(new_game_ctg,
                        (floor(display_width // 2) - (new_game_ctg.get_width() // 2), floor(display_height // 4)))
        else:
            new_game_ctg = self.MENU_FONT.render("Nouvelle partie", True, (0, 0, 0))
            screen.blit(new_game_ctg,
                        (floor(display_width // 2) - (new_game_ctg.get_width() // 2), floor(display_height // 4)))

        if self.category == 1:
            new_game_ctg = self.MENU_FONT.render("Charger une partie", True, (240, 0, 0))
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 4) + self.space_between))
        else:
            new_game_ctg = self.MENU_FONT.render("Charger une partie", True, (0, 0, 0))
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 4) + self.space_between))

        if self.category == 2:
            new_game_ctg = self.MENU_FONT.render("Options", True, (240, 0, 0))
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 4) + self.space_between * 2))
        else:
            new_game_ctg = self.MENU_FONT.render("Options", True, (0, 0, 0))
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 4) + self.space_between * 2))

        if self.category == 3:
            new_game_ctg = self.MENU_FONT.render("Succès", True, (240, 0, 0))
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 4) + self.space_between * 3))
        else:
            new_game_ctg = self.MENU_FONT.render("Succès", True, (0, 0, 0))
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 4) + self.space_between * 3))

        if self.category == 4:
            new_game_ctg = self.MENU_FONT.render("Quitter", True, (240, 0, 0))
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 4) + self.space_between * 4))
        else:
            new_game_ctg = self.MENU_FONT.render("Quitter", True, (0, 0, 0))
            screen.blit(new_game_ctg, (floor(display_width // 2) - (new_game_ctg.get_width() // 2),
                                       floor(display_height // 4) + self.space_between * 4))

    def update(self, frequence: pygame.time.Clock, delta: float, screen: pygame.Surface):
        if self.ctg_open == MenuCategories.OPTIONS:
            return options.update(frequence, delta)

        # Get keyboard keys
        keys = pygame.key.get_pressed()
        if self.key_cooldown <= 0:
            self.key_cooldown = 0.25
            if keys[pygame.K_UP] or keys[pygame.K_z]:
                self.category = ((self.category - 1) % 5)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.category = ((self.category + 1) % 5)
        elif self.key_cooldown > 0:
            self.key_cooldown -= delta

    #
    #
    #       Control
    #
    #

    def options_control_key_down(self, event: pygame.event.Event):
        if event.key == pygame.K_ESCAPE:
            if self.ctg_open == MenuCategories.OPTIONS:
                options.reset_options_interface()
                self.ctg_open = MenuCategories.NO_ONE

    def key_down(self, event: pygame.event.Event, engine):

        if self.ctg_open == MenuCategories.OPTIONS:
            options.key_down(event)
            self.options_control_key_down(event)
            return

        self.key_cooldown = 0

        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.category == 0:
                engine.status = GameStatus.GAME
            elif self.category == 2:
                self.ctg_open = MenuCategories.OPTIONS
            elif self.category == 4:
                engine.exit()

    def key_up(self, event: pygame.event.Event, engine):
        pass

    def mouse_btn_up(self, event: pygame.event.Event, engine):
        pass

    def mouse_btn_down(self, event: pygame.event.Event, engine):
        pass

    def mouse_move(self, event: pygame.event.Event, engine):
        pass
