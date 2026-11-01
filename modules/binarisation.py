"""Binarisation d'une image en niveaux de gris."""

from skimage.filters import threshold_otsu


def img_binarisee(image, objet_sombre=True):
    """Sépare l'objet du fond avec Otsu.

    Par défaut, les pixels sombres (comme les pièces sur fond clair) deviennent
    le premier plan. Utiliser `objet_sombre=False` pour un objet clair.
    """
    seuil = threshold_otsu(image)
    if objet_sombre:
        return image < seuil
    return image > seuil
