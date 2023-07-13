from qcodes import Instrument
from arbok.core.gettable_set import GettableSet

class DummyGettableSet(GettableSet):
    def __init__(self, name):
        super().__init__(name = name)
        self.gettables = {
            'TIMES': 's', 
            'state': None, 
            'read': 'A'
            }
        self.add_qc_gettables()