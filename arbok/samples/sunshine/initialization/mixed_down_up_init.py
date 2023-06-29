from arbok.core.subsequence import SubSequence
import numpy as np
from qm.qua import *

class MixedDownUpInit(SubSequence):
    """
    Class containing parameters and sequence for mixed down up initialization
    """
    def __init__(
            self, 
            unit_amp = 0.499,
            vHome = [0.0, 0.0, 0.0, 0.0],
            vDeltaM = [-0.035, -0.0, 0.035], 
            tPreControlRampMixed = int(11e3/4), 
            tInitLoadMixed = int(2e3/4), 
            vInitPreLoadMixed1 = [0.105, -0.35, -0.105],
            tInitPreLoad = int(1e4/4),
            tInitPreLoadRamp = int(1e4/4),
            tControl = int(1*1e2/4),
            tInitLoadRamp = int(1*1e2/4) ,
            vInitMixed2 = [0.13, -0.4, -0.13, 0.0],
            tPreControl = int(4e3/4)
            ):
        """
        Constructor method for 'MixedDownUpInit' class
        
        Args:
            unit_amp (float): unit amplitude of all pulses
            vDeltaM (list):
            tPreControlRampMixed (int): time in ns
            tInitLoadMixed (int): time in ns
            vInitPreLoadMixed1 (list):
            tInitPreLoad (int): time in ns
            tInitPreLoadRamp (int): time in ns
            tControl (int): time in ns
            tInitLoadRamp (int): time in ns
            vInitMixed2 (list):
            tPreControl (int): time in ns
        """
        super().__init__()
        self.unit_amp = unit_amp
        self.vHome = vHome
        self.delta = np.array(vDeltaM)/self.unit_amp
        self.tramp = tPreControlRampMixed
        self.tInitLoadMixed = tInitLoadMixed
        self.vInitPreLoadMixed1 = np.array(vInitPreLoadMixed1)/self.unit_amp
        self.tInitPreLoad = tInitPreLoad
        self.tInitPreLoadRamp = tInitPreLoadRamp
        self.tControl = tControl
        self.tInitLoadRamp = tInitLoadRamp
        self.vInitMixed2 = np.array(vInitMixed2)/self.unit_amp
        self.tPreControl = tPreControl

    def test(self):
        print(self.vHome)
        print(self.vHome[0])

    def sequence(self):
        """QUA sequence to perform mixed down up initialization"""
        align()
        play('unit_ramp'*amp(self.vInitMixed2[0] - self.vHome[0]),'P1',
            duration=self.tInitLoadRamp)
        play('unit_ramp'*amp(self.vInitMixed2[1] - self.vHome[1]),'J1',
            duration=self.tInitLoadRamp)
        play('unit_ramp'*amp(self.vInitMixed2[2] - self.vHome[2]),'P2',
            duration=self.tInitLoadRamp)
        wait(self.tInitLoadMixed,'P1','P2','J1')
    
        align()
        play('unit_ramp'*amp(self.vInitPreLoadMixed1[0] - self.vInitMixed2[0]),'P1',
            duration=self.tInitLoadRamp)
        play('unit_ramp'*amp(self.vInitPreLoadMixed1[1] - self.vInitMixed2[1]),'J1',
            duration=self.tInitLoadRamp)
        play('unit_ramp'*amp(self.vInitPreLoadMixed1[2] - self.vInitMixed2[2]),'P2',
            duration=self.tInitLoadRamp)
        wait(self.tControl,'P1','P2','J1')

        align()
        play('unit_ramp'*amp(self.delta[0]), 'P1', duration=self.tramp)
        play('unit_ramp'*amp(self.delta[1]), 'J1', duration=self.tramp)
        play('unit_ramp'*amp(self.delta[2]), 'P2', duration=self.tramp)
        # wait(tPreControl,'P1','P2','J1')

        align()  
        play('unit_ramp'*amp(self.vHome[0]- self.delta[0]-self.vInitPreLoadMixed1[0]),
            'P1', duration=self.tInitLoadRamp)
        play('unit_ramp'*amp(self.vHome[1]- self.delta[1]-self.vInitPreLoadMixed1[1]),
            'J1', duration=self.tInitLoadRamp)
        play('unit_ramp'*amp(self.vHome[2]- self.delta[2]-self.vInitPreLoadMixed1[2]),
            'P2', duration=self.tInitLoadRamp)
        align() 