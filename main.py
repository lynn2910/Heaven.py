import pygame

pygame.font.init()

from constants import *
from menu import Menu, GameStatus
from game import Game

class GameEngine:
    """Le gestionnaire du jeux"""
    def __init__(self):
        """
        Nous définissons toutes les variables qui seront utiles au jeux
        Principalement:
        - status: GameStatus; Utilisé pour savoir si nous sommes dans le menu ou en jeux
        - running: bool; Utilisé par la boucle du jeux (voir plus bas)
        - menu: Menu; Une class utilisée pour gérer les mises à jours/interactions/le comportement/l'interface du menu à l'entrée du jeu
        - game: Game; Contient le jeux, similaire à la class Menu
        - fullscreen: bool; Définit si le jeux est en plein écran ou non (utilisé dans la fonction "key_down")
        - display: 
        """
        self.status = GameStatus.MENU
        self.running = True
        self.LAST_FRAME = 0

        self.setup()

        self.menu = Menu()
        self.game = Game(self.display)

        self.run()
    
    def setup(self):
        pygame.init()
        pygame.font.init()

        monitor_info = pygame.display.Info()

        self.fullscreen = False
        self.display = pygame.display.set_mode((monitor_info.current_w, monitor_info.current_h), pygame.RESIZABLE, display=0) # Créer la fenêtre du jeu

        pygame.display.set_caption("Heaven")
        self.frequence = pygame.time.Clock()
    
    def draw(self):
        if self.status == GameStatus.MENU:
            self.menu.draw(self.display)
        elif self.status == GameStatus.GAME:
            self.game.draw(self.display, self.frequence.get_fps())
        else:
            self.display.fill((0, 0, 0))

    def update(self):
        # get delta
        t = pygame.time.get_ticks()
        delta = (t - self.LAST_FRAME) / 1000.0
        self.LAST_FRAME = t
        
        if self.status == GameStatus.MENU:
            self.menu.update(self.frequence, delta, self.display)
        elif self.status == GameStatus.GAME:
            self.game.update(self.frequence, delta)

    def exit(self):
        self.running = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            
            elif event.type == pygame.KEYDOWN: # Si la touche est appuyée

                # Plein écran ou non s
                if event.key == pygame.K_F11:
                    if not self.fullscreen:
                        monitor_info = pygame.display.Info()

                        self.fullscreen = True
                        pygame.display.quit()
                        self.display = pygame.display.set_mode((monitor_info.current_w, monitor_info.current_h), flags = pygame.RESIZABLE and pygame.FULLSCREEN, vsync=1)
                        pygame.display.init()
                    else:
                        monitor_info = pygame.display.Info()

                        self.fullscreen = False
                        pygame.display.quit()
                        self.display = pygame.display.set_mode((monitor_info.current_w, monitor_info.current_h), flags = pygame.RESIZABLE, vsync=1)
                        pygame.display.init()
                    


                if self.status == GameStatus.MENU:
                    self.menu.key_down(event, self)
                elif self.status == GameStatus.GAME:
                    self.game.key_down(event, self)
            
            elif event.type == pygame.KEYUP: # Si la touche est relachée
                if self.status == GameStatus.MENU:
                    self.menu.key_up(event, self)
            
            elif event.type == pygame.MOUSEBUTTONDOWN: # Si le  bouton de la souris est appuyé
                if self.status == GameStatus.MENU:
                    self.menu.mouse_btn_down(event, self)
            
            elif event.type == pygame.MOUSEBUTTONUP: # Si le bouton de la souris est relachée 
                if self.status == GameStatus.MENU:
                    self.menu.mouse_btn_up(event, self)

            elif event.type == pygame.MOUSEMOTION: # Si la souris bouge
                if self.status == GameStatus.MENU:
                    self.menu.mouse_move(event, self)
            
            elif event.type == pygame.VIDEORESIZE:
                # La fenêtre ne fait plus la même taille
                self.game.map.zone_decals = self.display.get_size()

    def run(self):
        while self.running:
            self.events()
            self.update()
            
            self.draw()
            pygame.display.update()

            self.frequence.tick(TICKS_PER_SECONDS)
        
        
        print("Good bye!")

engine = GameEngine()