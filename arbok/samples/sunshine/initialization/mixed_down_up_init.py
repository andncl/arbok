from arbok.core.sequence import Sequence
from arbok.core.sample import Sample

from arbok.samples.sunshine.configs.rf2v_config import rf2v_config

from qm.qua import *

class MixedDownUpInit(Sequence):
    """
    Class containing parameters and sequence for mixed down up initialization
    """
    def __init__(
            self,
            name: str,
            sample = Sample('sunshine', rf2v_config),
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
        play('unit_ramp'*amp(self.vInitMixed2_P1() - self.vHome_P1()),'P1',
            duration=self.tInitLoadRamp())
        play('unit_ramp'*amp(self.vInitMixed2_J1() - self.vHome_J1()),'J1',
            duration=self.tInitLoadRamp())
        play('unit_ramp'*amp(self.vInitMixed2_P2() - self.vHome_P2()),'P2',
            duration=self.tInitLoadRamp())
        wait(self.tInitLoadMixed(),'P1','P2','J1')
        align()
        play('unit_ramp'*amp(self.vInitPreLoadMixed1_P1() - self.vInitMixed2_P1()),
             'P1', duration=self.tInitLoadRamp())
        play('unit_ramp'*amp(self.vInitPreLoadMixed1_J1() - self.vInitMixed2_J1()),
             'J1', duration=self.tInitLoadRamp())
        play('unit_ramp'*amp(self.vInitPreLoadMixed1_P2() - self.vInitMixed2_P2()),
             'P2', duration=self.tInitLoadRamp())
        wait(self.tControl(),'P1','P2','J1')
        align()
        play('unit_ramp'*amp(self.vDeltaM_P1()), 'P1',
             duration=self.tPreControlRampMixed())
        play('unit_ramp'*amp(self.vDeltaM_J1()), 'J1',
             duration=self.tPreControlRampMixed())
        play('unit_ramp'*amp(self.vDeltaM_P2()), 'P2',
             duration=self.tPreControlRampMixed())
        wait(self.tPreControl(),'P1','P2','J1')
        align()  
        play('unit_ramp'*amp(
            self.vHome_P1()- self.vDeltaM_P1()-self.vInitPreLoadMixed1_P1()
            ), 'P1', duration=self.tInitLoadRamp())
        play('unit_ramp'*amp(
            self.vHome_J1()- self.vDeltaM_J1()-self.vInitPreLoadMixed1_J1()
            ), 'J1', duration=self.tInitLoadRamp())
        play('unit_ramp'*amp(
            self.vHome_P2()- self.vDeltaM_P2()-self.vInitPreLoadMixed1_P2()
            ), 'P2', duration=self.tInitLoadRamp())
        align() 

    def get_default_seq_config(self, elements: list = None) -> dict:
        """ Generates the sequence configuration dictionary """
        if elements is None:
            elements = ['P1', 'J1', 'P2']
        P1 = elements[0]
        J1 = elements[1]
        P2 = elements[2]
        config = {
            'unit_amp': {'unit': 'V', 'value': 0.5},
            'tPreControl': {'unit': 'cycles', 'value': int(4e3/4)},
            'tInitPreLoad': {'unit': 'cycles', 'value': int(1e4/4)},
            'tInitPreLoadRamp': {'unit': 'cycles', 'value': int(1e4/4)},
            'tControl': {'unit': 's', 'value': int(1*1e2/4)},
            'tInitLoadRamp': {'unit': 'cycles', 'value': int(1*1e2/4)},

            'vHome': {'unit': 'V', 'elements': {
                P1: 0.0,
                J1: 0.0,
                P2: 0.0,
            }},
            'vDeltaM': {'unit': 'cycles', 'elements': {
                P1: -0.035,
                J1: 0.0,
                P2: 0.035,
            }},
            'tPreControlRampMixed': {'unit': 'cycles', 'value': int(11e3/4)},
            'tInitLoadMixed': {'unit': 'cycles', 'value': int(2500e3/4)},
            'vInitPreLoadMixed1': {'unit': 'v', 'elements': {
                P1: 0.105,
                J1: -0.35,
                P2: -0.105,
            }},
            'vInitMixed2': {'unit': 'v', 'elements': {
                P1: 0.13,
                J1: -0.4,
                P2: -0.13,
            }}
        }
        return dict(config)