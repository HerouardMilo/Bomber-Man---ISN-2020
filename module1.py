

"""
Jeu BomberMan
Jeu dans lequel on doit casser des briques pour atteindre l'arrivée

"""

import pygame
from pygame.locals import *

from classes import *
from constantes import *


pygame.init()



#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((cote_fenetre, cote_fenetre))
#Mise en place de l'icone
icone = pygame.image.load(image_icone)
pygame.display.set_icon(icone)
#Mise en place du titre
pygame.display.set_caption(titre_fenetre)



#BOUCLE PRINCIPALE
continuer = 1
while continuer:
    accueil = pygame.image.load(image_accueil).convert()
    fenetre.blit(accueil, (0,0))

    #Rafraichissement
    pygame.display.flip()



    #On remet ces variables à 1 à chaque tour de boucle
    continuer_jeu = 1
    continuer_accueil = 1

	#BOUCLE D'ACCUEIL
    while continuer_accueil:

		#Limitation de vitesse de la boucle
        pygame.time.Clock().tick(30)

        for event in pygame.event.get():

			#Si l'utilisateur quitte, on met les variables
			#de boucle à 0 pour n'en parcourir aucune et fermer la fenêtre
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                continuer_accueil = 0
                continuer_jeu = 0
                continuer = 0
				#Variable de choix du niveau (car on envisage d'en faire plusieur on a donc mis un selecteur)
                choix = 0

            elif event.type == KEYDOWN:
				#Lancement du niveau 1
                if event.key == K_F1:
                    continuer_accueil = 0	#On quitte l'accueil
                    choix = 'carte'
                if event.key == K_F2:
                    continuer_accueil = 0
                    choix = 'commande' #On est censé avoir accès au commande en faisant F2 mais un bug nous empeche de rajouter une ligne de code




	#On vérifie que le joueur a bien fait le choix du niveau
	#pour ne pas charger s'il quitte la fenêtre (cela empêche les bugs)
    if choix != 0:

		#Chargement du fond
        fond = pygame.image.load(image_fond).convert()


		#Génération du niveau à partir du fichier portant le nom du niveau (ici "carte")
        niveau = Niveau(choix)
        niveau.generer()
        niveau.afficher(fenetre)

		#Création du BomberMan (le personnage) et de la bombe
        #bombe = Bombe("images/Bombe.png", niveau) on a ici un bug qu'on ne comprend pas vraiment(j'ai mis un # pour empecher le programme de bug)
        bm = Perso("images/bm_droite.png", "images/bm_gauche.png",
		"images/bm_haut.png", "images/bm_bas.png", niveau)




	#BOUCLE DE JEU
    while continuer_jeu:

		#Limitation de vitesse de la boucle
        pygame.time.Clock().tick(30)

        for event in pygame.event.get():

			#Si l'utilisateur quitte, on met la variable qui continue le jeu
			#et la variable générale à 0 pour fermer la fenêtre
            if event.type == QUIT:
                continuer_jeu = 0
                continuer = 0

            elif event.type == KEYDOWN:
				#Si l'utilisateur presse Echap ici, on revient seulement au menu
                if event.key == K_ESCAPE:
               	    continuer_jeu = 0

				#Touches de déplacement du BomberMan
                elif event.key == K_RIGHT:
                    bm.deplacer('droite')
                elif event.key == K_LEFT:
                    bm.deplacer('gauche')
                elif event.key == K_UP:
                    bm.deplacer('haut')
                elif event.key == K_DOWN:
                    bm.deplacer('bas')
                #touche pour poser la bombe
                elif event.key == K_b :
                    bombe.poser(bm.x,bm.y, image_bombe)


		#Affichages aux nouvelles positions
        fenetre.blit(fond, (0,0))
        niveau.afficher(fenetre)
        fenetre.blit(bm.direction, (bm.x, bm.y)) #bm.direction = l'image dans la bonne direction (on oriente correctement le personnage)
        pygame.display.flip()

		#Victoire -> Retour à l'accueil (on revient sur la potentiel futur selection de niveau)
        if niveau.structure[bm.case_y][bm.case_x] == 'a':
            continuer_jeu = 0

