import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from modules.luminosite import ameliorer_luminosite
from modules.niveaux_gris import convertir_en_gris
from modules.filtre_median import appliquer_filtre_median
from modules.flou_gaussien import corriger_ombres
from modules.binarisation import img_binarisee
from modules.erosion import appliquer_erosion
from modules.dilatation import appliquer_dilatation
from modules.remplissage_trous import remplir_trous
from modules.nettoyage_masque import supprimer_petits_objets
from modules.labellisation import labelliser_objets, compter_objets, mesurer_objets
from modules.calcul import identifier_piece, calcul_montant

dossier = ""
images = []
canvas_graphique = None

def choisir_dossier():
    global dossier, images
    chemin = filedialog.askdirectory()
    if not chemin:
        return
    dossier = chemin
    label_dossier.config(text=dossier)
    images = sorted(
        fichier for fichier in os.listdir(dossier)
        if fichier.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))
        and os.path.isfile(os.path.join(dossier, fichier))
    )
    liste_images["values"] = images
    if images:
        liste_images.current(0)
    else:
        liste_images.set("")
        messagebox.showinfo("Info", "Aucune image trouvée dans ce dossier")

def lancer_traitement():
    image = liste_images.get()
    if not image or not dossier:
        messagebox.showwarning("Attention", "Sélectionne une image !")
        return
    chemin_image = os.path.join(dossier, image)
    bouton_traitement.config(state="disabled")
    statut.config(text="Traitement en cours…")
    fenetre.update_idletasks()
    try:
        traitement_image(chemin_image)
    except Exception as erreur:
        statut.config(text="Erreur pendant le traitement")
        messagebox.showerror("Erreur", f"Impossible de traiter cette image :\n{erreur}")
    finally:
        bouton_traitement.config(state="normal")

def traitement_image(chemin):
    # Même ordre et mêmes paramètres que dans main.ipynb.
    image_originale = plt.imread(Path(chemin))
    image_lum = ameliorer_luminosite(image_originale)
    image_grise = convertir_en_gris(image_lum)
    image_filtree = appliquer_filtre_median(image_grise)
    image_corrigee = corriger_ombres(image_filtree, sigma=150)
    image_binarisee = img_binarisee(image_corrigee)
    image_erodee = appliquer_erosion(image_binarisee, rayon=1)
    image_dilatee = appliquer_dilatation(image_erodee, rayon=1)
    image_sans_trous = remplir_trous(image_dilatee)
    image_masque_propre = supprimer_petits_objets(image_sans_trous, taille_min=5000)
    image_labellisee = labelliser_objets(image_masque_propre, connectivite=1)
    nombre_pieces = compter_objets(image_labellisee)
    pieces = mesurer_objets(image_labellisee, image_originale)
    liste_montant = []
    lignes = []
    for piece in pieces:
        montant = identifier_piece(piece["aire (en px)"], piece["Couleur"])
        if montant is not None:
            liste_montant.append(montant)
        lignes.append((piece, montant))
    montant_total = calcul_montant(liste_montant)
    nombre_inconnues = len(pieces) - len(liste_montant)
    texte_montant = "Montant partiel" if nombre_inconnues else "Montant total"
    resultat.config(
        text=f"Pièces détectées : {nombre_pieces}    |    "
             f"{texte_montant} : {montant_total / 100:.2f} €    |    "
             f"Pièces inconnues : {nombre_inconnues}"
    )

    etapes = [
        ("Image originale", image_originale, None),
        ("Luminosité", image_lum, None),
        ("Niveaux de gris", image_grise, "gray"),
        ("Filtre médian", image_filtree, "gray"),
        ("Correction des ombres", image_corrigee, "gray"),
        ("Binarisation", image_binarisee, "gray"),
        ("Érosion", image_erodee, "gray"),
        ("Dilatation", image_dilatee, "gray"),
        ("Remplissage des trous", image_sans_trous, "gray"),
        ("Masque nettoyé", image_masque_propre, "gray"),
        ("Pièces labellisées", image_labellisee, "nipy_spectral"),
    ]

    afficher_etapes(etapes)
    afficher_tableau(lignes)
    statut.config(text=f"Traitement terminé : {Path(chemin).name}")

