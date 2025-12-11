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
    
    # Boucle de traitement Tuple par Tuple
    index = t.val[attribut] % modulo
    Tableau_verif = [0] * modulo
    Bloc_count = [0] * modulo

    print(f"Index calculé pour le tuple {t.val} : {index}")

    if (Tableau_verif[index] == t.records_per_block):
        # Si le bloc est plein, on ferme le fichier courant et on en ouvre un nouveau
        Table[index].close()
        Bloc_count[index] += 1
        file_name = f"table.{i}.bloc{Bloc_count[index]}"
        Table.append(openFile(file_name))
        Tableau_verif[index] = 0

        # Puis on écrit le tuple dans le nouveau bloc
        f = Table[index]
        for k in range(t.size):
            value = t.val[k]
            f.write(bytes(value))

        Tableau_verif[index] +=1
        f.seek(1)
        f.write(bytes(Tableau_verif[index]))
        f.seek(0, 2)

    else:
        # Écriture du tuple dans le bloc correspondant
        f = Table[index]
        for k in range(t.size):
            value = t.val[k]
            f.write(bytes(value))

        Tableau_verif[index] +=1
        f.seek(1)
        f.write(bytes(Tableau_verif[index]))
        f.seek(0, 2)
        
    print(f"Tuple {t.val} écrit dans le fichier table.{index}.bloc0")
    
    # Fermeture des fichiers
    for i in range(0, modulo):
        Table[i].close()    
