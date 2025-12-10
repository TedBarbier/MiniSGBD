from Instrumentation import Instrumentation
from Operateur import Operateur
from Tuple import Tuple

class FiltreEgalite(Instrumentation, Operateur):
    
    def __init__(self, _in, _col, _val):
        super().__init__("FiltreEgalite" + str(Instrumentation.number))
        Instrumentation.number += 1
        
        self.child = _in
        self.col = _col
        self.valeur = _val # The value to compare against

    def open(self):
        self.startTime = 0
        self.stopTime = 0
        self.memoire = 0
        self.tuplesProduits = 0
        self.start()
        self.child.open()
        self.stop()

    def next(self):
        self.start()
        while True:
            t = self.child.next()
            if t is None:
                self.stop()
                return None
            
            # Check equality
            # Assuming strictly integer comparison or same type
            if t.val[self.col] == self.valeur:
                self.produit(t)
                self.stop()
                return t
        self.stop()
        return t

    def close(self):
        self.child.close()

    