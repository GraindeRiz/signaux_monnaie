"""Réduction du bruit par un filtre médian."""

from skimage.filters import median
from skimage.morphology import disk


def appliquer_filtre_median(image):
    """Reçoit une image et renvoie une version filtrée.

    Le rayon règle la taille du voisinage utilisé autour de chaque pixel.
    """
    return median(image)
