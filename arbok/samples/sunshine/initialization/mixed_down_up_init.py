from arbok.core.sequence import Sequence
import numpy as np
from qm.qua import *
from quantify_core.measurement.control import MeasurementControl

class MixedDownUpInit(Sequence):
    """
    Class containing parameters and sequence for mixed down up initialization
    """
    def __init__(
            self, 
            name = 'MixedDuInit',
            config = {
                'elements': ['P1', 'J1', 'P2'],
                'unit_amp': {'unit': 'V', 'value': 0.5},
                'tPreControl': {'unit': 's', 'value': int(4e3/4)},
                'vHome': {'unit': 'v', 'value': [0.0, 0.0, 0.0]},
                'vDeltaM': {'unit': 's', 'value': [-0.035, -0.0, 0.035]},
                'tPreControlRampMixed': {'unit': 's', 'value': int(11e3/4)},
                'tInitLoadMixed': {'unit': 's', 'value': int(2500e3/4)},
                'vInitPreLoadMixed1': {'unit': 'v', 'value': [0.105, -0.35, -0.105]},
                'tInitPreLoad': {'unit': 's', 'value': int(1e4/4)},
                'tInitPreLoadRamp': {'unit': 's', 'value': int(1e4/4)},
                'tControl': {'unit': 's', 'value': int(1*1e2/4)},
                'tInitLoadRamp': {'unit': 's', 'value': int(1*1e2/4)},
                'vInitMixed2': {'unit': 'v', 'value': [0.13, -0.4, -0.13]},
                'tPreControl': {'unit': 's', 'value': int(40e3/4)},
            },
    ):
        """
        Constructor method for 'MixedDownUpInit' class
        
        Args:
            name (str): name of sequence
            config (dict): config containing pulse parameters
        """
        super().__init__(name = name)
        self.config = config
        self.add_qc_params_from_config(self.config)

    def qua_sequence(self, cls = None, simulate = False):
        """QUA sequence to perform mixed down up initialization"""
        if cls == None: cls = self
        align()
        play('unit_ramp'*amp(cls.vInitMixed2_P1() - cls.vHome_P1()),'P1',
            duration=cls.tInitLoadRamp())
        play('unit_ramp'*amp(cls.vInitMixed2_J1() - cls.vHome_J1()),'J1',
            duration=cls.tInitLoadRamp())
        play('unit_ramp'*amp(cls.vInitMixed2_P2() - cls.vHome_P2()),'P2',
            duration=cls.tInitLoadRamp())
        wait(cls.tInitLoadMixed(),'P1','P2','J1')
    
        align()
        play('unit_ramp'*amp(cls.vInitPreLoadMixed1_P1() - cls.vInitMixed2_P1()),
             'P1', duration=cls.tInitLoadRamp())
        play('unit_ramp'*amp(cls.vInitPreLoadMixed1_J1() - cls.vInitMixed2_J1()),
             'J1', duration=cls.tInitLoadRamp())
        play('unit_ramp'*amp(cls.vInitPreLoadMixed1_P2() - cls.vInitMixed2_P2()),
             'P2', duration=cls.tInitLoadRamp())
        wait(cls.tControl(),'P1','P2','J1')

        align()
        play('unit_ramp'*amp(cls.vDeltaM_P1()), 'P1',
             duration=cls.tPreControlRampMixed())
        play('unit_ramp'*amp(cls.vDeltaM_J1()), 'J1',
             duration=cls.tPreControlRampMixed())
        play('unit_ramp'*amp(cls.vDeltaM_P2()), 'P2',
             duration=cls.tPreControlRampMixed())
        wait(cls.tPreControl(),'P1','P2','J1')

        align()  
        play('unit_ramp'*amp(
            cls.vHome_P1()- cls.vDeltaM_P1()-cls.vInitPreLoadMixed1_P1()
            ), 'P1', duration=cls.tInitLoadRamp())
        play('unit_ramp'*amp(
            cls.vHome_J1()- cls.vDeltaM_J1()-cls.vInitPreLoadMixed1_J1()
            ), 'J1', duration=cls.tInitLoadRamp())
        play('unit_ramp'*amp(
            cls.vHome_P2()- cls.vDeltaM_P2()-cls.vInitPreLoadMixed1_P2()
            ), 'P2', duration=cls.tInitLoadRamp())
        align() 

    def qua_declare_vars(self):
        return
    
    def qua_streams(self):
        return