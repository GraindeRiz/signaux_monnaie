"""Correction des ombres par estimation de l'éclairage avec OpenCV."""

import cv2
import numpy as np


def corriger_ombres(image, sigma=25):
    """Compense les variations lentes d'éclairage d'une image en niveaux de gris.

    Un grand sigma estime l'éclairage de fond sans conserver les détails de la pièce.
    L'image d'entrée doit être en niveaux de gris avec des valeurs entre 0 et 1.
    """
    image = np.asarray(image, dtype=np.float32)
    fond = cv2.GaussianBlur(
        image,
        (0, 0),
        sigmaX=float(sigma),
        sigmaY=float(sigma),
        borderType=cv2.BORDER_REFLECT,
    )
    eclairage_moyen = float(np.mean(fond))
    image_corrigee = image * eclairage_moyen / np.maximum(fond, 1e-6)
    return np.clip(image_corrigee, 0, 1)
