from enum import Enum
from typing import List

import pygame

from modules.fonts import fonts

"""
Ce fichier contient le système de succès
"""


class AchievementsID(Enum):
    WALK_10000_STEPS = 0  # Marcher 10 000 pas
    FIRST_PARTY = 1  # Lancer une partie pour la première fois
    GET_THE_OLD_ADVENTURE = 2  # Charger une sauvegarde
    WATCH_CREDITS = 3  # Regarder les crédits
    THIRD_TIME_RIGHT = 4  # Lancer le jeu 3 fois


class Achievement:
    """
    Cette class représente un succès
    """

    def __init__(self, success_name: str, success_id: AchievementsID, description: str,
                 completed: bool = False) -> None:
        self.name = success_name
        self.id = success_id
        self.description = description

        self.completed = completed

    def complete(self):
        self.completed = True

    def uncompleted(self):
        self.completed = False


class AchievementsBank:
    """
    Cette class contient le système de gestion des succès
    """

    def __init__(self) -> None:
        # On stocke un dictionnaire qui contiendra en clé des AchievementsID et en valeur Achievement
        self.success = {}

        # Cette liste fera office de file
        # On va dessiner chaque succès à la suite
        self.success_showed = []

        # On stocke le nombre de secondes écoulées
        self.ticks = 0

        # Le temps maximal d'affichage d'un succès, exprimé en secondes
        self.MAX_TICKS_ANIMATION = 7.0  # 7s

        # Le temps pour les animations d'entrées et sortie
        self.ANIMATION_DURATION = 1.0

    def to_json(self) -> List:
        return [{"completed": s.completed, "id": s.id.value} for s in self.success.values()]

    def register_success(self, success_id: AchievementsID, new_success: Achievement, force: bool = False):
        """
        Enregistre un succès dans la base de donnée grâce à son identifiant
        N'effectue l'action que si le succès n'est pas enregistré ou que `force` est vrai
        """
        if not (success_id in self.success) or force:
            self.success[success_id] = new_success

    def complete(self, success_id: AchievementsID):
        """
        Complète un succès 
        """
        if success_id in self.success:
            self.success[success_id].complete()

            # On affiche le succès
            self.success_showed.append(success_id)

            if len(self.success_showed) <= 1:
                # Comme on sais que il y a AU MOINS un succès affiché, on regarde si il n'y en avait qu'un
                # si oui, on met les ticks à 0
                self.ticks = 0

    def uncompleted(self, success_id: AchievementsID):
        """
        Déclare un succès comme "à faire"
        """
        if success_id in self.success:
            self.success[success_id].uncompleted()

    def is_complete(self, success_id: AchievementsID) -> bool:
        """
        Renvoi une boolean qui permet de savoir si un succès est complété
        """
        return (success_id in self.success) and self.success[success_id].completed

    def format(self, per_page: int = 5) -> List[List[Achievement]]:
        """
        Renvoie une list en 2D pour l'affichage des succès
        Comme c'est un système de pages, nous allons mettre au maximum 5 succès par pages (personnalisable)
        """
        # Contiendra toutes les pages
        pages: List[List[Achievement]] = []
        # Contient les succès qui sont sur le point d'être placées dans `pages`
        temp = []
        # On parcourt chaque succès
        for s in self.success.values():
            # On ajoute le succès à `temp`
            temp.append(s)
            # Si `temp` a atteint ou dépassé la longueur par page demandée,
            # alors on ajoute `temp` aux pages et on nettoie `temp`
            if len(temp) >= per_page:
                pages.append(temp)
                temp = []
        # On vérifie une dernière fois pour éviter toute oublie
        if len(temp) > 0:
            pages.append(temp)
        return pages

    def draw_success(self, screen: pygame.Surface):
        """
        Cette fonction permet de dessine les messages d'obtention des succès
        """
        if len(self.success_showed) <= 0:
            return

        # On récupère le succès à afficher
        actual_success_id = self.success_showed[0]

        # On génère les textes
        title = fonts.get(25).render("Nouveau succès débloqué", True, (255, 255, 255))
        success_name = fonts.get(25).render(ACHIEVEMENTS_INFO[actual_success_id][0], True, (255, 255, 255))

        # On regarde quel texte est le plus long, pour ne pas avoir de texte qui dépasse
        width = title.get_width()
        if success_name.get_width() > width:
            width = success_name.get_width()

        # On calcule la taille réelle de la box (20px de bordure de chaque coté)
        box_width = width + 140

        # On calcule la hauteur des deux textes
        height = title.get_height() + success_name.get_height() + 25  # 25px d'écart

        # On calcule le décalage sur `x`
        x, y = screen.get_width() - width - 100, 40

        # Système d'animation
        if self.ticks <= self.ANIMATION_DURATION:
            # Entrée
            before = box_width
            box_width /= (self.ANIMATION_DURATION - self.ticks)
            # On doit inverser!
            x += before * (self.ANIMATION_DURATION - self.ticks)
        elif self.ticks >= self.MAX_TICKS_ANIMATION - self.ANIMATION_DURATION:
            # Sortie
            x += box_width - (box_width * (self.MAX_TICKS_ANIMATION - self.ticks))

        # On dessine le fond
        # avec un écart de 20px sur chaque coté
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                x - 20,
                y - 20,
                box_width,
                height + 40
            ),
            border_top_left_radius=25,
            border_bottom_left_radius=25
        )

        # On dessine les textes
        screen.blit(title, (x, y))
        screen.blit(success_name, (x, y + 15 + title.get_height()))

    def update(self, delta: float):
        """
        Cette fonction met à jour le système de succès
        """
        if self.ticks > self.MAX_TICKS_ANIMATION:
            # L'animation est finie
            # On retire le premier de la file
            if len(self.success_showed) > 0:
                self.success_showed.pop(0)
            self.ticks = 0
        elif len(self.success_showed) > 0:
            self.ticks += delta


# On déclare la banque de succès afin de pouvoir y accéder depuis n'importe où
achievements: AchievementsBank = AchievementsBank()

ACHIEVEMENTS_INFO = {
    AchievementsID.FIRST_PARTY: ("Première partie", "Lancer une partie pour la première fois"),
    AchievementsID.GET_THE_OLD_ADVENTURE: ("Retour en territoire connu", "Charger une ancienne sauvegarde"),
    AchievementsID.WALK_10000_STEPS: ("Une petite promenade", "Marcher 10.000 pas"),
    AchievementsID.WATCH_CREDITS: ("Regarder les crédits", "La patience il faudra."),
    AchievementsID.THIRD_TIME_RIGHT: ("Lancer le jeu 3 fois", "Le succès est une affaire de loyauté")
}

# On enregistre chaque évènement
for achievement, id in AchievementsID.__members__.items():
    # On récupère le nom et la description
    name, desc = ACHIEVEMENTS_INFO[id]
    success = Achievement(name, id, desc, completed=False)
    achievements.register_success(id, success, force=False)
