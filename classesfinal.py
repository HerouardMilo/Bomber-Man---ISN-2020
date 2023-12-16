# voici toute les classes dont on a eu besoin pour faire le bomberMan

import pygame
import time
from pygame.locals import *
from constantes import *
from datetime import datetime, timedelta


class Niveau:
    # classe permettant de crée un niveau
    def __init__(self, fichier):
        self.fichier = fichier
        self.structure = 0

    def generer(self):

        # On ouvre le fichier
        with open(self.fichier, "r") as fichier:
            structure_niveau = []
            # On parcourt les lignes du fichier
            for ligne in fichier:
                ligne_niveau = []
                # On parcourt les sprites (lettres) contenus dans le fichier
                for sprite in ligne:
                    # On ignore les "\n" de fin de ligne
                    if sprite != '\n':
                        # On ajoute le sprite à la liste de la ligne
                        ligne_niveau.append(sprite)
                # On ajoute la ligne à la liste du niveau
                structure_niveau.append(ligne_niveau)
            # On sauvegarde cette structure
            self.structure = structure_niveau

    def afficher(self, fenetre):

        # Chargement des images
        mur = pygame.image.load(image_mur).convert()
        brique = pygame.image.load(image_brique).convert()
        arrivee = pygame.image.load(image_arrivee).convert_alpha()
        commande = pygame.image.load(image_commande).convert()
        bombe = pygame.image.load(image_bombe).convert()

        # On parcourt la liste du niveau
        num_ligne = 0
        for ligne in self.structure:

            num_case = 0
            for sprite in ligne:
                # On calcule la position réelle en pixels
                x = num_case * taille_sprite
                y = num_ligne * taille_sprite
                if sprite == 'm':  # m = Mur incassable
                    fenetre.blit(mur, (x, y))
                elif sprite == 'b':  # b = brique
                    fenetre.blit(brique, (x, y))
                elif sprite == 'o':  # o = bombes
                    fenetre.blit(bombe, (x, y))
                elif sprite == 'c':  # c = menu des commandes
                    fenetre.blit(commande, (x, y))
                elif sprite == 'a':  # a = Arrivée
                    fenetre.blit(arrivee, (x, y))
                num_case += 1
            num_ligne += 1

    def pose_et_destruit(self, bombe, bm):
        # Fonction permettant de détruire une brique
        if self.structure[bombe.case_y + 1][bombe.case_x] == "b":
            self.structure[bombe.case_y + 1][bombe.case_x] = "d"
        if self.structure[bombe.case_y - 1][bombe.case_x] == "b":
            self.structure[bombe.case_y - 1][bombe.case_x] = "d"
        if self.structure[bombe.case_y][bombe.case_x - 1] == "b":
            self.structure[bombe.case_y][bombe.case_x - 1] = "d"
        if self.structure[bombe.case_y][bombe.case_x + 1] == "b":
            self.structure[bombe.case_y][bombe.case_x + 1] = "d"

class Bm:
    # Classe permettant de crée un personnage
    def __init__(self, droite, gauche, haut, bas, niveau):
        # Sprites du personnage
        self.droite = pygame.image.load(droite).convert_alpha()
        self.gauche = pygame.image.load(gauche).convert_alpha()
        self.haut = pygame.image.load(haut).convert_alpha()
        self.bas = pygame.image.load(bas).convert_alpha()
        # Position du personnage en cases et en pixels
        self.case_x = 1
        self.case_y = 1
        self.x = 32
        self.y = 32
        # Direction par défaut
        self.direction = self.bas
        self.orientation = "bas"
        # Niveau dans lequel le personnage se trouve
        self.niveau = niveau

    def deplacer(self, direction):
        # Méthode permettant de déplacer le personnage et de gérer les collisions

        # Déplacement vers la droite
        if direction == 'droite':
            # Pour ne pas dépasser l'écran
            if self.case_x < (nombre_sprite_cote - 1):
                # On vérifie que la case de destination n'est pas un mur
                if self.niveau.structure[self.case_y][self.case_x + 1] != 'm' and self.niveau.structure[self.case_y][
                    self.case_x + 1] != 'b':
                    # Déplacement d'une case
                    self.case_x += 1
                    # Calcul de la position "réelle" en pixel
                    self.x = self.case_x * taille_sprite
            # Image dans la bonne direction
            self.direction = self.droite
            self.orientation = "droite"

        # Déplacement vers la gauche
        if direction == 'gauche':
            if self.case_x > 0:
                if self.niveau.structure[self.case_y][self.case_x - 1] != 'm' and self.niveau.structure[self.case_y][
                    self.case_x - 1] != 'b':
                    self.case_x -= 1
                    self.x = self.case_x * taille_sprite
            self.direction = self.gauche
            self.orientation = "gauche"

        # Déplacement vers le haut
        if direction == 'haut':
            if self.case_y > 0:
                if self.niveau.structure[self.case_y - 1][self.case_x] != 'm' and \
                        self.niveau.structure[self.case_y - 1][self.case_x] != 'b':
                    self.case_y -= 1
                    self.y = self.case_y * taille_sprite
            self.direction = self.haut
            self.orientation = "haut"

        # Déplacement vers le bas
        if direction == 'bas':
            if self.case_y < (nombre_sprite_cote - 1):
                if self.niveau.structure[self.case_y + 1][self.case_x] != 'm' and \
                        self.niveau.structure[self.case_y + 1][self.case_x] != 'b':
                    self.case_y += 1
                    self.y = self.case_y * taille_sprite
            self.direction = self.bas
            self.orientation = "bas"


class Bombe:
    # Classe permettant de crée un personnage
    def __init__(self, bombe, niveau, bm):
        # Sprites du personnage
        self.bombe = pygame.image.load(bombe).convert_alpha()
        # Position du personnage en cases et en pixels
        self.case_x = 1
        self.case_y = 2
        self.x = 32
        self.y = 64
        self.début_temps = datetime.now()

        # Niveau dans lequel le personnage se trouve
        self.niveau = niveau
        self.bm = bm
        self.explosion = 0

    def pose(self, bm, bombe,niveau):

        self.bombe = pygame.image.load(bombe).convert()

        if bm.orientation == "bas" :
            if niveau.structure[bm.case_y + 1][bm.case_x] != "b" and niveau.structure[bm.case_y + 1][bm.case_x] != "m" :
                self.case_x = bm.case_x
                self.case_y = bm.case_y + 1
        if bm.orientation == "haut" :
            if niveau.structure[bm.case_y - 1][bm.case_x] != "b" and niveau.structure[bm.case_y - 1][bm.case_x] != "m" :
                self.case_x = bm.case_x
                self.case_y = bm.case_y - 1
        if bm.orientation == "droite" :
            if niveau.structure[bm.case_y][bm.case_x + 1] != "b" and niveau.structure[bm.case_y][bm.case_x + 1] != "m" :
                self.case_x = bm.case_x + 1
                self.case_y = bm.case_y
        if bm.orientation == "gauche" :
            if niveau.structure[bm.case_y][bm.case_x - 1] != "b" and niveau.structure[bm.case_y][bm.case_x - 1] != "m" :
                self.case_x = bm.case_x - 1
                self.case_y = bm.case_y

        niveau.structure[self.case_y][self.case_x] = "o"
        print(self.case_x, self.case_y)


