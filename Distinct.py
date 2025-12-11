from Instrumentation import Instrumentation
from Operateur import Operateur
from Tuple import Tuple

class Distinct(Instrumentation, Operateur):

    def __init__(self, _in):
        super().__init__("Distinct" + str(Instrumentation.number))
        Instrumentation.number += 1
        self.child = _in
        self.sortedTuples = []
        self.lastReturned = None


    def open(self):
        self.start()
        self.child.open()
        self.tuplesProduits = 0
        self.memoire = 0

        t = self.child.next()
        while True:
            if t == None:
                break
            self.sortedTuples.append(t)
            t = self.child.next()

        self.sortedTuples.sort(key=lambda t: (t.size, Tuple(t.val)))

        self.iterator = self.sortedTuples.iterator()
        self.lastReturned = None
        self.stop()

    def next(self):
        self.start()
        while self.iterator.hasNext():
            current = self.iterator.next()
            isDuplicate = False
            if self.lastReturned != None:
                if current.size == self.lastReturned.size:
                    equal = True
                    for i in range(current.size):
                        if current.val[i] != self.lastReturned.val[i]:
                            equal = False
                            break
                    if equal:
                        isDuplicate = True

            if not isDuplicate:
                self.lastReturned = current
                self.produit(current)
                self.stop()
                return current

        self.stop()
        return None

    def close(self):
        self.child.close()
