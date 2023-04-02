from enum import Enum
from math import floor
import pygame
from typing import List, Tuple

class CinematicAsset:
    def __init__(
            self,
            name: str,
            asset: pygame.Surface,
            start: float,
            end: float,
            center: bool,
            coords: Tuple[float, float] = (0,0),
        ) -> None:
        self.name = name
        self.asset = asset
        self.start = start
        self.end = end

        self.center = center
        self.coords = coords

    def is_middled(self, ticks: float):
        """
        Renvoit une boolean pour savoir si les ticks sont entre les propriétés start et end

        Utilise le théorème des valeurs intermédiaires
        """
        return self.start <= ticks <= self.end

    def draw(self, screen: pygame.Surface, ticks: float) -> None:
        if not self.center:
            screen.blit(self.asset, self.coords)
        else:
            # On récupère la taille de l'écran
            sw, ss = screen.get_size()
            if sw >= self.asset.get_width() and ss >= self.asset.get_height():
                screen.blit(self.asset, self.coords)
            else:
                screen.blit(
                    self.asset,
                    (
                        -(self.asset.get_width() - sw),
                        -(self.asset.get_height() - ss)
                    )
                )
        
class Position(Enum):
    """
    Précise la position du text
    """
    BOTTOM = 0
    MIDDLE = 1
    UP = 2

