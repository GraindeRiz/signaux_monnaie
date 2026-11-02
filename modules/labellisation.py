"""Labellisation des régions connectées d'un masque binaire."""

import numpy as np
from skimage.measure import label
from skimage import measure


def labelliser_objets(image, connectivite=1):
    return label(image, connectivity=connectivite)


def compter_objets(image_labellisee):
    return int(np.max(image_labellisee))

def mesurer_objets(image_labellisee,image_originale):
    data = measure.regionprops(image_labellisee, intensity_image=image_originale)
    tab=[]
    for i in data:
        r,g,b = i.intensity_mean
        tab.append({
            "piece": i.label,
            "aire (en px)": round(i.area,2),
            "périmètre(en px)": round(i.perimeter,2),
            "diamètre(en px)": round(i.equivalent_diameter,2),
            "Couleur": "#{:02x}{:02x}{:02x}".format(int(r), int(g), int(b)),
            })
    return tab