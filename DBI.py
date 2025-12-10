from Instrumentation import Instrumentation
from Operateur import Operateur
from Tuple import Tuple

class DBI(Instrumentation, Operateur):
    """
    Double Boucle Imbriquée (Nested Loop Join)
    """
    
    def __init__(self, leftOps, rightOps, leftCol, rightCol):
        super().__init__("DBI" + str(Instrumentation.number))
        Instrumentation.number += 1
        
        self.leftOps = leftOps
        self.rightOps = rightOps
        self.leftCol = leftCol
        self.rightCol = rightCol
        
        self.currentLeftTuple = None

    def open(self):
        self.startTime = 0
        self.stopTime = 0
        self.memoire = 0
        self.tuplesProduits = 0
        
        self.start()
        self.leftOps.open()
        self.rightOps.open()
        
        # Load first left tuple
        self.currentLeftTuple = self.leftOps.next()
        self.stop()

    def next(self):
        self.start()
        
        while self.currentLeftTuple is not None:
            # Iterate right table
            t_right = self.rightOps.next()
            
            if t_right is None:
                # End of right table -> Advance left and Reset right
                self.currentLeftTuple = self.leftOps.next()
                if self.currentLeftTuple is None:
                    break # End of join
                
                self.rightOps.close() # Usually re-opening is enough to reset scan
                self.rightOps.open()
                continue
            
            # Check Join Condition
            if self.currentLeftTuple.val[self.leftCol] == t_right.val[self.rightCol]:
                # Match found -> Merge tuples
                # Result size = size(left) + size(right)
                
                new_size = self.currentLeftTuple.size + t_right.size
                t_res = Tuple(new_size)
                
                # Copy values
                # Part 1: Left
                for i in range(self.currentLeftTuple.size):
                    t_res.val[i] = self.currentLeftTuple.val[i]
                    
                # Part 2: Right
                for i in range(t_right.size):
                    t_res.val[self.currentLeftTuple.size + i] = t_right.val[i]
                
                self.produit(t_res)
                self.stop()
                return t_res
                
        self.stop()
        return None

    def close(self):
        self.start()
        self.leftOps.close()
        self.rightOps.close()
        self.stop()
