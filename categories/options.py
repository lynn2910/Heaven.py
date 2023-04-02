import pygame
from constants import *
from typing import List, Tuple


class Options:
    def __init__(self) -> None:
        
        self.FONT_40 = pygame.font.Font("./RetroGaming.ttf", 40)
        self.FONT_30 = pygame.font.Font("./RetroGaming.ttf", 30)
        self.FONT_25 = pygame.font.Font("./RetroGaming.ttf", 25)
        self.FONT_20 = pygame.font.Font("./RetroGaming.ttf", 20)
        
        self.esc_to_close = self.FONT_20.render("[ECHAP] pour quitter ce menu", True, (240, 240, 240))
        self.dev_mode = self.FONT_20.render("Mode développeur", True, (240, 240, 240))

        self.actual_page = 0
        self.MAX_PAGES = 1
        self.row_selected = 0
        self.MAX_SELECTED = 2

        self.key_cooldown = 0

        self.can_change_page = True

        # mode développeur
        self.show_dev_page = False
        self.DEV_KEYS = 0

    def draw(self, screen: pygame.Surface):
        screen_width, screen_height = screen.get_size()

        # Fond
        pygame.draw.rect(
            screen,
            (0, 0, 0, 0),
            (
                100,
                100,
                screen_width - 200,
                screen_height - 200
            ),
            border_radius=25
        )
        pygame.draw.rect(
            screen,
            (20, 20, 20),
            (
                100,
                100,
                screen_width - 200,
                self.esc_to_close.get_height() + 40
            ),
            border_top_left_radius=25,
            border_top_right_radius=25
        )

        # Instruction pour revenir en arrière
        screen.blit(self.esc_to_close, (145, 120))

        # Mode dev:
        if self.show_dev_page:
            screen.blit(
                self.dev_mode,
                (
                    screen_width - 145 - self.dev_mode.get_width(),
                    120
                )
            )


        #
        #   Dessin de la page
        # 
        # Catégories :
        # - Général (FPS, Coords, VSYNC)
        # - Dev(GRID, DEBUG_BACKGROUND, CASE_SIZE)
        #

        # Parties
        if self.actual_page == 0:
            # Général (FPS, Coords, VSYNC)
            x, y = 190, 190
            if self.row_selected == 0:
                self.draw_back_selection(screen, y, 5)
                self.checkbox(screen, (x, y), "VSYNC", VSYNC, color = (0,0,0))
            else:
                self.checkbox(screen, (x, y), "VSYNC", VSYNC, color = (255, 255, 255))
            y += CHECKBOX_SIZE + 10
            
            if self.row_selected == 1:
                self.draw_back_selection(screen, y, 5)
                self.checkbox(screen, (x, y), "TEST", False, color = (0,0,0))
            else:
                self.checkbox(screen, (x, y), "TEST", False, color = (255, 255, 255))



        # Draw pages
        if self.show_dev_page:
            pygame.draw.circle(
                screen,
                self.get_option_page_pos_color(0),
                (
                    screen_width // 2 - 15,
                    screen_height - 122
                ),
                9
            )
            pygame.draw.circle(
                screen,
                self.get_option_page_pos_color(1),
                (
                    screen_width // 2 + 15,
                    screen_height - 122
                ),
                9
            )
        else:
            pygame.draw.circle(
                screen,
                self.get_option_page_pos_color(0),
                (
                    screen_width // 2,
                    screen_height - 122
                ),
                9
            )
            

    def get_option_page_pos_color(self, page: int) -> Tuple[int, int, int]:
        if self.actual_page == page: return (230, 230, 230)
        else: return (90, 90, 90)

    def draw_back_selection(self, screen: pygame.Surface, y: int, margin: int):
        pygame.draw.rect(screen, (200, 200, 200), (100, y - margin, screen.get_width() - 200, CHECKBOX_SIZE + 5 + margin))

    def checkbox(self, screen: pygame.Surface, coords: Tuple[int, int], name: str, v: bool, color: Tuple[int, int, int]):
        checkbox = pygame.Surface((CHECKBOX_SIZE, CHECKBOX_SIZE))
        checkbox.fill((0,0,0))
        pygame.draw.rect(
            checkbox,
            color,
            (0, 0, CHECKBOX_SIZE, CHECKBOX_SIZE)
        )
        
        pygame.draw.rect(
            checkbox,
            (255 - color[0], 255 - color[1], 255 - color[2]),
            (4, 4, CHECKBOX_SIZE - 8, CHECKBOX_SIZE - 8)
        )

        if v:
            pygame.draw.rect(
                checkbox,
                color,
                (8, 8, CHECKBOX_SIZE - 16, CHECKBOX_SIZE - 16)
            )

        screen.blit(checkbox, coords)

        text = self.FONT_25.render(name, True, color)
        screen.blit(
            text,
            (
                coords[0] + CHECKBOX_SIZE + 20,
                coords[1] + 4
            )
        )

    def reset_options_interface(self):
        self.actual_page = 0
        self.row_selected = 0

    def update(self, frequence: pygame.time.Clock, delta: float):
        
        keys = pygame.key.get_pressed()
        if (not self.show_dev_page) and keys[pygame.K_h] and keys[pygame.K_e] and keys[pygame.K_a] and keys[pygame.K_v] and keys[pygame.K_n]:
            self.show_dev_page = True
            self.MAX_PAGES += 1

        if self.key_cooldown <= 0:
            self.key_cooldown = 0.2
            if keys[pygame.K_UP] or keys[pygame.K_z]:
                self.row_selected = ((self.row_selected - 1) % self.MAX_SELECTED)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.row_selected = ((self.row_selected + 1) % self.MAX_SELECTED)
        elif self.key_cooldown > 0:
            self.key_cooldown -= delta

    def key_down(self, event):
        self.key_cooldown = 0

        if (not self.show_dev_page) and event.key == pygame.K_t:
            self.DEV_KEYS += 1
            if self.DEV_KEYS >= 5:
                self.show_dev_page = True
                self.MAX_PAGES += 1

        if self.can_change_page and ((event.key == pygame.K_a) or (event.key == pygame.K_LEFT)):
            # changement de page vers la gauche
            self.actual_page = (self.actual_page + 1) % self.MAX_PAGES
        elif self.can_change_page and ((event.key == pygame.K_e) or (event.key == pygame.K_RIGHT)):
            # changement de page vers la droite
            self.actual_page = (self.actual_page - 1 + self.MAX_PAGES) % self.MAX_PAGES


options: Options = Options()
