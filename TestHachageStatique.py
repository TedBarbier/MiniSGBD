from IndexHachageStatique import hachage_statique
from Tuple import Tuple

# Test avec plusieurs tuples
tuple1 = Tuple(3)
tuple1.val = [1, 10, 100]
hachage_statique(tuple1, 5, 1, records_per_block=4)

tuple2 = Tuple(3)
tuple2.val = [2, 15, 200]
hachage_statique(tuple2, 5, 1, records_per_block=4)

tuple3 = Tuple(3)
tuple3.val = [3, 20, 300]
hachage_statique(tuple3, 5, 1, records_per_block=4)

tuple4 = Tuple(3)
tuple4.val = [4, 25, 400]
hachage_statique(tuple4, 5, 1, records_per_block=4)

tuple5 = Tuple(3)
tuple5.val = [5, 30, 500]
hachage_statique(tuple5, 5, 1, records_per_block=4)