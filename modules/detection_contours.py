"""Détection des contours dans une image grise, binaire ou labellisée."""

import numpy as np
from skimage.filters import sobel
from skimage.segmentation import find_boundaries


def detecter_contours(image, image_labellee=False):
    """Renvoie les frontières d'un masque ou le gradient d'une image grise."""
    image = np.asarray(image)
    if image.ndim != 2:
        raise ValueError("L'image doit être en niveaux de gris ou binaire.")

    est_binaire = image.dtype == bool or np.all((image == 0) | (image == 1))
    if image_labellee or est_binaire:
        return find_boundaries(image, mode="inner")

    return sobel(image)
