from arbok.core.sequence import Sequence
from arbok.core.sample import Sample

from arbok.samples.aurora.configs.aurora_qua_config import aurora_qua_config

from qm.qua import update_frequency, wait, align

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
                to_volt = 'vControl',
                duration = self.tControlRamp(),
                operation = 'unit_ramp_20ns')
        align()
        wait(self.tControlPre, 'P1')
        align()
        update_frequency('Q1',self.IfQ1)
        update_frequency('Q2',self.IfQ2)
        align()

        """ Control part belongs here"""
        align()
        wait(self.tControlPost, 'P1')
        align()
        self.arbok_go(
                from_volt = 'vHome',
                to_volt = 'vControl',
                duration = self.tControlRamp(),
                operation = 'unit_ramp_20ns')
        align()
        wait(self.tHomeWait, 'P1')

    def get_default_seq_config(self, elements: list = None) -> dict:
        """ Generates the sequence configuration dictionary """
        if elements is None:
            elements = ['P1', 'J1', 'P2', 'J2', 'P3', 'P5', 'J5', 'P6']
        P1, J1, P2, J2, P3, P5, J5, P6 = elements

        config = {
            'tControlRamp': {'unit': 'cycles', 'value': int(6)},
            'tControlPre': {'unit': 'cycles', 'value': int(6)},
            'tControlPost': {'unit': 'cycles', 'value': int(6)},
            'tHomeWait': {'unit': 'cycles', 'value': int(100e3/4)},
            
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
            'vControl': {'unit': 'V', 'elements': {
                P1: -0.0,
                J1: 0.0,
                P2: 0.0,
                J2: 0.0,
                P3: 0.0,
                P5: -0.0,
                J5: -0.4,
                P6: 0.0
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