from DisqueBloc import DisqueBloc
from FullScanDisqueBloc import FullScanDisqueBloc
import os

def test_disque_bloc():
    table_name = "table1"
    num_columns = 4
    num_rows = 10
    records_per_block = 4
    
    # Nettoyage préalable
    for i in range(1, 5):
        try:
            os.remove(f"{table_name}.bloc{i}")
        except OSError:
            pass

    # Début du test
    print("--- Génération de la table ---")
    db = DisqueBloc()
    # db.generate_table(table_name, num_columns, num_rows, records_per_block)
    tuples = db.randomize(num_columns, num_rows)
    db.generate_table(tuples, table_name, num_columns, num_rows, records_per_block)

    print("\n--- Test de FullScanDisqueBloc ---")

    # 1. Création de l'opérateur
    scan = FullScanDisqueBloc(table_name)
    
    # 2. Ouverture
    scan.open()
    
    print("Lecture des tuples via FullScan :")
    count = 0
    while True:
        # 3. Itération avec next()
        t = scan.next()
        if t is None:
            break
            
        print(f"Tuple lu {count+1}: {t}")
        count += 1
        
    # 4. Fermeture
    scan.close()
    
    print(f"\nTotal tuples lus : {count}")
    print(f"Attendu : {num_rows}")
    
    if count == num_rows:
        print("✅ SUCCÈS : Tous les tuples ont été lus correctement !")
    else:
        print("❌ ÉCHEC : Nombre de tuples incorrect.")
    
if __name__ == "__main__":
    test_disque_bloc()
