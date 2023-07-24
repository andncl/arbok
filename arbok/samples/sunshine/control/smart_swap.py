
from arbok.core.sequence import Sequence
from arbok.core.sample import Sample
from arbok.samples.sunshine.configs.rf2v_config import rf2v_config
from qm.qua import *

class SmartSwap(Sequence):
    """
    Class containing parameters and sequence for a smart Y-gate
    """
    def __init__(
            self, 
            name: str,
            sample = Sample('sunshine', rf2v_config),
            config = {
                'elements': ['J1'],
                'unit_amp': {'unit': 'V', 'value': 0.5},
                'vControl2': {'unit': 'v', 'value': [0]},
                'vControlSWAP': {'unit': 'v', 'value': [0.5]},
                'tWait': {'unit': 'cycles', 'value': int(192)},
                'tSwap': {'unit': 'cycles', 'value': int(12)},
                'tControlRamp': {'unit': 'cycles', 'value': int(5)},
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
            
        align('Q1','J1')
        wait(self.tWait(),'J1')
        play('cos', 'Q1')
        play('unit_ramp_20ns'*amp(-self.vControl2_J1()+self.vControlSWAP_J1()),
                'J1', duration = self.tControlRamp())
        wait(self.tSwap(), 'J1')
        play('unit_ramp_20ns'*amp(+self.vControl2_J1()-self.vControlSWAP_J1()),
                'J1', duration = self.tControlRamp())
            
        align('Q1','P1','P2','J1','P2_not_sticky','P1_not_sticky','J1_not_sticky')