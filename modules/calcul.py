"""Aires de référence mesurées sur la photo euro-61.jpeg."""

# Les montants sont en centimes et les aires en pixels carrés.
AIRES_PAR_MONTANT = {
    1: [94_635],
    2: [120_794],
    5: [148_461],
    50: [198_659],
    200: [220_329],
}


def identifier_piece(aire):
    ecart_max = 5001
    meilleur_ecart = float("inf")
    meilleur_montant = None
    

    for montant, aire_reference in AIRES_PAR_MONTANT.items():
        ecart = abs(aire - aire_reference[0])
        if ecart < meilleur_ecart:
            meilleur_ecart = ecart 
            meilleur_montant = montant

    if meilleur_ecart > ecart_max:
        raise ValueError("Pièce inconnue")    

    return meilleur_montant 
