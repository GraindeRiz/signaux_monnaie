"""Dilatation morphologique d'une image binaire."""

from skimage.morphology import dilation as skimage_dilation, diamond


def appliquer_dilatation(image, rayon=1):
    """Agrandit les régions blanches avec un losange de rayon donné."""
    return skimage_dilation(image, footprint=diamond(rayon))
