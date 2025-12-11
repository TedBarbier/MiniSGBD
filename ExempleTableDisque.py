from FullScannTableDisque import FullScanTableDisque
from FiltreEgalite import FiltreEgalite
from DBI import DBI
import os

# Note: Using relative paths for portability, assuming user replaces them as needed or runs in local dir
# But keeping user's structure in comments.

table1_path = "table1.bin"
table2_path = "table2.bin"

# 1. Generate tables if they don't exist (Helper for the example to work immediately)
# Creating dummy tables for the specific test case:
# Table 4 and Table 5 (from user example T4, T5)
# User example uses T4 (3 columns, size 10?) and T5.
# Join on T4 col 0 and T5 col 0.

# Let's generate them first
t = FullScanTableDisque(table1_path)
t.randomize(3, 10) # 3 cols, 10 rows
t.setFilePath(table2_path)
t.randomize(3, 10) # 3 cols, 10 rows

print("--- Start Execution ---")

# 2. Setup Operators
T4 = FullScanTableDisque(table1_path)
T5 = FullScanTableDisque(table2_path)

# 3. Print T4
T4.open()
print("Table T4 ****")
while True:
    t = T4.next()
    if t is None: break
    print(t)
T4.close()

# Print T5
T5.open()
print("Table T5 ****")
while True:
    t = T5.next()
    if t is None: break
    print(t)
T5.close() # Important to close before reusing in Join if using file handles? 
# Warning: DBI will open them again.

# 4. Filter on T4
# "FiltreEgalite f = new FiltreEgalite(T4, 2, 1);" -> Filter T4 where col 2 == 1
# Note: T4 must be closed/reset or re-opened by Filter. 
# Filter.open calls child.open(). FullScanTableDisque.open resets cursor. OK.
f = FiltreEgalite(T4, 2, 1) # Assumes randomized data might have 1. range is 100 so probability is low (1%).
# Force randomized range to be smaller for testing? FullScanTableDisque has hardcoded range=100.
# Let's run it as is.

f.open()
print("Filtre sur T4 (Col 2 == 1) ****")
while True:
    t = f.next()
    if t is None: break
    print(t)
f.close()

# 5. Join (DBI)
# DBI join = new DBI(T4, T5, 0, 0); -> Join T4 and T5 on col 0
join = DBI(T4, T5, 0, 0)
join.open()
print("JOIN T4.col0 = T5.col0 ****")
while True:
    t = join.next()
    if t is None: break
    print(t)
join.close()

# 6. Stats
print("-" * 30)
print(f"Stats T4: {T4}")
print(f"Stats T5: {T5}")
print(f"Stats Filter: {f}")
print(f"Stats Join: {join}")
