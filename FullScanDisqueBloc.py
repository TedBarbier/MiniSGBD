from Operateur import Operateur
from Tuple import Tuple
from Instrumentation import Instrumentation
from collections import deque
import os

class FullScanDisqueBloc(Instrumentation, Operateur):

    def __init__(self, table_name):
        super().__init__("FullScanDisqueBloc" + str(Instrumentation.number))
        Instrumentation.number += 1
        self.table_name = table_name
        self.file_name = self.table_name + "bloc1"

    def open(self):
        self.openFile()
        self.start_flag = True
        self.tuples_in_block = self.num_tuples
        self.tuplesProduits = 0
        self.memoire = 0
        self.startTime = 0
        self.stopTime = 0
        t = Tuple(self.num_columns)
        for j in range(self.num_columns):
            b = self.myReader.read(1)
            t.val[j] = b[0]
            self.tuplesProduits += 1
        return t
        
    def openFile(self):
        try:
            # Mode 'rb' pour lire des bytes comme des entiers (0-255)
            self.myReader = open(self.file_name, "rb")
            
            # Header: 
            # On lit 1 octet à chaque fois
            self.num_columns = self.myReader.read(1)[0]
            self.num_tuples = self.myReader.read(1)[0]
            self.next_block_id = self.myReader.read(1)[0]

            
        except FileNotFoundError:
            print("Erreur de lecture: fichier introuvable")
        except Exception as e:
            print(f"Erreur de lecture: {e}")

    def next(self):
        if self.next_block_id != 0:
            self.myReader.close()
            self.file_name = self.table_name + "bloc" + str(self.next_block_id)
            self.openFile()
            t = Tuple(self.num_columns)
            for j in range(self.num_columns):
                b = self.myReader.read(1)
                t.val[j] = b[0]
                self.tuplesProduits += 1
            return t
        else:
            self.myReader.close()
            return None
    def close(self):
        if self.myReader:
            self.myReader.close()
            self.myReader = None
