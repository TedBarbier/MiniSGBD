from Tuple import Tuple
from Instrumentation import Instrumentation
from Operateur import Operateur

class Avg(Instrumentation, Operateur):

    def __init__(self, _in, _col):
        super().__init__("Avg" + str(Instrumentation.number))
        Instrumentation.number += 1
        self.start()
        self.col = _col
        self.child = _in
        self.stop()

    def open(self):
        self.start()
        self.child.open()
        self.tuplesProduits = 0
        self.memoire = 0
        
        first = self.child.next()
        if first is not None:
            count = 1
            c = self.col
            sum = first.val[c]
            while True:
                temp = self.child.next()
                if temp is None:
                    break
                sum += temp.val[c]
                count += 1
            self.tempValAvg.val[c] = sum / count
        self.stop()

    def next(self):
        self.start()
        if self.tempValAvg is None:
            self.stop()
            return None
        else:
            ret = Tuple(1)
            ret.val[0] = self.tempValAvg.val[self.col]
            self.tempValAvg = None
            self.produit(ret)
            self.stop()
            return ret
    
    def close(self):
        self.child.close()