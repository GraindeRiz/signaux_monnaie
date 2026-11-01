"""Labellisation des régions connectées d'un masque binaire."""

import numpy as np
from skimage.measure import label


def labelliser_objets(image, connectivite=1):
    return label(image, connectivity=connectivite)


def compter_objets(image_labellisee):
    return int(np.max(image_labellisee))
