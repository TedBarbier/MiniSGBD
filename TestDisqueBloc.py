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

    db.display_bloc_content("table1", 1)
    db.display_bloc_content("table1", 2)
    db.display_bloc_content("table1", 3)
    
if __name__ == "__main__":
    test_disque_bloc()
