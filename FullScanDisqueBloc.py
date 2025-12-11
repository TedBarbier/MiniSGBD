from Operateur import Operateur
from Tuple import Tuple
import os

class FullScanDisqueBloc(Operateur):
    def __init__(self, table_name):
        super().__init__()
        self.table_name = table_name
        self.current_block_id = 1
        self.file_handle = None
        self.num_columns = 0
        self.tuples_in_current_block = 0
        self.next_block_id = 0
        self.tuples_read_in_block = 0
        self.blocks_read_count = 0
        self.finished = False
        
    def open(self):
        self.current_block_id = 1
        self.blocks_read_count = 0
        self.finished = False
        self._open_block(self.current_block_id)
        
    def _open_block(self, block_id):
        if self.file_handle:
            self.file_handle.close()
            
        file_name = f"{self.table_name}.bloc{block_id}"
        try:
            self.file_handle = open(file_name, "rb")
            self.blocks_read_count += 1
            
            # Lecture de l'entête
            # 1. Nombre de colonnes
            b = self.file_handle.read(1)
            if not b:
                self.finished = True
                return
            self.num_columns = ord(b)
            
            # 2. Nombre de tuples dans le bloc
            b = self.file_handle.read(1)
            self.tuples_in_current_block = ord(b)
            
            # 3. Numéro du bloc suivant
            b = self.file_handle.read(1)
            self.next_block_id = ord(b)
            
            self.tuples_read_in_block = 0
            # print(f"DEBUG: Reading block {block_id}, entries: {self.tuples_in_current_block}, next: {self.next_block_id}")
            
        except FileNotFoundError:
            print(f"Erreur: Fichier {file_name} non trouvé.")
            self.finished = True
        except Exception as e:
            print(f"Erreur lecture bloc {block_id}: {e}")
            self.finished = True

    def next(self):
        if self.finished:
            return None
            
        if self.tuples_read_in_block >= self.tuples_in_current_block:
            # Fin du bloc actuel, passer au suivant
            if self.next_block_id == 0:
                self.finished = True
                return None
            else:
                self._open_block(self.next_block_id)
                # Vérifier si l'ouverture a réussi et s'il y a des données
                if self.finished or self.tuples_read_in_block >= self.tuples_in_current_block:
                    return None

        # Lecture d'un tuple
        t = Tuple(self.num_columns)
        for i in range(self.num_columns):
            b = self.file_handle.read(1)
            if not b:
                self.finished = True
                return None
            t.val[i] = ord(b)
            
        self.tuples_read_in_block += 1
        return t

    def close(self):
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None

    def get_blocks_read_count(self):
        return self.blocks_read_count
