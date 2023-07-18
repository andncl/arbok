
from arbok.core.sequence import Sequence
from arbok.core.sample import Sample
from arbok.samples.sunshine.configs.rf2v_config import rf2v_config
from qm.qua import *

class Square(Sequence):
    """
    Class containing parameters and sequence for a smart Y-gate
    """
    def __init__(
            self, 
            name: str,
            sample = Sample('sunshine', rf2v_config),
            config = {
                'elements': ['J1'],
                'amp': {'unit': 'V', 'value': 0.5},
                'tWait': {'unit': 'cycles', 'value': int(20)},
                'tSquare': {'unit': 'cycles', 'value': int(4)},
            },
    ):
        """
        Constructor method for 'SmartY' class
        
        Args:
            name (str): name of sequence
            config (dict): config containing pulse parameters
        """
        super().__init__(name, sample)
        self.config = config
        self.add_qc_params_from_config(self.config)

    def qua_sequence(self, simulate = False):
        """QUA sequence to perform smart Y-gate"""

        align('Q1','P1','P2','J1','P2_not_sticky','P1_not_sticky','J1_not_sticky')
        wait(self.tWait(),'J1')
        play('unit_ramp_20ns'*amp(self.amp()),
                'J1')
        wait(self.tSquare(),'J1')
        play('unit_ramp_20ns'*amp(-self.amp()),
                'J1')
        wait(self.tWait(),'J1')
        align('Q1','P1','P2','J1','P2_not_sticky','P1_not_sticky','J1_not_sticky')