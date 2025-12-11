import random
from Tuple import Tuple
import os

class DisqueBloc:
    def __init__(self):
        self.range = 100

    def generate_table(self, tuples, table_name, num_columns, num_rows, records_per_block):

        try:
            current_row = 0
            block_num = 1
            
            while current_row < num_rows:
                # Calculer combien de tuples dans ce bloc
                remaining_rows = num_rows - current_row
                tuples_in_block = min(remaining_rows, records_per_block)
                
                # Déterminer si c'est le dernier bloc
                is_last_block = (current_row + tuples_in_block) >= num_rows
                next_block_id = 0 if is_last_block else block_num + 1
                
                file_name = f"{table_name}.bloc{block_num}"
                
                with open(file_name, "wb") as f:
                    # Écriture de l'entête
                    f.write(bytes([num_columns]))
                    f.write(bytes([tuples_in_block]))
                    f.write(bytes([next_block_id]))
                    
                    # Écriture des tuples
                    for _ in range(tuples_in_block):
                        t = Tuple(num_columns)
                        for j in range(num_columns):
                            val = tuples[current_row][j]
                            t.val[j] = val
                            f.write(bytes([val]))
                
                print(f"Bloc {block_num} généré: {file_name} ({tuples_in_block} tuples, suivant: {next_block_id})")
                
                current_row += tuples_in_block
                block_num += 1
                
        except Exception as e:
            print(f"Erreur lors de la génération de la table: {e}")

    def randomize(self):
        
