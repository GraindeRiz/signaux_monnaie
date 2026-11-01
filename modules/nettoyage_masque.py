"""Nettoyage des petites régions d'un masque binaire."""

from skimage.morphology import remove_small_objects


def supprimer_petits_objets(image, taille_min=5000):
    return remove_small_objects(image, min_size=taille_min)
