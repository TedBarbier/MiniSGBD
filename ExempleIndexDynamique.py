
from IndexHachageDynamique import IndexHachageDynamique
from Tuple import Tuple
import random
import glob
import os

def main():
    # Paramètres
    TABLE_NAME = "ExempleTable"
    NUM_COLS = 3
    NUM_ROWS = 20  # Assez pour provoquer des splits si max_per_block est petit
    KEY_COL = 0    # On indexe sur la première colonne
    MAX_PER_BLOCK = 2

    print(f"--- Génération de {NUM_ROWS} tuples aléatoires ---")
    tuples = []
    for _ in range(NUM_ROWS):
        t = Tuple(NUM_COLS)
        # On met des valeurs aléatoires. 
        # On force un peu des valeurs proches pour tester les collisions/splits si besoin
        t.val[0] = random.randint(0, 100) 
        t.val[1] = random.randint(0, 100)
        t.val[2] = random.randint(0, 100)
        tuples.append(t)
        print(f"Tuple généré: {t.val}")

    print("\n--- Initialisation de l'Index Hachage Dynamique ---")
    # On instancie l'index avec une capacité très faible (2) pour forcer les splits
    index = IndexHachageDynamique(TABLE_NAME, NUM_COLS, KEY_COL, max_per_block=MAX_PER_BLOCK)
    
    index.open(tuples)

    print("\n--- Insertion des tuples (Next) ---")
    count = 0
    while True:
        t = index.next()
        if t is None:
            break
        count += 1
        # On pourrait afficher chaque insertion mais ça ferait beaucoup de logs
        # print(f"Insertion #{count}: {t.val}")

    index.close()
    print(f"Fin de l'insertion. {count} tuples traités.")

    print("\n--- État final des fichiers (Blocs) ---")
    files = glob.glob(f"{TABLE_NAME}.*")
    files.sort()
    
    total_stored = 0
    for f_path in files:
        # On lit juste l'entête pour voir combien de tuples il y a
        with open(f_path, "rb") as f:
            # Structure : Cols (1 byte), NbTuples (1 byte)
            cols = int.from_bytes(f.read(1), "big")
            nb = int.from_bytes(f.read(1), "big")
            
            # Lecture des tuples pour affichage (optionnel)
            tuples_content = []
            for _ in range(nb):
                t_vals = []
                for _ in range(cols):
                    t_vals.append(int.from_bytes(f.read(1), "big"))
                tuples_content.append(t_vals)
            
            print(f"Fichier {f_path: <20} : {nb} tuples -> {tuples_content}")
            total_stored += nb

    print(f"\nTotal tuples stockés sur disque : {total_stored} / {NUM_ROWS}")
    
    if total_stored == NUM_ROWS:
        print("SUCCÈS : Tous les tuples sont présents.")
    else:
        print("ERREUR : Il manque des tuples !")

if __name__ == "__main__":
    main()
