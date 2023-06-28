from PulseLibrary import initMixed
from qm.qua import *

class MeasurementBlueprint():
    """
    Blueprint to construct OPX sequences consising of initialization,
    control and readout.
    """
    def __init__(self):
        self.vHome1 = float(0)
        self.vHome2 = float(1)
        self.vHome3 = float(2)
        self.vHome4 = float(3)
        self.fESR = 10e6

    def run_sequence(self):
        """
        Constructs OPX seq. from its subparts init, control and readout.
        """
        with program() as prog:
            self.reset_device()
            self.run_init()
            self.run_control()
            self.run_readout()
        return prog

    def reset_device(self):
        reset_phase('Q1')
        reset_frame('Q1')
        align()
        update_frequency('Q1',self.fESR)
        align()
        goHome([self.vHome1,self.vHome2,self.vHome3,self.vHome4])
        align()

    def run_init(self):
        initMixed(
            delta = [self.vDeltaM1,self.vDeltaM2,self.vDeltaM3],
            tramp = self.tPreControlRampMixed,
            tInitLoadMixed=self.tInitLoadMixed,
            vInitPreLoadMixed1 = [
                self.vInitPreLoadMixed11,
                self.vInitPreLoadMixed12,
                self.vInitPreLoadMixed13
                ],
            tInitPreLoad=tInitPreLoad,
            tInitPreLoadRamp=self.tInitPreLoadRamp,
            tControl=self.tControl,
            tInitLoadRamp=self.tInitLoadRamp,
            vInitMixed2=[
                self.vInitMixed21,
                self.vInitMixed22,
                self.vInitMixed23
                ],
            tPreControl=self.tPreControl,
            vHome0=[self.vHome1,self.vHome2,self.vHome3,self.vHome4],
            vLoadMixed1=[
                self.vLoadMixed11,
                self.vLoadMixed12,
                self.vLoadMixed13
                ]
        )
    def run_control():
        pass
        
    def run_readout():
        pass