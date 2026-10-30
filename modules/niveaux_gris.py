"""Conversion d'une image couleur en niveaux de gris."""

from skimage.color import rgb2gray


def convertir_en_gris(image):
    """Reçoit une image couleur et renvoie une image en niveaux de gris."""
    return rgb2gray(image)
