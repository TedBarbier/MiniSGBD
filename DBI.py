from Instrumentation import Instrumentation
from Operateur import Operateur
from Tuple import Tuple

class DBI(Instrumentation, Operateur):

    def __init__(self, o1, o2, c1, c2):
        super().__init__("DBI" + str(Instrumentation.number))
        Instrumentation.number += 1
        self.op1 = o1
        self.op2 = o2
        self.col1 = c1
        self.col2 = c2

    def open(self):
        self.start()
        self.op1.open()
        self.nouveauTour = True
        self.t1 = None
        self.t2 = None
        self.stop()
        
    def next(self):
        self.start()
        if (self.nouveauTour):
            while True:
                self.t1 = self.op1.next()
                if (self.t1 == None):
                    break
                self.op2.open()
                self.nouveauTour = False
                while True:
                    self.t2 = self.op2.next()
                    if (self.t2 == None):
                        break
                    if (self.t1.val[self.col1] == self.t2.val[self.col2]):
                        ret = Tuple(len(self.t1.val) + len(self.t2.val))
                        for i in range(len(self.t1.val)):
                            ret.val[i] = self.t1.val[i]
                        for i in range(len(self.t2.val)):
                            ret.val[i + len(self.t1.val)] = self.t2.val[i]
                        self.produit(ret)
                        self.stop()
                        return ret
                self.nouveauTour = True
            self.stop()
            return None    
        else:
            while True:
                self.t2 = self.op2.next()
                if (self.t2 == None):
                    break
                if (self.t1.val[self.col1] == self.t2.val[self.col2]):
                    ret = Tuple(len(self.t1.val) + len(self.t2.val))
                    for i in range(len(self.t1.val)):
                        ret.val[i] = self.t1.val[i]
                    for i in range(len(self.t2.val)):
                        ret.val[i + len(self.t1.val)] = self.t2.val[i]
                    self.produit(ret)
                    self.stop()
                    return ret
            self.nouveauTour = True
            self.stop()
            return self.next()

    def close(self):
        self.op1.close()
        self.op2.close()
        
