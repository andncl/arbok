from arbok.core.sequence import SubSequence
import numpy as np
from qm.qua import *

class DummyReadout(SubSequence):
    """
    Class containing parameters and sequence for mixed down up initialization
    """
    def __init__(
            self, 
            unit_amp = 0.499,
            ):
        """
        Constructor method for 'DummyReadout' class
        
        Args:
            unit_amp (float): unit amplitude of all pulses
        """
        super().__init__()
        self.unit_amp = unit_amp

    def sequence(self):
        """QUA sequence to perform mixed down up initialization"""
        pass