""" Detemrminer le périmètre"""
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage.morphology import square,binary_erosion
from skimage.segmentation import find_boundaries

def determiner_perimetre(image,image_labellee=False):
    image = np.asarray(image)
    if image.ndim != 2:
        raise ValueError("L'image doit être en niveaux de gris ou binaire.")
    
    est_binaire = image.dtype == bool or np.all((image == 0) | (image == 1))
    if image_labellee or est_binaire:
        se=square(3)
        BWe = binary_erosion(image,se)
        BWperim = find_boundaries(BWe)
        return BWperim
