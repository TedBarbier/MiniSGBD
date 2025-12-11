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

def hachage_statique(t : list[Tuple], modulo : int, attribut : int, records_per_block : int):
    # Préouverture des fichiers de sortie blocs
    Table = []
    for i in range(0, modulo):
        file_name = f"table.{i}.bloc0"
        Table.append(openFile(file_name))
        # print(Table[i])
    
    # Boucle de traitement Tuple par Tuple
    Tableau_verif = [0] * modulo
    Bloc_count = [0] * modulo

    for element in t:
        index = element.val[attribut] % modulo # Calcul de l'index de hachage
        if (Tableau_verif[index] == records_per_block):
            # Si le bloc est plein, on ferme le fichier courant et on en ouvre un nouveau
            Table[index].close()
            Bloc_count[index] += 1
            print(Bloc_count[index])
            file_name = f"table.{index}.bloc{Bloc_count[index]}"
            Table[index] = openFile(file_name)
            Tableau_verif[index] = 0

            # Puis on écrit le tuple dans le nouveau bloc
            f = Table[index]
            for k in range(element.size):
                value = element.val[k]
                f.write(bytes(value))

            Tableau_verif[index] +=1
            f.seek(1)
            f.write(bytes(Tableau_verif[index]))
            f.seek(0, 2)

        else:
            # Écriture du tuple dans le bloc correspondant
            f = Table[index]
            for k in range(element.size):
                value = element.val[k]
                f.write(bytes(value))

            print(Tableau_verif[index])
            Tableau_verif[index] +=1
            print(Tableau_verif[index])
            f.seek(1)
            f.write(bytes(Tableau_verif[index]))
            f.seek(0, 2)
            
            print(f"Tuple {element.val} écrit dans le fichier table.{index}.bloc{Bloc_count[index]}")

    # Fermeture des fichiers
    for i in range(0, modulo):
        Table[i].close()    
