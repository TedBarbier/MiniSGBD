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
    
    print("--- Génération de la table ---")
    db = DisqueBloc()
    db.generate_table(table_name, num_columns, num_rows, records_per_block)
    
    print("\n--- Lecture de la table ---")
    fs = FullScanDisqueBloc(table_name)
    fs.open()
    
    count = 0
    t = fs.next()
    while t is not None:
        count += 1
        print(f"Tuple {count}: {t}")
        t = fs.next()
        
    fs.close()
    
    blocks_read = fs.get_blocks_read_count()
    print(f"\nNombre total de tuples lus: {count}")
    print(f"Nombre de blocs lus: {blocks_read}")
    
    if count == 10 and blocks_read == 3:
        print("SUCCESS: Le test a réussi.")
    else:
        print("FAILURE: Le test a échoué.")

if __name__ == "__main__":
    test_disque_bloc()
