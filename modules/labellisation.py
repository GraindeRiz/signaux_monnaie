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
    """Mesure les objets et estime leur couleur par teinte et saturation."""
    data = measure.regionprops(image_labellisee)
    image_HSV = rgb2hsv(image_originale)
    tab=[]
    for i in data:
        lignes = i.coords[:,0]
        colonnes = i.coords[:,1]
        pixels_hsv = image_HSV[lignes, colonnes]
        teinte_degres = np.median(pixels_hsv[:, 0]) * 360

        # Comparer le centre et un anneau à l'intérieur du masque.
        cy, cx = i.centroid
        distances = np.hypot(lignes - cy, colonnes - cx)
        rayon = np.sqrt(i.area / np.pi)
        centre = distances < 0.55 * rayon
        bord = (distances > 0.75 * rayon) & (distances < 0.90 * rayon)

        ecart_saturation = 0.0
        if np.any(centre) and np.any(bord):
            saturation_centre = np.median(pixels_hsv[centre, 1])
            saturation_bord = np.median(pixels_hsv[bord, 1])
            ecart_saturation = abs(saturation_centre - saturation_bord)

        if teinte_degres < 30:
            couleur = "Cuivre"
        elif ecart_saturation > 0.12:
            couleur = "Bicolor"
        else:
            couleur = "Dorée"
        tab.append({
           
            
            "piece": i.label,
            "aire (en px)": round(i.area,2),
            "périmètre(en px)": round(i.perimeter,2),
            "Couleur": couleur,
            })
    return tab