class CinematicText:
    def __init__(
        self,
        name: str,
        asset: pygame.Surface,
        start: float,
        end: float,
        animation_duration = 0.05,
        center: bool = True,
        position: Position = Position.MIDDLE,
        coords: Tuple[float, float] = (0,0)
    ) -> None:
        """
        Propriétés passées en arguments:
        identiques à CinematicAsset, sauf:
        - animation_duration: durée de l'animation de sortie (descente et transparence modifiée)
        - position: Précise la position du texte

        /!\ ATTENTION: les valeurs "start" et "end" doivent inclures le temps de l'animation !!!
        """
        self.name = name
        self.asset = asset
        self.ALPHA = self.asset.get_alpha()
        self.start = start
        self.end = end

        self.center = center
        self.coords = coords

        self.animation_duration = animation_duration
        self.position = position

    def is_middled(self, ticks: float):
        """
        Renvoit une boolean pour savoir si les ticks sont entre les propriétés start et end

        Utilise le théorème des valeurs intermédiaires
        """
        return self.start <= ticks <= self.end
    
    def detect_animation(self, ticks: float) -> 0 | 1 | 2:
        """
        Renvoit le statut de l'animation
        0 = animation de début
        1 = pas d'animation
        2 = animation de fin
        """
        if self.start + self.animation_duration >= ticks: return 0
        elif self.end - self.animation_duration >= ticks: return 2
        else: return 1

    def draw(self, screen: pygame.Surface, ticks: float) -> None:
        if not self.center:
            screen.blit(self.asset, self.coords)
        else:
            # On récupère la taille de l'écran
            sw, sh = screen.get_size()

            x, y = (
                (sw // 2) - (self.asset.get_width() // 2) + self.coords[0],
                (sh // 2) - (self.asset.get_height() // 2) + self.coords[1]  
            )

            if self.position == Position.BOTTOM:
                y += sh // 4
            elif self.position == Position.UP:
                y -= sh // 4


            # On gère les animations
            # TODO
            animation = self.detect_animation(ticks)

            if animation < 1:
                # Start
                self.asset.set_alpha(
                    255 / ((ticks + self.animation_duration) - ticks)
                )

            # if animation < 1:
            #     #y -= ((sh - x) / (ticks - self.start)) * (1 - self.out_in_animation_duration)
            #     self.asset.set_alpha(floor(255 / ((ticks + self.out_in_animation_duration))))
            # elif animation > 1:
            #     y += ((sh - x) / (ticks - self.start)) * (1 - self.out_in_animation_duration)

            # On dessine le text
            screen.blit(self.asset, (x, y))

class CinematicID(Enum):
    BEGINNING = 0
    
class Cinematic:
    """
    Moteur permettant de gérer les cinematiques
    """
    def __init__(
        self,
        assets: List[CinematicAsset],
        texts: List[Tuple[str, float, float, pygame.Surface, Tuple[float, float]]],
        max_timeline: float,
        fill: bool = False,
        fill_color: Tuple[int, int, int] = (0,0,0)
    ) -> None:
        """
        Propriétés passées en arguments:
        - assets: Contient une liste de tuples composé d'un string (nom utilisé en tant qu'identifiant), de deux nmbres flottants (début et fin) ainsi que d'une Surface pygame, et pour finir une boolean pour savoir si on doit centrer ou les coordonnées du coin en haut à gauche
        - texts: Même concept que les assets mais la Surface est le texte, et un tuple précise des coordonnées relatives du centre de l'écran ((0.5, 0.5) donne le centre de l'écran)
        - max_timeline: Le nombre de millisecondes pendant lequel la cinématique dure.
        """
        
        self.assets = assets
        
        self.texts = texts
        self.max_timeline = max_timeline

        self.ticks = 0

        self.pause = False

        self.started = False

        self.fill = fill
        self.fill_color = fill_color

        self.FONT_30 = pygame.font.Font("./RetroGaming.ttf", 30)
        self.FONT_20 = pygame.font.Font("./RetroGaming.ttf", 20)

        self.pause_text = self.FONT_30.render("[PAUSE]", True, (255, 255, 255))
        self.exit_cin_text = self.FONT_20.render("Quitter la cinématique", True, (255, 255, 255))

        self.exit_ticks = 0.0
        self.MAX_EXIT_TICKS = 2.0

    def is_ended(self):
        return (self.max_timeline <= self.ticks)

    def update(self, frequence: pygame.time.Clock, delta: float) -> None:
        """
        Propriétés passées en arguments:
        - frequence: Horloge du moteur de jeux; Permet d'accéder au nombre d'image par secondes, le nombre de ticks etc...
        - delta: un nombre exprimant le temps écoulé entre la dernière mise à jour et la mise à jour présente; Bien souvent un nombre très faible (0.009 par exemple).
        """
        # Si la cinématique est finie, alors on ne va pas plus loin
        if self.is_ended(): return

        if not self.pause:
            # La cinématique n'est pas en pause
            self.ticks += delta

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.exit_ticks += delta
        
        if not keys[pygame.K_e] and self.exit_ticks != 0:
            self.exit_ticks = 0
        elif self.MAX_EXIT_TICKS <= self.exit_ticks:
            # On met les ticks au dela du maximum
            self.ticks = self.max_timeline + 1.0

    def key_down(self, event: pygame.event.Event):
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
            self.pause = not self.pause

    def draw(self, screen: pygame.Surface) -> None:
        # Si la cinématique est terminée, on ne dessine rien car c'est inutile
        if self.is_ended(): return;

        # Fond en noir :D
        screen.fill(self.fill_color)
        
    
        # Nous dessinons les assets (aussi appelés les fonds)
        for asset in self.assets:
            if asset.is_middled(self.ticks):
                asset.draw(
                    screen,
                    self.ticks
                )


        # Puis les textes...
        for text in self.texts:
            if text.is_middled(self.ticks):
                text.draw(screen, self.ticks)

        if self.pause or self.exit_ticks != 0:
            # Add background
            back_surface = pygame.Surface(screen.get_size())
            back_surface.set_alpha(191) # 75% opaque
            back_surface.fill((0,0,0))

            screen.blit(back_surface, (0,0))
        
        if self.pause:
            # Add text
            screen.blit(
                self.pause_text,
                (
                    screen.get_width() // 2 - (self.pause_text.get_width() // 2),
                    screen.get_height() // 2 - (self.pause_text.get_height() // 2),
                )
            )

        if self.exit_ticks != 0:
            # On essaie de quitter la cinématique
            screen.blit(
                self.exit_cin_text,
                (
                    screen.get_width() - self.exit_cin_text.get_width() - 100,
                    screen.get_height() - self.exit_cin_text.get_height() - 100,
                )
            )
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (
                    screen.get_width() - self.exit_cin_text.get_width() - 100,
                    screen.get_height() - self.exit_cin_text.get_height() - 65,
                    floor(self.exit_cin_text.get_width() * (self.exit_ticks / self.MAX_EXIT_TICKS)),
                    7
                )
            )