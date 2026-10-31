"""Amélioration de la luminosité d'une image."""

from skimage.exposure import adjust_gamma


def ameliorer_luminosite(image, gain=1.2):
    """Éclaircit une image avec un gain supérieur à 1.

    `gain=1` conserve la luminosité d'origine. Une valeur inférieure à 1
    assombrit l'image.
    """
    return adjust_gamma(image, gamma=1, gain=gain)
