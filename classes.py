#voici toute les classes dont on a eu besoin pour faire le BomberMan

import pygame
from pygame.locals import *
from constantes import *

class Niveau:
 #classe permettant de crée un niveau
	def __init__(self, fichier):
		self.fichier = fichier
		self.structure = 0


	def generer(self):

		#On ouvre le fichier
		with open(self.fichier, "r") as fichier:
			structure_niveau = []
			#On parcourt les lignes du fichier
			for ligne in fichier:
				ligne_niveau = []
				#On parcourt les sprites (lettres) contenus dans le fichier
				for sprite in ligne:
					#On ignore les "\n" de fin de ligne
					if sprite != '\n':
						#On ajoute le sprite à la liste de la ligne
						ligne_niveau.append(sprite)
				#On ajoute la ligne à la liste du niveau
				structure_niveau.append(ligne_niveau)
			#On sauvegarde cette structure
			self.structure = structure_niveau


	def afficher(self, fenetre):
		#Chargement des images
		mur = pygame.image.load(image_mur).convert()
		arrivée = pygame.image.load(image_arrivée).convert()
		brique = pygame.image.load(image_brique).convert_alpha()

		#On parcourt la liste du niveau
		num_ligne = 0
		for ligne in self.structure:
			num_case = 0
			for sprite in ligne:
				#On calcule la position réelle en pixels
				x = num_case * taille_sprite
				y = num_ligne * taille_sprite
				if sprite == 'm':		   #m = mur incassable
					fenetre.blit(mur, (x,y))
				elif sprite == 'a':		   #a = arrivée
					fenetre.blit(arrivée, (x,y))
				elif sprite == 'b':		   #b = brique
					fenetre.blit(brique, (x,y))

				num_case += 1
			num_ligne += 1




class Perso:
	#Classe permettant de crée un personnage
	def __init__(self, droite, gauche, haut, bas, niveau):
		#Sprites du personnage
		self.droite = pygame.image.load(droite).convert_alpha()
		self.gauche = pygame.image.load(gauche).convert_alpha()
		self.haut = pygame.image.load(haut).convert_alpha()
		self.bas = pygame.image.load(bas).convert_alpha()
		#Position du personnage en cases et en pixels
		self.case_x = 1
		self.case_y = 1
		self.x = 32
		self.y = 32
		#Direction par défaut
		self.direction = self.bas
		#Niveau dans lequel le personnage se trouve
		self.niveau = niveau


	def deplacer(self, direction):
		#Méthode permettant de déplacer le personnage et de gérer les collisions

		#Déplacement vers la droite
		if direction == 'droite':
			#Pour ne pas dépasser l'écran
			if self.case_x < (nombre_sprite_cote - 1):
				#On vérifie que la case de destination n'est pas un mur
				if self.niveau.structure[self.case_y][self.case_x+1] != 'm' and self.niveau.structure[self.case_y][self.case_x+1] != 'b':
					#Déplacement d'une case
					self.case_x += 1
					#Calcul de la position "réelle" en pixel
					self.x = self.case_x * taille_sprite
			#Image dans la bonne direction
			self.direction = self.droite

		#Déplacement vers la gauche
		if direction == 'gauche':
			if self.case_x > 0:
				if self.niveau.structure[self.case_y][self.case_x-1] != 'm' and self.niveau.structure[self.case_y][self.case_x-1] != 'b' :
					self.case_x -= 1
					self.x = self.case_x * taille_sprite
			self.direction = self.gauche

		#Déplacement vers le haut
		if direction == 'haut':
			if self.case_y > 0:
				if self.niveau.structure[self.case_y-1][self.case_x] != 'm'and self.niveau.structure[self.case_y-1][self.case_x] != 'b':
					self.case_y -= 1
					self.y = self.case_y * taille_sprite
			self.direction = self.haut

		#Déplacement vers le bas
		if direction == 'bas':
			if self.case_y < (nombre_sprite_cote - 1):
				if self.niveau.structure[self.case_y+1][self.case_x] != 'm'and self.niveau.structure[self.case_y+1][self.case_x] != 'b':
					self.case_y += 1
					self.y = self.case_y * taille_sprite
			self.direction = self.bas

class Bombe: #Classe permettant de creer une bombe (On a un problème concernant la pose de bombe)

    def __init__(self,pose,bombe, niveau):
        self.bombe = pygame.image.load(Bombe).convert()

        self.niveau = niveau
        self.x = 32
        self.y = 32
        self.case_x = 1
        self.case_y = 1




    def poser(self, x, y, bombe, niveau):

        self.bombe = pygame.image.load(bombe).convert()
        self.x = x
        self.y = y
        self.case_x = (x / taille_sprite)
        self.case_y = (y / taille_sprite)


