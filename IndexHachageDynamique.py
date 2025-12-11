


import os
import glob
import math
from Tuple import Tuple

class IndexHachageDynamique:
    def __init__(self, table_name, num_columns, key_col_index, max_per_block=4):
        self.table_name = table_name
        self.num_columns = num_columns
        self.key_col_index = key_col_index
        self.max_per_block = max_per_block
        self.source_tuples = []
        self.current_pos = 0

    def _get_hash_binary(self, value):
        # On inverse la chaîne binaire pour utiliser les bits de poids faible (LSB)
        # comme préfixe pour le nom des fichiers.
        if isinstance(value, int):
            return format(value, '032b')[::-1]
        
        # Pour les autres types, on inverse aussi
        return format(hash(value) % 256, '08b')[::-1]

    def _init_storage(self):
        for f in glob.glob(f"{self.table_name}.*"):
            parts = f.split('.')
            if len(parts) > 1:
                ext = parts[-1]
                if all(c in '01' for c in ext):
                    try:
                        os.remove(f)
                    except OSError:
                        pass
        
        # Création des deux blocs initiaux : .0 et .1
        self._create_empty_block("0")
        self._create_empty_block("1")
    
    def _create_empty_block(self, suffix):
        filename = f"{self.table_name}.{suffix}"
        with open(filename, "wb") as f:
            f.write(bytes([self.num_columns])) # Entête : Nombre de colonnes
            f.write(bytes([0]))                # Entête : Nombre de tuples (0)

    def open(self, tuples: list[Tuple]):
        self.source_tuples = tuples
        self.current_pos = 0
        self._init_storage()

    def next(self):
        if self.current_pos >= len(self.source_tuples):
            return None
        
        tuple_obj = self.source_tuples[self.current_pos]
        self.current_pos += 1
        
        self._insert(tuple_obj)
        return tuple_obj

    def close(self):
        pass

    def _find_target_block(self, hash_bin):
        candidates = glob.glob(f"{self.table_name}.*")
        
        best_match = None
        max_len = -1
        
        for fname in candidates:
            suffix = fname.split('.')[-1]
            # Vérifier si c'est bien un bloc binaire
            if not all(c in '01' for c in suffix):
                continue
                
            if hash_bin.startswith(suffix):
                if len(suffix) > max_len:
                    max_len = len(suffix)
                    best_match = suffix
        
        return best_match

    def _insert(self, tuple_obj):
        key_val = tuple_obj.val[self.key_col_index]
        hash_bin = self._get_hash_binary(key_val)
        
        block_suffix = self._find_target_block(hash_bin)
        if block_suffix is None:
            # Cas théoriquement impossible si on initialise avec 0 et 1 et qu'on couvre tout l'espace
            print(f"Erreur: Aucun bloc trouvé pour {hash_bin}")
            return

        block_filename = f"{self.table_name}.{block_suffix}"
        
        # 1. Lire le bloc pour voir s'il y a de la place
        tuples_in_block = []
        with open(block_filename, "rb") as f:
            cols = int.from_bytes(f.read(1), "big")
            nb_tuples = int.from_bytes(f.read(1), "big")
            
            for _ in range(nb_tuples):
                t = Tuple(cols)
                for i in range(cols):
                    val = int.from_bytes(f.read(1), "big")
                    t.val[i] = val
                tuples_in_block.append(t)


        # 2. Vérifier la capacité
        if len(tuples_in_block) < self.max_per_block:
            # OK, on ajoute à la fin
            with open(block_filename, "r+b") as f: # r+b pour lecture/écriture sans écraser
                 # Mettre à jour le compteur (2ème octet)
                f.seek(1)
                f.write(bytes([len(tuples_in_block) + 1]))
                
                # Aller à la fin pour ajouter le tuple
                f.seek(0, 2) 
                for v in tuple_obj.val:
                    f.write(bytes([v]))
        else:
            # Récupérer tous les tuples (ceux du fichier + le nouveau)
            all_tuples = tuples_in_block + [tuple_obj]
            
            # Supprimer l'ancien fichier
            os.remove(block_filename)
            
            # Créer les nouveaux suffixes
            new_suffix_0 = block_suffix + "0"
            new_suffix_1 = block_suffix + "1"
            
            self._create_empty_block(new_suffix_0)
            self._create_empty_block(new_suffix_1)
            
            for t in all_tuples:
                self._insert(t)
