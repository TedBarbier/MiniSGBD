# En paramètres le modulo et l'attribut sur lequel on va indexer le tri
from Tuple import Tuple
import os

def openFile(file_name):
    try:
        # Mode 'rb' pour lire des bytes comme des entiers (0-255)
        myWriter = open(file_name, "wb")
        return myWriter
    
    except FileNotFoundError:
        print("Erreur de lecture: fichier introuvable")
    except Exception as e:
        print(f"Erreur de lecture: {e}")

def hachage_statique(t : Tuple, modulo : int, attribut : int, records_per_block : int):
    # Préouverture des fichiers de sortie blocs
    Table = []
    for i in range(0, modulo):
        file_name = f"table.{i}.bloc0"
        Table.append(openFile(file_name))
        print(Table[i])
    
tuple = Tuple(3)
hachage_statique(tuple, 5, 1, records_per_block=4)
