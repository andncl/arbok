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
            config = {
                'elements': ['P1', 'J1', 'P2'],
                'unit_amp': {'unit': 'V', 'value': 0.5},
                'tPreControl': {'unit': 'cycles', 'value': int(4e3/4)},
                'vHome': {'unit': 'v', 'value': [0.0, 0.0, 0.0]},
                'vDeltaM': {'unit': 'cycles', 'value': [-0.035, -0.0, 0.035]},
                'tPreControlRampMixed': {'unit': 'cycles', 'value': int(11e3/4)},
                'tInitLoadMixed': {'unit': 'cycles', 'value': int(2500e3/4)},
                'vInitPreLoadMixed1': {'unit': 'v', 'value': [0.105, -0.35, -0.105]},
                'tInitPreLoad': {'unit': 'cycles', 'value': int(1e4/4)},
                'tInitPreLoadRamp': {'unit': 'cycles', 'value': int(1e4/4)},
                'tControl': {'unit': 's', 'value': int(1*1e2/4)},
                'tInitLoadRamp': {'unit': 'cycles', 'value': int(1*1e2/4)},
                'vInitMixed2': {'unit': 'v', 'value': [0.13, -0.4, -0.13]},
            },
    ):
        """
        Constructor method for 'MixedDownUpInit' class
        
        Args:
            name (str): name of sequence
            config (dict): config containing pulse parameters
        """
        super().__init__(name, sample)
        self.config = config
        self.add_qc_params_from_config(self.config)

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
