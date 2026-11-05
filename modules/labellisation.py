"""Labellisation des régions connectées d'un masque binaire."""

import numpy as np
from skimage.measure import label
from skimage import measure
from skimage.color import rgb2hsv


def labelliser_objets(image, connectivite=1):
    return label(image, connectivity=connectivite)


def compter_objets(image_labellisee):
    return int(np.max(image_labellisee))

def mesurer_objets(image_labellisee,image_originale):
    data = measure.regionprops(image_labellisee)
    image_HSV = rgb2hsv(image_originale)
    tab=[]
    for i in data:
        lignes = i.coords[:,0]
        colonnes = i.coords[:,1]
        teinte_piece = image_HSV[lignes,colonnes,0]
        teinte_piece = np.median(teinte_piece)
        teinte_degres = teinte_piece *360
        if teinte_degres < 25:
            couleur = "Cuivre"
        elif 30 <= teinte_degres < 45:
            couleur = "Dorée"
        else:
            couleur = "Bicolor"
        tab.append({
           
            
            "piece": i.label,
            "aire (en px)": round(i.area,2),
            "périmètre(en px)": round(i.perimeter,2),
            "Couleur": couleur,
            })
    return tab

def liste_aires(tab):
    for i in tab:
        for cle, valeur in i.items():
            print(valeur)