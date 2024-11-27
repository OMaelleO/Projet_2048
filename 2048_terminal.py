from random import randint
import keyboard
import time
import tkinter as tk

###Grille

def creer_grille(n):
    """
    Créer un grille carré de taille n
    Entrée : un entier
    Sortie : Une liste de n liste de n element
    """
    grille = []
    for i in range(n):
        tab = []
        for j in range(n):
            tab.append(0)
        grille.append(tab)
    return grille

def afficher_grille(grille): #A faire
    """
    Affiche la grille d'une certaine façon
    Entrée : la grille
    Sortie : l'affichage de la grille
    """ 
    for i in range(len(grille)):
        print('---------------------')
        for j in range(len(grille)):
            if grille[i][j] == 0:
                print('|'+ ' ' * 4, end='')
            else :
                print('|'+ ' ' * (4- len(str(grille[i][j]))) + str(grille[i][j]), end='')
        print('|')
    print('---------------------')

grille = creer_grille(4)
print(afficher_grille(grille))

###Verification

def est_libre(x,y,grille):
    """
    Vérifie si la case est dans la grille et si elle est libre
    Entrée : les coordoné de la case à verifier, la grille
    Sortie : True sur libre, False sinon
    """
    if x <= len(grille) and y <= len(grille) and grille[y][x] == 0:
        return True
    return False

def est_plein(grille):
    """
    Place une tuile de 2 ou 4 aléatoirement dans la grille
    Entrée : La grille
    Sortie : None mais la grille est modifier avec la tuiles
    """ #Vérifie si la grille est pleine
    for y in range(len(grille)):
        for x in range(len(grille)):
            if est_libre(x,y,grille):
                return False
    return True

def mouvement_possible(grille):
    """
    Vérifie si un y a des cases libre ou des fusions possible
    Entrée : la grille
    Sortie : True si un mouvement est possible, False sinon
    """
    taille = len(grille)
    if not est_plein(grille): # Vérifie s'il y a des cases libres
        return True
    for y in range(taille): # Vérifie la possibilité de fusion en comparant avec les cases adjacentes
        for x in range(taille):
            if x < taille - 1 and grille[y][x] == grille[y][x + 1]:
                return True
            if y < taille - 1 and grille[y][x] == grille[y + 1][x]:
                return True
    return False


###Ajout tuiles auto

def tuiles(grille): 
    """
    Place une tuile de 2 ou 4 aléatoirement dans la grille
    Entrée : La grille
    Sortie : None mais la grille est modifier avec la tuiles
    """
    tab = [2, 4]
    nbr = tab[randint(0, 1)]
    
    cases_vides = []
    for y in range(len(grille)):
        for x in range(len(grille)):
            if grille[y][x] == 0:
                cases_vides.append((x, y))

    if cases_vides:
        x, y = cases_vides[randint(0, len(cases_vides) - 1)]
        grille[y][x] = nbr

###Déplacement

def deplacer_droite(ligne):
    """
    Deplace la ligne vers la Droite
    Entrée : La ligne
    Sortie : la ligne modifié
    """
    ligne2 = [x for x in ligne if x != 0] #Liste sans les None
    i = len(ligne2) - 1
    while i > 0:
        if ligne2[i] == ligne2[i - 1]: #Si deux même nombre sont à coté, on les fusionnes et i-1 devient None 
            ligne2[i] *= 2 
            ligne2[i - 1] = 0 
            i -= 2
        else:
            i -= 1
    ligne2 = [x for x in ligne2 if x != 0] #On enleve les None qui sont arrivé
    ligne = [0] * (len(ligne) - len(ligne2)) + ligne2 # On met les chiffres à droite et on complete à gauche les case restantes avec des None
    return ligne

def deplacer_gauche(ligne):
    """
    Deplace la ligne vers la Gauche
    Entrée : La ligne
    Sortie : la ligne modifié
    """
    ligne = ligne[::-1] 
    ligne = deplacer_droite(ligne)
    return ligne[::-1]

def deplacer_haut(grille,col_index):
    """
    Deplace la colonne vers le Haut
    Entrée : La grille, l'index de la colonne ou numero de colonne
    Sortie : la colonne modifié reintegré dans la grille
    """
    colonne = [grille[i][col_index] for i in range(len(grille))] #on extrait les elements en colonne pour les avoirs dans une liste
    colonne = deplacer_droite(colonne[::-1])
    for i in range(len(grille)): #On réintegre la liste dans la grille sous forme de colomne
        grille[i][col_index] = colonne[::-1][i]
    return grille

def deplacer_bas(grille, col_index):
    """
    Deplace la colonne vers le Bas
    Entrée : La grille, l'index de la colonne ou numero de colonne
    Sortie : la colonne modifié reintegré dans la grille
    """
    colonne = [grille[i][col_index] for i in range(len(grille))]
    colonne = deplacer_droite(colonne)
    for i in range(len(grille)):
        grille[i][col_index] = colonne[i]
    return grille


def jouer(meilleur_score = 0):
    """
    Jouer au 2048
    """
    taille = int(input("Quelle taille de grille ?:"))
    grille = creer_grille(taille)
    tuiles(grille)
    tuiles(grille)
    afficher_grille(grille)
    while mouvement_possible(grille):
        event = keyboard.read_event()
        if event.name == "d":
            for ligne in range(taille):
                grille[ligne] = deplacer_droite(grille[ligne])
        elif event.name == "q":
            for ligne in range(taille):
                grille[ligne] = deplacer_gauche(grille[ligne])
        elif event.name == "z":
            for i in range(taille):
                grille = deplacer_haut(grille,i)
        elif event.name == "s":
            for i in range(taille):
                grille = deplacer_bas(grille,i)
        elif event.name == "esc":
                print("Sortie...")
                break
        tuiles(grille)
        afficher_grille(grille)
        time.sleep(0.2)
    print('game over')
    score = 0
    for y in grille:
        for x in y:
            if x > score:
                score = x
    print("Votre score est :", score)
    if score > meilleur_score:
        meilleur_score = score
        print("Record battu !")
    print("Meilleur score :", meilleur_score)
    rejouer = input("Voulez vous rejouer ? [y / n] :")
    if rejouer == "y":
        return jouer(meilleur_score = meilleur_score)
    else :
        print("Au revoir")

    



print(jouer())

