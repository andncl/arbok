from qm.qua import align, play, wait

from arbok.core.sequence import Sequence
from arbok.core.sample import Sample

from arbok.samples.aurora.configs.aurora_qua_config import aurora_qua_config

class InitOdd6dot(Sequence):
    """
    Class containing parameters and sequence for mixed down up initialization
    """
    def __init__(
            self,
            name: str,
            sample = Sample('aurora', aurora_qua_config),
            seq_config: dict = None
    ):
        """
        Constructor method for 'MixedDownUpInit' class
        
        Args:
            name (str): name of sequence
            sample  (Sample): Sample class for physical device
            config (dict): config containing pulse parameters
        """
        super().__init__(name, sample)
        self.seq_config = seq_config
        if self.seq_config is None:
            self.seq_config = self.get_default_seq_config()
        self.add_qc_params_from_config(self.seq_config)

    def qua_sequence(self):
        """QUA sequence to perform mixed down up initialization"""
        align()
        self.arbok_go(
                from_volt = 'vHome',
                to_volt = 'vInitPreLoadMixed',
                duration = self.tInitPreLoadRampMixed,
                operation = 'unit_ramp')
        align()
        wait(self.tInitPreLoadMixed())
        align()
        self.arbok_go(
                from_volt = 'vInitPreLoadMixed',
                to_volt = 'vInitLoadMixed',
                duration = self.tInitLoadRampMixed,
                operation = 'unit_ramp')
        align()
        wait(self.tInitLoadMixed())
        align()
        self.arbok_go(
                to_volt = 'vDeltaMixed',
                duration = self.tDeltaLoadRampMixed,
                operation = 'unit_ramp')
        align()
        wait(self.tDeltaLoadMixed())
        align()
        self.arbok_go(
                from_volt = ['vDeltaMixed', 'vInitLoadMixed'],
                to_volt = 'vHome',
                duration = self.tHomeRamp,
                operation = 'unit_ramp')
        align()

    def get_default_seq_config(self, elements: list = None) -> dict:
        """ Generates the sequence configuration dictionary """
        if elements is None:
            elements = ['P1', 'J1', 'P2', 'J2', 'P3', 'P5', 'J5', 'P6']
        P1, J1, P2, J2, P3, P5, J5, P6 = elements

        config = {
            'tInitPreLoadRampMixed': {'unit': 'cycles', 'value': int(1e4/4)},
            'tInitPreLoadMixed': {'unit': 'cycles', 'value': int(200e3/4)},
            'tInitLoadRampMixed': {'unit': 'cycles', 'value': int(0.1e3/4)},
            'tInitLoadMixed': {'unit': 'cycles', 'value': int(0.1e3/4)},
            'tDeltaLoadRampMixed': {'unit': 'cycles', 'value': int(1.6e3/4)},
            'tDeltaLoadMixed': {'unit': 'cycles', 'value': int(1e3/4)},
            'tHomeRamp': {'unit': 'cycles', 'value': int(6)},

            'vHome': {'unit': 'V', 'elements': {
                P1: 0,
                J1: 0,
                P2: 0,
                J2: 0,
                P3: 0,
                P5: 0,
                J5: 0,
                P6: 0
            }},
            'vInitPreLoadMixed': {'unit': 'V', 'elements': {
                P1: -0.15,
                J1: 0.0,
                P2: 0.15,
                J2: 0,
                P3: 0,
                P5: -0.2,
                J5: 0,
                P6: 0.2
            }},
            'vInitLoadMixed': {'unit': 'V', 'elements': {
                P1: -0.1,
                J1: 0.0,
                P2: 0.1,
                J2: 0,
                P3: 0,
                P5: -0.125,
                J5: 0.19,
                P6: 0.125
            }},
            'vDeltaMixed': {'unit': 'V', 'elements': {
                P1: 0.05,
                J1: 0.0,
                P2: 0.05,
                J2: 0,
                P3: 0,
                P5: 0.06,
                J5: -0,
                P6: -0.06
            }},
        }
        return dict(config)