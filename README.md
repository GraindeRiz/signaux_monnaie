# signaux_monnaie

**Détecter les pièces, calculer le montant** — Signaux III, guide de travail (cours v4.7).

Un parcours simple : une photo, une devise hors euro, un résultat expliqué.

> **Version de départ :** pièces séparées et entièrement visibles, fond uni mat, vue du dessus, distance, zoom et résolution fixes.

Cochez les cases au fur et à mesure (`- [ ]` → `- [x]`) pour suivre l'avancement.

---

## 01 · Les outils dans l'ordre

| # | Outil et utilisation | Cours / rôle |
|---|---|---|
| 1 | **Python 3 + JupyterLab** : écrire et exécuter le notebook. NumPy pour les calculs, Matplotlib pour afficher images et résultats. | Tout le projet |
| 2 | **Téléphone, support fixe, fond mat, éclairage diffus** : photographier les pièces. Une règle aide à vérifier les dimensions réelles si nécessaire. | Acquisition |
| 3 | **scikit-image : `imread`, `rgb2gray`** : lire la photo et créer sa version en gris. Conserver aussi l'original couleur. | Ch. 8, p. 103 |
| 4 | **scikit-image : `median`** : atténuer le bruit si nécessaire avec un petit voisinage (lissage : voir ch. 3). | Ch. 8, p. 106-108 |
| 5 | **scikit-image : `threshold_otsu`** : séparer pièces et fond, produire un masque binaire avec les pièces en blanc. | Ch. 8, p. 112-113 |
| 6 | **Morphologie + SciPy : `binary_fill_holes`** : nettoyer le masque (petites ouvertures/fermetures si utile), remplir les trous parasites. | Ch. 8, p. 114-120 |
| 7 | **scikit-image : `label`, `regionprops`** : numéroter les objets, filtrer les parasites, mesurer surface, position et diamètre équivalent. | Ch. 8, p. 121-123 |
| 8 | **Table de références + règles Python/NumPy** : associer les mesures à une valeur connue, avec tolérance et rejet si ambigu. | À construire pour le projet |
| 9 | **Python `sum` ; annotations Matplotlib** : additionner les valeurs, afficher la photo annotée, le total et les éventuelles inconnues. | Restitution |

---

## 02 · Préparer et isoler les pièces

Garder une image de chaque étape : elle servira à vérifier le traitement et à l'expliquer.

### Étape 01 — Installer et organiser le projet

- [ ] Créer l'environnement et installer les bibliothèques depuis `requirements.txt` :

  ```powershell
  # Windows (PowerShell)
  py -m venv .venv
  ```

  ```bash
  # macOS / Linux
  python3 -m venv .venv
  ```

  Activer l'environnement :

  ```powershell
  # Windows (PowerShell)
  .venv\Scripts\Activate.ps1
  ```

  ```bash
  # macOS / Linux
  source .venv/bin/activate
  ```

  Puis installer les dépendances et enregistrer le noyau Jupyter :

  ```bash
  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt
  python -m ipykernel install --user --name signaux-monnaie --display-name "Python (signaux_monnaie)"
  jupyter lab
  ```

  Sous Windows, exécuter uniquement les commandes PowerShell (ne pas exécuter `source`). Si PowerShell bloque l'activation, lancer `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, puis réessayer. Pour vérifier que l'installation utilise le bon Python : `python -c "import numpy, scipy, skimage, matplotlib; print('Environnement prêt')"`.

- [X] Créer le notebook (`main.ipynb`)
- [ ] Créer les dossiers `images/calibration/`, `images/test/` et `resultats/`
- [ ] Séparer les étapes du notebook par des titres
- [ ] ✅ **Tu peux continuer quand…** le notebook s'ouvre et les bibliothèques s'importent sans erreur.

### Étape 02 — Choisir la devise et fixer la prise de vue

- [ ] Lister les valeurs et variantes de pièces acceptées
- [ ] Commencer avec trois types faciles à distinguer
- [ ] Étendre ensuite à toute la liste retenue
- [ ] Utiliser d'abord des pièces rondes, séparées, sur le même plan
- [ ] Fixer téléphone, distance, zoom, résolution et éclairage
- [ ] Prendre plusieurs photos de chaque type
- [ ] Prévoir un lot de test à part
- [ ] ✅ **Tu peux continuer quand…** une même pièce garde une taille apparente stable sur plusieurs photos.

### Étape 03 — Afficher, passer en gris, filtrer légèrement

- [ ] Charger une photo JPG ou PNG avec trois pièces
- [ ] Afficher l'original et la version en gris côte à côte
- [ ] Garder la couleur pour une éventuelle reconnaissance
- [ ] Si l'image est bruitée, tester un filtre médian à petit voisinage (ex. 3 × 3 pixels)
- [ ] Comparer avec l'image non filtrée
- [ ] ✅ **Tu peux continuer quand…** les pièces restent nettes et leurs bords ne sont pas visiblement déformés.

### Étape 04 — Séparer les pièces du fond et nettoyer

- [ ] Calculer le seuil d'Otsu sur l'image en gris
- [ ] Choisir le sens du seuil pour obtenir des pièces blanches sur fond noir (le **masque**)
- [ ] Remplir les trous parasites
- [ ] Si nécessaire, appliquer une petite ouverture ou fermeture
- [ ] Vérifier qu'aucune pièce n'est fusionnée avec une autre ni redimensionnée
- [ ] ✅ **Tu peux continuer quand…** chaque pièce donne une silhouette pleine et séparée, sans morceau de fond inclus.

---

## 03 · Des mesures au montant

