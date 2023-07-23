
from arbok.core.sequence import Sequence
from arbok.core.sample import Sample
from arbok.samples.sunshine.configs.rf2v_config import rf2v_config
from qm.qua import *

class Square(Sequence):
    """ Class containing parameters and sequence for a smart Y-gate """
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
        Constructor method for square pulse on J1 class

        Args:
            name (str): name of the sequence
            sample (Sample): Sample (class) on which sequence is performed
            config (dict): Dict containing all parameter info for sequence
        """
        super().__init__(name, sample)
        self.config = config
        self.add_qc_params_from_config(self.config)

    def qua_sequence(self):
        """ QUA sequence to perform square pulse """

        align('Q1','P1','P2','J1','P2_not_sticky','P1_not_sticky','J1_not_sticky')
        wait(self.tWait(),'J1')
        play('unit_ramp_20ns'*amp(self.amp()),
                'J1')
        wait(self.tSquare(),'J1')
        play('unit_ramp_20ns'*amp(-self.amp()),
                'J1')
        wait(self.tWait(),'J1')
        align('Q1','P1','P2','J1','P2_not_sticky','P1_not_sticky','J1_not_sticky')


class DummyRead(Sequence):
    """ Class containing parameters and sequence for a short dummy """
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
        pass