def afficher_etapes(etapes):
    global canvas_graphique
    if canvas_graphique is not None:
        canvas_graphique.get_tk_widget().destroy()
        plt.close(canvas_graphique.figure)
    figure, axes = plt.subplots(4, 3, figsize=(12, 11), constrained_layout=True)
    for axe, (titre, image, cmap) in zip(axes.flat, etapes):
        axe.imshow(image, cmap=cmap)
        axe.set_title(titre, fontsize=10)
        axe.axis("off")
    for axe in list(axes.flat)[len(etapes):]:
        axe.axis("off")
    canvas_graphique = FigureCanvasTkAgg(figure, master=zone_graphique)
    canvas_graphique.draw()
    canvas_graphique.get_tk_widget().pack(fill="both", expand=True)

def afficher_tableau(lignes):
    tableau.delete(*tableau.get_children())
    for indice, (piece, montant) in enumerate(lignes, start=1):
        couleur = str(piece["Couleur"])
        aire = piece["aire (en px)"]
        montant_texte = "Inconnue" if montant is None else f"{montant / 100:.2f} €"
        tableau.insert("", "end", values=(indice, aire, couleur, montant_texte))

fenetre = tk.Tk()
fenetre.title("Détection et calcul du montant des pièces")
fenetre.geometry("1200x850")
fenetre.minsize(850, 650)
haut = ttk.Frame(fenetre, padding=12)
haut.pack(fill="x")
ttk.Button(haut, text="Sélectionner un dossier", command=choisir_dossier).pack(side="left")
label_dossier = ttk.Label(haut, text="Aucun dossier sélectionné", wraplength=550)
label_dossier.pack(side="left", padx=12)
commandes = ttk.Frame(fenetre, padding=(12, 0, 12, 10))
commandes.pack(fill="x")
ttk.Label(commandes, text="Image :").pack(side="left")
liste_images = ttk.Combobox(commandes, state="readonly", width=45)
liste_images.pack(side="left", padx=8)
bouton_traitement = ttk.Button(commandes, text="Lancer le traitement", command=lancer_traitement)
bouton_traitement.pack(side="left")
resultat = ttk.Label(fenetre, text="Sélectionne un dossier et une image pour commencer.", font=("Arial", 12, "bold"), padding=(12, 4))
resultat.pack(fill="x")
contenu = ttk.Panedwindow(fenetre, orient="horizontal")
contenu.pack(fill="both", expand=True, padx=12, pady=8)
zone_graphique = ttk.LabelFrame(contenu, text="Étapes du traitement")
contenu.add(zone_graphique, weight=4)
zone_tableau = ttk.LabelFrame(contenu, text="Pièces mesurées", padding=6)
contenu.add(zone_tableau, weight=1)
colonnes = ("numero", "aire", "couleur", "montant")
tableau = ttk.Treeview(zone_tableau, columns=colonnes, show="headings", height=18)
for identifiant, titre, largeur in [
    ("numero", "N°", 40), ("aire", "Aire (px)", 90),
    ("couleur", "Couleur", 95), ("montant", "Montant", 95),
]:
    tableau.heading(identifiant, text=titre)
    tableau.column(identifiant, width=largeur, minwidth=40, stretch=True)
barre = ttk.Scrollbar(zone_tableau, orient="vertical", command=tableau.yview)
tableau.configure(yscrollcommand=barre.set)
barre.pack(side="right", fill="y")
tableau.pack(fill="both", expand=True)
statut = ttk.Label(fenetre, text="Prêt", padding=(12, 5))
statut.pack(fill="x")

if __name__ == "__main__":
    fenetre.mainloop()
