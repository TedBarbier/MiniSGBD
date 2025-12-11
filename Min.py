from Instrumentation import Instrumentation
from Operateur import Operateur

class Min(Instrumentation, Operateur):

    def __init__(self, _in, _col):
        super().__init__("Min" + str(Instrumentation.number))
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
            c = self.col
            while True:
                temp = self.child.next()
                if temp is None:
                    break
                if temp.val[c] < first.val[c]:
                    self.tempValMin = temp
            self.stop()


    def next(self):
        self.start()
        if self.tempValMin is None:
            self.stop()
            return None
        else:
            ret = Tuple(1)
            ret.val[0] = self.tempValMin.val[self.col]
            self.tempValMin = None
            self.produit(ret)
            self.stop()
            return ret
    
    def close(self):
        self.child.close()