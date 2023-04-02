from entities.companion import Companion
from menu import GameStatus
from mod.assets import GameAssets
from mod.cinematic import Cinematic, CinematicAsset, CinematicID, CinematicText, Position
from mod.ui import *
from entities.mod import *
from mod.map import *
from mod.camera import *
from mod.save import convert_tiled_to_map, open_file
from mod.inventory import Wood

#
#
#       GAME
#
#


class Game:
    def __init__(self, screen: pygame.Surface) -> None:
        map_json = open_file("map.json")
        self.map = convert_tiled_to_map(map_json, screen)  # Map()
        self.camera = Camera()
        self.assets = GameAssets()
        self.assets.load_images()
        self.ui_assets = UiAssets()

        # resizing window
        self.map.zone_decals = screen.get_size()
        self.map.DEFAULT_ZONE_DECALS = screen.get_size()

        # TEST

        """

        self.map.add_layer(0)
        self.map.insert_tile(0, (0, 0), Tile("test_grass"))
        self.map.insert_tile(0, (-CASE_SIZE*1.5, 0), Tile("rock1"))
        self.map.insert_tile(0, (CASE_SIZE, 2 * CASE_SIZE), Tile("rock2"))

        self.map.add_entity(0, SpriteType.SPIRIT, Spirit(CASE_SIZE * 2, CASE_SIZE))

        """

        # Blep
        self.player = Player()
        
        # TODO
        # self.companion = Companion(self.player.x - (CASE_SIZE * 0.86), self.player.y - (CASE_SIZE * 0.86))

        self.player.inventory.add_item(Wood())

        print(self.player.inventory)

        self.ui = UI()

        # Menu affiché quand on appuie sur [ECHAP]
        self.is_escaped = False
        self.ESC_FONT = pygame.font.Font("./RetroGaming.ttf", 40)
        self.PAUSE_ESC_FONT = pygame.font.Font("./RetroGaming.ttf", 25)
        self.IN_DEV = pygame.font.Font("./RetroGaming.ttf", 15)
        self.esc_menu_ctg = 0
        self.space_between = 75
        self.key_cooldown = 0

        # Gestion des cinématiques
        self.cinematics = {
            CinematicID.BEGINNING: Cinematic(
                [
                    CinematicAsset(
                        "test",
                        pygame.image.load("assets/ui/cloud_2.png"),
                        0,
                        19,
                        True,
                        (0,0)
                    )
                ],
                [
                    CinematicText(
                        "1",
                        self.ESC_FONT.render("Elle était tout pour moi...", True, (0,0,0)),
                        0.5 - 0.15,
                        4.5 + 0.15,
                        center=True,
                        coords=(0,100),
                        position=Position.BOTTOM
                    ),
                    CinematicText(
                        "2",
                        self.ESC_FONT.render("...jusqu'à ce moment.", True, (0,0,0)),
                        4.5 - 0.15 + 1,
                        9 + 0.15 + 1,
                        center=True,
                        coords=(0,100),
                        position=Position.BOTTOM
                    ),
                    CinematicText(
                        "3",
                        self.ESC_FONT.render("Kady, me voilà.", True, (0,0,0)),
                        9 + 0.15 + 2,
                        14 + 0.15 + 2,
                        center=True,
                        coords=(0,100),
                        position=Position.BOTTOM
                    )
                ],
                19
            )
        }

        # TODO
        self.run_cinematic = True
        self.actual_cinematic = CinematicID.BEGINNING


    def draw_esc_menu(self, screen: pygame.Surface, fps: int) -> None:
        if not self.is_escaped: return;

        # On rajoute un fond légèrement noir
        back_surface = pygame.Surface(screen.get_size())
        back_surface.set_alpha(191) # 75% opaque

        back_surface.fill((0,0,0))

        screen.blit(back_surface, (0,0))

        # On dessine les catégories
        # Catégories:
        # - Retour en jeu
        # - Options
        # - Contrôles
        # - Quitter la partie
        # - Quitter le jeux

        (screen_width, screen_height) = screen.get_size()

        # [PAUSE]
        pause_top_text = self.PAUSE_ESC_FONT.render("[PAUSE]", True, (240, 240, 240))
        screen.blit(pause_top_text, (floor((screen_width // 2) - (pause_top_text.get_width() // 2)), floor(self.space_between)))

        
        # Retour en jeu
        if self.esc_menu_ctg == 0:
            retrun_in_game = self.ESC_FONT.render("Retour en jeu", True, (240, 0, 0))
            screen.blit(retrun_in_game, (floor(screen_width // 2) - (retrun_in_game.get_width() // 2), floor(screen_height // 2) - self.space_between * 2.5))
        else:
            retrun_in_game = self.ESC_FONT.render("Retour en jeu", True, (255, 255, 255))
            screen.blit(retrun_in_game, (floor(screen_width // 2) - (retrun_in_game.get_width() // 2), floor(screen_height // 2) - self.space_between * 2.5))

        # Options
        if self.esc_menu_ctg == 1:
            opt_ctg = self.ESC_FONT.render("Options", True, (240, 0, 0))
            screen.blit(opt_ctg, (floor(screen_width // 2) - (opt_ctg.get_width() // 2), floor(screen_height // 2) - self.space_between * 1.5))
        else:
            opt_ctg = self.ESC_FONT.render("Options", True, (255, 255, 255))
            screen.blit(opt_ctg, (floor(screen_width // 2) - (opt_ctg.get_width() // 2), floor(screen_height // 2) - self.space_between * 1.5))

        
        # Contrôles
        if self.esc_menu_ctg == 2:
            cntrl_ctg = self.ESC_FONT.render("Contrôles", True, (240, 0, 0))
            screen.blit(cntrl_ctg, (floor(screen_width // 2) - (cntrl_ctg.get_width() // 2), floor(screen_height // 2) - self.space_between * 0.5))
        else:
            cntrl_ctg = self.ESC_FONT.render("Contrôles", True, (255, 255, 255))
            screen.blit(cntrl_ctg, (floor(screen_width // 2) - (cntrl_ctg.get_width() // 2), floor(screen_height // 2) - self.space_between * 0.5))
        

        # Quitter la partie
        if self.esc_menu_ctg == 3:
            opt_ctg = self.ESC_FONT.render("Quitter la partie", True, (240, 0, 0))
            screen.blit(opt_ctg, (floor(screen_width // 2) - (opt_ctg.get_width() // 2), floor(screen_height // 2) + self.space_between * 0.5))
        else:
            opt_ctg = self.ESC_FONT.render("Quitter la partie", True, (255, 255, 255))
            screen.blit(opt_ctg, (floor(screen_width // 2) - (opt_ctg.get_width() // 2), floor(screen_height // 2) + self.space_between * 0.5))
            
        # Quitter le jeux
        if self.esc_menu_ctg == 4:
            opt_ctg = self.ESC_FONT.render("Quitter le jeux", True, (240, 0, 0))
            screen.blit(opt_ctg, (floor(screen_width // 2) - (opt_ctg.get_width() // 2), floor(screen_height // 2) + self.space_between * 1.5))
        else:
            opt_ctg = self.ESC_FONT.render("Quitter le jeux", True, (255, 255, 255))
            screen.blit(opt_ctg, (floor(screen_width // 2) - (opt_ctg.get_width() // 2), floor(screen_height // 2) + self.space_between * 1.5))


    def draw(self, screen: pygame.Surface, fps: int) -> None:
        if self.run_cinematic:
            cin = self.cinematics[self.actual_cinematic]
            if not cin.is_ended(): return cin.draw(screen)

        screen.fill((0, 0, 0))

        self.map.draw(screen, self.assets, self.camera, self.player)
        # self.player.draw(screen, self.assets, self.camera, self.map)
        self.ui.draw(UiDrawArguments(self.player, self.ui_assets, screen))

        self.draw_esc_menu(screen, fps)

        screen.blit(
            self.IN_DEV.render("En développement...", True, (255, 255, 255)),
            (20, screen.get_height() - 35)
        )

    def update(self, frequence: pygame.time.Clock, delta: float) -> None:
        self.player.x = self.camera.x
        self.player.y = self.camera.y

        # Cinematique
        if self.run_cinematic:
            cin = self.cinematics[self.actual_cinematic]
            if not cin.is_ended(): return cin.update(frequence, delta)

        # Si le menu "echap" est ouvert, le joueur ne doit pas se déplacer, alors:
        if not self.is_escaped: self.movements(frequence, delta)

        self.player.update(frequence, delta)
        # self.companion.update(frequence, self.player, self.camera, self.map, delta)
        self.ui.update(frequence, self.player, self.map)

        
        keys = pygame.key.get_pressed()
        if self.key_cooldown <= 0:
            self.key_cooldown = 0.2
            if keys[pygame.K_UP] or keys[pygame.K_z]:
                self.esc_menu_ctg = ((self.esc_menu_ctg - 1 ) % 5)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.esc_menu_ctg = ((self.esc_menu_ctg + 1) % 5)
        elif self.key_cooldown > 0:
            self.key_cooldown -= delta

    def key_down(self, event: pygame.event.Event, engine) -> None:
        if self.run_cinematic:
            cin = self.cinematics[self.actual_cinematic]
            if not cin.is_ended(): return cin.key_down(event)


        if event.key == pygame.K_ESCAPE:
            self.is_escaped = not self.is_escaped
        elif (event.key == pygame.K_e) and (not self.is_escaped):
            self.player.inventory_open = not self.player.inventory_open
        
        elif ((event.key == pygame.K_UP) or (event.key == pygame.K_z)) and self.is_escaped:
            self.key_cooldown = 0.2
            self.esc_menu_ctg = ((self.esc_menu_ctg - 1 ) % 5)
        elif ((event.key == pygame.K_DOWN) or (event.key == pygame.K_s)) and self.is_escaped:
            self.key_cooldown = 0.2
            self.esc_menu_ctg = ((self.esc_menu_ctg + 1) % 5)
        
        elif ((event.key == pygame.K_SPACE) or (event.key == pygame.K_RETURN)) and self.is_escaped:
            if self.esc_menu_ctg == 4:
                # Quitter le jeu
                engine.running = False
            elif self.esc_menu_ctg == 3:
                # Retour au menu
                engine.status = GameStatus.MENU
                self.esc_menu_ctg = False
                self.player.inventory_open = False
            elif self.esc_menu_ctg == 0:
                # retour en jeux
                self.is_escaped = not self.is_escaped

    def manage_collisions(self, vec: Tuple[int, int], movement: Movement) -> Tuple[int, int]:
        for collision in self.map.actual_zone.collisions:
            top_x = collision.x
            top_y = collision.y
            bottom_x = -(-top_x + collision.width)
            bottom_y = -(-top_y + collision.height)

            x = self.player.x + vec[0]
            y = self.player.y + vec[1]
        
            if (top_x >= x) and (top_y >= y) and (bottom_x <= x + CASE_SIZE) and (bottom_y <= y + (CASE_SIZE * 1.5)):
                if movement in [Movement.UP, Movement.UP_LEFT, Movement.UP_RIGHT, Movement.BOTTOM, Movement.BOTTOM_LEFT, Movement.BOTTOM_RIGHT]:
                    vec = (vec[0], 0)
                if movement in [Movement.RIGHT, Movement.UP_RIGHT, Movement.UP_LEFT, Movement.LEFT, Movement.BOTTOM_LEFT, Movement.BOTTOM_RIGHT]:
                    vec = (0, vec[1])

                # Check x & y
                x_check = determine_collision_move(movement, 0)
                if (x_check == movement):
                    return (0,0)
                elif not(x_check is None):
                    vec = (0, vec[1])
                y_check = determine_collision_move(movement, 1)
                if (y_check == movement):
                    return (0,0)
                elif not(y_check is None):
                    vec = (vec[0], 0)

        return vec

    def movements(self, frequence: pygame.time.Clock, delta: float) -> None:
        keys = pygame.key.get_pressed()

        # On vérifie chaque touche (z, q, s, d) pour connaitre le mouvement précis

        vec = (0,0)
        movement = self.player.movement

        if keys[pygame.K_s] and keys[pygame.K_q] and (not keys[pygame.K_d]):
            # move bottom left
            vec = (self.camera.speed // PLAYER_DIAGONAL_COEFF, -(self.camera.speed // PLAYER_DIAGONAL_COEFF))
            movement = Movement.BOTTOM_LEFT
        elif keys[pygame.K_s] and keys[pygame.K_d] and (not keys[pygame.K_q]):
            # move bottom right
            vec = (-(self.camera.speed // PLAYER_DIAGONAL_COEFF), -(self.camera.speed // PLAYER_DIAGONAL_COEFF))
            movement = Movement.BOTTOM_RIGHT
        elif keys[pygame.K_z] and keys[pygame.K_q] and (not keys[pygame.K_d]):
            # move up left
            vec = (self.camera.speed // PLAYER_DIAGONAL_COEFF, self.camera.speed // PLAYER_DIAGONAL_COEFF)
            movement = Movement.UP_LEFT
        elif keys[pygame.K_z] and keys[pygame.K_d] and (not keys[pygame.K_q]):
            # move up right
            vec = (-(self.camera.speed // PLAYER_DIAGONAL_COEFF), self.camera.speed // PLAYER_DIAGONAL_COEFF)
            movement = Movement.UP_RIGHT
        elif keys[pygame.K_z] and ((not (keys[pygame.K_q] or keys[pygame.K_d] or keys[pygame.K_s])) or ((keys[pygame.K_q] and keys[pygame.K_d]) or keys[pygame.K_s])):
            # move only up
            vec = (0, self.camera.speed)
            movement = Movement.UP
        elif keys[pygame.K_q] and not (keys[pygame.K_z] or keys[pygame.K_s] or keys[pygame.K_d]):
            # move only left
            vec = (self.camera.speed, 0)
            movement = Movement.LEFT
        elif keys[pygame.K_d] and not (keys[pygame.K_z] or keys[pygame.K_s] or keys[pygame.K_q]):
            # move only right
            vec = (-self.camera.speed, 0)
            movement = Movement.RIGHT
        elif keys[pygame.K_s] and ((not (keys[pygame.K_q] or keys[pygame.K_d] or keys[pygame.K_s])) or ((keys[pygame.K_q] and keys[pygame.K_d]) or keys[pygame.K_s])):
            # move only bottom
            vec = (0, -self.camera.speed)
            movement = Movement.BOTTOM

        # Il n'y a aucun changement de coordonnées
        if (self.player.movement == movement) and (vec == (0,0)): return

        # Normaliser vecteurs
        total_speed = sqrt(vec[0] ** 2 + vec[1] ** 2)
        if total_speed > SPEED_NORMALIZE_SEUIL:
            normalization_coeff = SPEED_NORMALIZE_SEUIL / total_speed
            vec = (vec[0] * normalization_coeff, vec[1] * normalization_coeff)

        # Move player based on his movement
        decompose_x = determine_collision_move(movement, 0)
        if not(decompose_x is None):
            self.player.move(movement, self.manage_collisions((vec[0] * delta, 0), movement), self.camera, delta)

        decompose_y = determine_collision_move(movement, 1)
        if not(decompose_y is None):
            self.player.move(movement, self.manage_collisions((0, vec[1] * delta), movement), self.camera, delta)
