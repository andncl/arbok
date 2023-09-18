from typing import List, Optional

from qm.qua import wait, align, ramp_to_zero
from arbok.core.sample import Sample
from arbok.core.read_sequence import ReadSequence
from arbok.QMv2.Readout import Readout
from arbok.samples.aurora.configs.aurora_qua_config import aurora_qua_config

class PSB6dotRead(ReadSequence):
    """
    Class containing parameters and sequence for mixed down up initialization
    Args:
        param_config (dict): Dict containing all program parameters 
    """
    def __init__(
            self,
            name: str,
            sample = Sample('aurora', aurora_qua_config),
            seq_config: dict = None,
    ):
        """
        Constructor method for 'DummyReadout' class
        
        Args:
        unit_amp (float): unit amplitude of all pulses
        """
        super().__init__(name, sample)
        self.seq_config = seq_config
        if self.seq_config is None:
            self.seq_config = self.get_default_seq_config()
        self.add_qc_params_from_config(self.seq_config)

        self.ref_set1 = Readout('ref_set1', self, read_label = 'SDC1')
        self.ref_set2 = Readout('ref_set2', self, read_label = 'SDC2')
        self.read_set1 = Readout('read_set1', self, read_label = 'SDC1')
        self.read_set2 = Readout('read_set2', self, read_label = 'SDC2')
        self.diff_set1 = Readout('diff_set1', self, read_label = 'SDC1')
        self.diff_set2 = Readout('diff_set2', self, read_label = 'SDC2')

        self.diff_set1.threshold = -0.00
        self.diff_set1.threshold = -0.004
        self.readouts = [   self.ref_set1, self.ref_set2,
                            self.read_set1, self.read_set2,
                            self.diff_set1, self.diff_set2  ]
        self.add_gettables_from_readouts()

    def qua_declare(self):
        """ QUA variable declaration for mixed down up initialization """
        for readout in self.readouts:
            readout.init_qua_vars()

    def qua_sequence(self):
        """QUA sequence to perform mixed down up initialization"""

        align()
        wait(self.tHomeWait(), 'P1')
        # To measurement point
        align()
        self.arbok_go(
                from_volt = 'vHome',
                to_volt = 'vPreRead',
                duration = self.tPreReadRamp,
                operation = 'unit_ramp')
        align()
        wait(self.tPreRead(), 'SDC1')
        # physical REFERENCE measurement
        self.ref_set1.measureAndSave()
        self.ref_set2.measureAndSave()
        align()
        wait(self.tReadPost(), 'SDC1')
        align()

        self.arbok_go(
                from_volt = 'vPreRead',
                to_volt = 'vRead',
                duration = self.tReadRamp,
                operation = 'unit_ramp')

        align()
        wait(self.tPreRead(), 'SDC1')
        align()
        # physical READ measurement
        self.read_set1.measureAndSave()
        self.read_set2.measureAndSave()
        align()
        wait(self.tReadPost(), 'SDC1')
        align()
        self.arbok_go(
                from_volt = 'vRead',
                to_volt = 'vHome',
                duration = self.tPreReadRamp,
                operation = 'unit_ramp')
        align()
        wait(self.tShotPost(), 'P1')
        # calculating the difference of acquired results at READ and REF point
        self.diff_set1.takeDiff(self.read_set1, self.ref_set1)
        self.diff_set2.takeDiff(self.read_set2, self.ref_set2)

        align()
        ramp_to_zero('P1')
        ramp_to_zero('J1')
        ramp_to_zero('P2')
        ramp_to_zero('J2')
        ramp_to_zero('P3')
        ramp_to_zero('P5')
        ramp_to_zero('J5')
        ramp_to_zero('P6')
        align()

    def get_default_seq_config(
            self, elements: Optional[List[str]] = None) -> dict:
        """ 
        Generates the sequence configuration dictionary 
        
        Args:
            elements (list(str)): list of elements of importance for config

        Returns:
            dict: Configuration dictionairy for qua sequence
        """
        if elements is None:
            elements = ['P1', 'J1', 'P2', 'J2', 'P3', 'P5', 'J5', 'P6']
        P1, J1, P2, J2, P3, P5, J5, P6 = elements

        config = {
            'tHomeWait': {'unit': 'cycles', 'value': int(100e3/4)},
            'tPreRead': {'unit': 'cycles', 'value': int(10e3/4)},
            'tPreReadRamp': {'unit': 'cycles', 'value': int(0.1e3/4)},
            'tReadPost': {'unit': 'cycles', 'value': int(0.1e3/4)},
            'tReadRamp': {'unit': 'cycles', 'value': int(4e3/4)},
            'tShotPost': {'unit': 'cycles', 'value': int(4e3/4)},

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
            'vPreRead': {'unit': 'V', 'elements': {
                P1: -0.045,
                J1: -0.1,
                P2: 0.045,
                J2: 0.0,
                P3: 0.0,
                P5: -0.06,
                J5: 0.0,
                P6: 0.06
            }},
            'vRead': {'unit': 'V', 'elements': {
                P1: -0.085,
                J1: -0.1,
                P2: 0.045,
                J2: 0.0,
                P3: 0.0,
                P5: -0.1,
                J5: 0.0,
                P6: 0.1
            }},
        }
        return config