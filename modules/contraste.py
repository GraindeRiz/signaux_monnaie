import matplotlib.pyplot as plt
from skimage.exposure import equalize_hist

def appliquer_filtre_contrast(image):
     """Reçoit une image et renvoie une version filtrée.
    
        améliore le contrast de l'image en équilibrant l'histogramme.
        """
     return equalize_hist(image)
