from Operateur import Operateur
from Tuple import Tuple
from Instrumentation import Instrumentation

class FullScanDisqueBloc(Instrumentation, Operateur):

    def __init__(self, table_name):
        super().__init__("FullScanDisqueBloc" + str(Instrumentation.number))
        Instrumentation.number += 1
        self.table_name = table_name

