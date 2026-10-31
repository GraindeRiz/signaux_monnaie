import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu

def img_binarisee(image):
    """Reçoit une image en noir et blanc et renvoie une version binarisée.
        
    ?.
    """
    seuil = threshold_otsu(image)
    imgBinaire = image > seuil
    return imgBinaire

