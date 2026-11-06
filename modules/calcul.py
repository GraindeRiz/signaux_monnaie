AIRES_CUIVRE = {
    1: [94_635],
    2: [120_794],
    5: [148_461],
}

AIRES_DOREE = {
    10: [131_771],
    20: [167_242],
    50: [198_659],
}

AIRES_BICOLORE = {
    100: [182_613],
    200: [220_329],
}


def identifier_piece(aire,couleur):
    if couleur == "Cuivre":
        references = AIRES_CUIVRE
    elif couleur == "Dorée":
        references = AIRES_DOREE
    elif couleur == "Bicolor":
        references = AIRES_BICOLORE
    else:
        references = AIRES_CUIVRE | AIRES_DOREE | AIRES_BICOLORE

    meilleur_ecart = float("inf")
    meilleur_montant = None

    for montant, aire_reference in references.items():
        ecart = abs(aire - aire_reference[0])
        if ecart < meilleur_ecart:
            meilleur_ecart = ecart
            meilleur_montant = montant

    return meilleur_montant


def calcul_montant(liste):
    somme = 0
    for i in liste:
        somme += i
    return somme
