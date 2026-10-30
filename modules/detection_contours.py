"""Détection des contours dans une image en niveaux de gris."""

import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.color import rgb2gray

def detecter_contours(image):
    distance = 3
    ligne, colonne = image.shape
    img_contours = np.zeros_like(image)

    for i in range(ligne-distance):
        for j in range(colonne-distance):
            img_contours[i,j] = np.sqrt((image[i,j] - image[i,j+distance])**2+(image[i,j] - image[i+distance,j])**2
    ) 

    return img_contours