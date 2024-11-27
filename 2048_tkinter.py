import tkinter as tk
from random import randint
import keyboard
import time

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
    x = len(grille)+1
    y = len(grille)+1
    tab = [2,4]
    nbr = tab[randint(0,1)]
    while not est_libre(x,y,grille):
        x = randint(0,len(grille)-1)
        y = randint(0,len(grille)-1)
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




CELL_SIZE = 100  # Taille de chaque cellule
COULEURS = {
    0: "#cdc1b4",  # Fond vide
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
}

def ouvrir_fenetre():
    """
    Lancer le jeu en mode graphique (Tkinter)
    """
    taille = int(entry.get())  # Taille de la grille carrée (par exemple 4x4)
    grille = creer_grille(taille)  # Crée une nouvelle grille
    tuiles(grille)
    tuiles(grille)

    # Création de la fenêtre de jeu
    fenetre_grille = tk.Toplevel(fenetre_principal)
    fenetre_grille.title("Jeu du 2048")

    # Canvas pour afficher la grille
    canvas = tk.Canvas(
        fenetre_grille, width=taille * CELL_SIZE, height=taille * CELL_SIZE, bg="white"
    )
    canvas.pack()

    def afficher_grille_tk():
        """Affiche la grille dans l'interface Tkinter"""
        for i in range(taille):
            for j in range(taille):
                valeur = grille[i][j]
                x1, y1 = j * CELL_SIZE, i * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                couleur = COULEURS[valeur]
                canvas.create_rectangle(x1, y1, x2, y2, fill=couleur, outline="black")
                if valeur != 0:
                    canvas.create_text(
                        (x1 + x2) // 2, (y1 + y2) // 2,
                        text=str(valeur),
                        font=("Helvetica", 24, "bold"),
                        fill="black"
                    )

    # Afficher la grille initiale
    afficher_grille_tk()

    # Gérer les déplacements via les touches du clavier
    def deplacement(event):
        """Met à jour la grille en fonction de la touche pressée"""
        nonlocal grille
        if event.keysym == "q":
            for ligne in range(taille):
                grille[ligne] = deplacer_gauche(grille[ligne])
        elif event.keysym == "d":
            for ligne in range(taille):
                grille[ligne] = deplacer_droite(grille[ligne])
        elif event.keysym == "z":
            for i in range(taille):
                grille = deplacer_haut(grille, i)
        elif event.keysym == "s":
            for i in range(taille):
                grille = deplacer_bas(grille, i)
        tuiles(grille)
        afficher_grille_tk()

        # Vérifier si le jeu est terminé
        if not mouvement_possible(grille):
            canvas.create_text(
                taille * CELL_SIZE // 2, taille * CELL_SIZE // 2,
                text="Game Over",
                font=("Helvetica", 32, "bold"),
                fill="red"
            )

    # Lier les touches du clavier au déplacement
    fenetre_grille.bind("<Key>", deplacement)
    fenetre_grille.mainloop()


# Fenêtre principale
fenetre_principal = tk.Tk()
fenetre_principal.title("Jeu du 2048")
fenetre_principal.geometry("400x300")

label = tk.Label(fenetre_principal, text="Veuillez entrez la taille de la grille :")
label.pack()

entry = tk.Entry(fenetre_principal)
entry.pack()

bouton = tk.Button(fenetre_principal, text="Jouer", command=ouvrir_fenetre)
bouton.pack()

fenetre_principal.mainloop()
