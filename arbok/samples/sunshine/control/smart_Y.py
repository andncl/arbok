from arbok.core.sequence import Sequence
from arbok.core.sample import Sample
from arbok.samples.sunshine.configs.rf2v_config import rf2v_config
from qm.qua import *

class SmartY(Sequence):
    """
    Class containing parameters and sequence for a smart Y-gate
    """
    def __init__(
            self, 
            name: str,
            sample = Sample('sunshine', rf2v_config),
            config = {
                'unit_amp': {'unit': 'V', 'value': 0.5},
                'amp': {'unit': 'V', 'value': 0.5},
                'smart_cycles': {'unit': '', 'value': int(5)},
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

        nn = declare(int)
        with for_(nn, 0, nn < self.smart_cycles(), nn+1):
            play('sine'*amp(self.amp()), 'P2_not_sticky')
            play('cos', 'Q1')

        align('Q1','P1','P2','J1','P2_not_sticky','P1_not_sticky','J1_not_sticky')

    def qua_declare_vars(self, simulate = False):
        y_amp = declare()
        return
    
    def qua_streams(self, simulate = False):
        return