Appliquer le même traitement aux photos de référence et aux photos à analyser.

### Étape 05 — Numéroter et mesurer chaque objet

- [ ] Utiliser `label` puis `regionprops`
- [ ] Afficher un numéro sur chaque objet
- [ ] Relever surface, centre et diamètre équivalent
- [ ] Écarter les petits parasites par leur surface
- [ ] Signaler les objets coupés par le bord ou de forme anormale
- [ ] Vérifier qu'une région ne contient pas deux pièces
- [ ] ✅ **Tu peux continuer quand…** chaque pièce possède un seul numéro et une ligne de mesures.

> **Diamètre équivalent :** d = 2 × √(A / π), où A est la surface du masque en pixels. C'est le diamètre d'un disque de même surface ; il n'est fiable que si la segmentation est correcte.

### Étape 06 — Construire la table de références

- [ ] Pour chaque valeur, mesurer plusieurs photos de pièces connues (ex. cinq pour commencer)
- [ ] Noter dans un tableau : valeur, diamètre moyen, variation observée
- [ ] En déduire une plage acceptable par valeur
- [ ] Si deux plages se chevauchent : ajouter un critère distinctif (ex. couleur de l'original) ou changer les types de pièces du premier prototype
- [ ] ✅ **Tu peux continuer quand…** les références permettent de distinguer les valeurs retenues, sans utiliser les photos de test.

> **Attention à l'échelle :** garder distance, zoom et résolution fixes ; sinon, recalibrer. Pour des distances variables, utiliser un repère de taille connue dans le plan de la table.

### Étape 07 — Attribuer une valeur ou signaler une inconnue

- [ ] Comparer chaque mesure aux références
- [ ] Attribuer une valeur seulement si une seule classe respecte les tolérances ; sinon indiquer **« non reconnue »**
- [ ] Tester d'abord une pièce de chaque type
- [ ] Tester ensuite une photo de pièces mélangées
- [ ] Afficher la valeur trouvée à côté de chaque numéro
- [ ] ✅ **Tu peux continuer quand…** les valeurs sont correctes et les cas ambigus restent signalés.

### Étape 08 — Calculer et afficher le montant

- [ ] Stocker les valeurs en nombres entiers dans la plus petite unité retenue
- [ ] Additionner ; convertir seulement pour l'affichage
- [ ] Afficher la photo annotée, le nombre de pièces et le montant avec la devise
- [ ] En cas d'inconnues : afficher **« sous-total des pièces reconnues »** et le nombre de pièces non reconnues
- [ ] ✅ **Tu peux continuer quand…** tu peux vérifier manuellement chaque valeur et retrouver la somme affichée.

---

## 04 · Tester et préparer la démonstration

Une nouvelle photo doit être traitée sans retoucher les paramètres à la main.

### Étape 09 — Évaluer sur des photos réservées aux tests

- [ ] Constituer un premier lot d'environ vingt photos :
  - [ ] table vide
  - [ ] une pièce
  - [ ] plusieurs exemplaires identiques
  - [ ] mélanges
  - [ ] toutes les valeurs retenues
- [ ] Varier légèrement positions et éclairage dans le cadre prévu
- [ ] Pour chaque photo, noter : nombres réel/détecté, valeurs réelles/prédites, totaux réel/calculé
- [ ] Vérifier les correspondances sur la photo (un bon compte peut cacher une détection manquée + un parasite)
- [ ] ✅ **Tu peux continuer quand…** tu connais les réussites, les erreurs et les conditions où le système fonctionne.

> **Trois résultats à présenter :** pièces correctement détectées, valeurs correctement attribuées, proportion de photos dont le total est exact. Si le programme est ajusté après un test, réserver de nouvelles photos pour l'évaluation finale.

### Étape 10 — Rendre une démonstration reproductible

- [ ] Relancer le notebook depuis le début (**Restart Kernel / Run All**)
- [ ] Vérifier que seul le chemin de la photo change pour analyser une autre image conforme
- [ ] Préparer : notebook commenté, références, images de démo, tableau de tests, consignes d'installation
- [ ] Sauvegarder les versions des bibliothèques utilisées (ex. `pip freeze > requirements.txt`)
- [ ] Montrer : original, masque, pièces numérotées et résultat
- [ ] Vérifier le format final demandé par l'enseignant
- [ ] ✅ **Tu peux continuer quand…** quelqu'un peut reproduire un exemple en suivant les consignes.

---

## Le cours à garder ouvert

| Priorité | Chapitres |
|---|---|
| **En priorité** | **Ch. 3, p. 40-44** : convolution, lissage et contours.<br>**Ch. 8, p. 103-123** : gris, filtres, seuil, morphologie, labellisation et mesures. |
| **Si nécessaire** | **Ch. 9, p. 128-129** : classification supervisée si les règles ne suffisent pas.<br>**Ch. 3, p. 45-50** : corrélation, autre piste de comparaison à des modèles. |
| **Pour expliquer** | **Ch. 5, p. 69-72** : filtres 1D, à transposer aux images.<br>**Ch. 1, p. 10-12 ; ch. 6, p. 80 et 83-88** : quantification et échantillonnage. |

*Source : Traitement de Signal Cours v4.7, 137 pages (pages du PDF, deux diapositives par page). Le protocole de prise de vue, la calibration et les critères de validation sont des propositions pour ce projet.*

**À ajouter plus tard seulement :** contours avancés, pièces qui se touchent, corrélation, apprentissage automatique ou interface dédiée. La première cible reste une chaîne simple qui fonctionne sur de nouvelles photos.
