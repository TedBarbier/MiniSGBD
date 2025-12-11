from Operateur import Operateur
from Instrumentation import Instrumentation
from collections import deque
from Tuple import Tuple
import random
import os

class FullScanTableDisque(Instrumentation, Operateur):
    
    def __init__(self, file_path):
        super().__init__("FullScanDisque" + str(Instrumentation.number))
        Instrumentation.number += 1
        
        self.filePath = file_path
        self.taille = 0
        self.tupleSize = 0
        self.range = 100
        self.blockSize = 4
        self.blockCursor = 0
        self.memorySize = 3 # nombre de blocs
        
        # Cache: Tuple[memorySize][blockSize]
        self.cache = [[None for _ in range(self.blockSize)] for _ in range(self.memorySize)]
        
        self.q = deque()
        self.currentMemoryBlock = 0
        
        self.myReader = None
        self.start_flag = True
        self.reads = 0

    def open(self):
        self.openFile()
        self.start_flag = True
        self.q.clear()
        # Reset cache logic if needed, but array structure persists
        # Counters reset
        self.tuplesProduits = 0
        self.memoire = 0
        self.startTime = 0
        self.stopTime = 0
    
    def close(self):
        if self.myReader:
            self.myReader.close()
            self.myReader = None
            
    def setFilePath(self, fp):
        self.filePath = fp
        
    def next(self):
        # Logic: if start or block consumed -> load next block
        if self.start_flag or self.blockCursor == self.blockSize:
            self.readNextBlock()
            self.blockCursor = 0
            self.start_flag = False
            
        t = self.cache[self.currentMemoryBlock][self.blockCursor]
        self.blockCursor += 1
        
        if t is not None:
             self.produit(t)

        return t
        
    def openFile(self):
        try:
            # Mode 'rb' pour lire des bytes comme des entiers (0-255)
            self.myReader = open(self.filePath, "rb")
            
            # Header: taille table puis taille tuple
            # On lit 1 octet à chaque fois
            b = self.myReader.read(1)
            if b: self.taille = ord(b)
            
            b = self.myReader.read(1)
            if b: self.tupleSize = ord(b)
            
        except FileNotFoundError:
            print("Erreur de lecture: fichier introuvable")
        except Exception as e:
            print(f"Erreur de lecture: {e}")

    def readNextBlock(self):
        try:
            # Gestion de la queue FIFO pour les blocs en mémoire
            if len(self.q) < self.memorySize:
                self.currentMemoryBlock = len(self.q)
                self.q.append(len(self.q))
            else:
                last_block = self.q.popleft()
                self.currentMemoryBlock = last_block
                self.q.append(last_block)
                
            for i in range(self.blockSize):
                t = Tuple(self.tupleSize)
                valid_tuple = True
                
                for j in range(self.tupleSize):
                    b = self.myReader.read(1)
                    if not b: # EOF
                        t.val[0] = -1 # Marker for EOF/Invalid based on Java logic
                        valid_tuple = False
                        break # Stop reading this tuple
                    t.val[j] = ord(b)
                
                # Check control value
                # "if(t.val[0] != -1)" logic from Java
                # Note: In Java code provided, read() returns -1 on EOF.
                # Here we simulate valid check. 
                # If we hit EOF, we mark slot as None or logic specific
                
                if valid_tuple:
                     self.cache[self.currentMemoryBlock][i] = t
                else:
                     self.cache[self.currentMemoryBlock][i] = None

            self.reads += 1
            
        except Exception as e:
            print(f"Erreur de lecture block: {e}")

    def randomize(self, tuple_size, table_size):
        try:
            with open(self.filePath, "wb") as myWriter:
                # Header
                myWriter.write(bytes([table_size]))
                myWriter.write(bytes([tuple_size]))
                
                for i in range(table_size):
                    t = Tuple(tuple_size)
                    for j in range(tuple_size):
                        val = int(random.random() * self.range)
                        t.val[j] = val
                        myWriter.write(bytes([val]))
            
            print("Table générée sur disque")
            self.taille = table_size # Update internal size
            
        except Exception as e:
            print(f"Erreur écriture fichier: {e}")