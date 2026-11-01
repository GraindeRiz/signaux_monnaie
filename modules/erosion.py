"""Érosion morphologique d'une image binaire."""

from skimage.morphology import diamond, erosion as skimage_erosion


def appliquer_erosion(image, rayon=1):
    """Réduit les régions blanches avec un losange de rayon donné."""
    return skimage_erosion(image, footprint=diamond(rayon))
