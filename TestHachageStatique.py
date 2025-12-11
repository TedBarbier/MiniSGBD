from IndexHachageStatique import hachage_statique
from Tuple import Tuple

# Test avec plusieurs tuples
tuple1 = Tuple(3)
tuple1.val = [1, 24, 100]

tuple2 = Tuple(3)
tuple2.val = [2, 31, 200]

tuple3 = Tuple(3)
tuple3.val = [3, 28, 300]

tuple4 = Tuple(3)
tuple4.val = [4, 16, 400]

tuple5 = Tuple(3)
tuple5.val = [5, 2, 500]

tuple6 = Tuple(3)
tuple6.val = [5, 2, 500]

tuple7 = Tuple(3)
tuple7.val = [5, 2, 500]

tuple8 = Tuple(3)
tuple8.val = [5, 2, 500]

tuple9 = Tuple(3)
tuple9.val = [5, 2, 500]

tuple10 = Tuple(3)
tuple10.val = [5, 2, 500]

tuple11 = Tuple(3)
tuple11.val = [5, 2, 500]

tuple12 = Tuple(3)
tuple12.val = [5, 2, 500]

tuple13 = Tuple(3)
tuple13.val = [5, 2, 500]

tuples = [tuple1, tuple2, tuple3, tuple4, tuple5, tuple6, tuple7, tuple8, tuple9, tuple10, tuple11, tuple12, tuple13]
hachage_statique(tuples, modulo=5, attribut=1, records_per_block=3)