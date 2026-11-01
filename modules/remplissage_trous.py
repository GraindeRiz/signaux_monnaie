"""Remplissage des trous fermés dans un masque binaire."""

from scipy.ndimage import binary_fill_holes


def remplir_trous(image):
    return binary_fill_holes(image)
