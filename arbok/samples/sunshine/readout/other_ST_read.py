from arbok.core.subsequence import SubSequence
from arbok.QMv2.Readout import Readout
import numpy as np
from qm.qua import *

class DummyReadout(SubSequence):
    """
    Class containing parameters and sequence for mixed down up initialization
        Args:
            program_parameters (dict): Dict containing all program parameters 
            unit_amp (float): unit amplitude of all pulses
    """
    def __init__(
        self, 
        program_parameters = {
            'unit_amp': {'value': 0.499, 'unit': 'V'},
            'vHome':{
                'value': [0, 0, 0], 'elements': ['P1', 'J1', 'P2'], 'unit': 'V'
            }
        },
        unit_amp = 0.499,
        vHome = [0, 0, 0],
        vReference = [ (0.00)/self.unit_amp ,0.0/self.unit_amp,
                                (-0.00)/self.unit_amp],
        tReadReferenceRamp = int(17),
        vPreRead = [(0.065)/self.unit_amp,(readJ),(-0.065)/self.unit_amp],
        vRead = [(0.0925)/self.unit_amp,(readJ),(-0.0925)/self.unit_amp],
        tPreRead = int(0.1e3/4),
        tPostRead = int(0.1e3/4),
    ):
        """ Constructor method for 'DummyReadout' class
        
        Args:
            unit_amp (float): unit amplitude of all pulses
        """
        super().__init__()
        self.program_parameters = program_parameters
        self.unit_amp = unit_amp
        self.vHome = vHome
        self.vReference = vReference
        self.tReferenceRamp = tReadReferenceRamp
        self.vPreRead = vPreRead
        self.tPreRead = tPreRead
        self.tPostRead = tPostRead
    
        ref2 = Readout('ref2_')
        ref2.read_label =  'SDC'
        read = Readout('read_')
        read.read_label = 'SDC'
        diff = Readout('diff_')
        diff.read_label = 'SDC'
        diff.threshold = 0.004

    def create_qc_params_from_program_dict(self):
        pass

    def declare(self):
        ref2.dec    
    def sequence(self):
        """QUA sequence to perform mixed down up initialization"""
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
              'Qoff','J1_not_sticky')
        play('unit_ramp_20ns'*amp(self.vReference[0] - self.vHome[0]),
             'P1',duration=self.tReadReferenceRamp)
        play('unit_ramp_20ns'*amp(self.vReference[1] - self.vHome[1]),
             'J1',duration=self.tReadReferenceRamp)
        play('unit_ramp_20ns'*amp(self.vReference[2] - self.vHome[2]),
             'P2',duration=self.tReadReferenceRamp)
           
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
              'Qoff','J1_not_sticky')
        wait(self.tPreRead,'SDC')
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
              'Qoff','J1_not_sticky')
        ref2.measureAndSave()
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
              'Qoff','J1_not_sticky')
        wait(self.tPostRead,'SDC')
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
              'Qoff','J1_not_sticky')
         
        play('unit_ramp_20ns'*amp(-self.vReference[0] + self.vHome[0]),
             GA,duration=self.tReadReferenceRamp)
        play('unit_ramp_20ns'*amp(-self.vReference[1] + self.vHome[1]),
             GC,duration=self.tReadReferenceRamp)
        play('unit_ramp_20ns'*amp(-self.vReference[2] + self.vHome[2]),
             GB,duration=self.tReadReferenceRamp)
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
              'Qoff','J1_not_sticky')
            
        play('unit_ramp_20ns'*amp(self.vPreRead[0] - self.vHome[0]),'P1',
             duration = self.tPreReadRamp)
        play('unit_ramp_20ns'*amp(self.vPreRead[1] - self.vHome[1]),'J1',
             duration = self.tPreReadRamp)
        play('unit_ramp_20ns'*amp(self.vPreRead[2] - self.vHome[2]),'P2',
             duration = self.tPreReadRamp)
           
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky'
              ,'Qoff','J1_not_sticky')
        wait(self.tPreReadPoint)
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
              'Qoff','J1_not_sticky')
           
        play('unit_ramp_20ns'*amp(self.vRead[0] - self.vPreRead[0]),'P1',
             duration = self.tReadRamp)
        play('unit_ramp_20ns'*amp(self.vRead[1] - self.vPreRead[1]),'J1',
             duration = self.tReadRamp)
        play('unit_ramp_20ns'*amp(self.vRead[2] - self.vPreRead[2]),'P2',
             duration = self.tReadRamp)
                  
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
              'Qoff','J1_not_sticky')
        wait(self.tPreRead,'SDC')       
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
              'Qoff','J1_not_sticky')
        read.measureAndSave() 
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
              'Qoff','J1_not_sticky')
        wait(self.tPostRead,'SDC')
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
              'Qoff','J1_not_sticky')
         
        play('unit_ramp_20ns'*amp(self.vHome[0]-self.vRead[0]),'P1')
        play('unit_ramp_20ns'*amp(self.vHome[1]-self.vRead[1]),'J1')
        play('unit_ramp_20ns'*amp(self.vHome[2]-self.vRead[2]),'P2')

        align()
                     
        #setVars.feedback_SSR(ref2.read,set_pt=SETFB_DCsetpt, fb_gate='SDC',
        #                      gain = SETFB_DCalpha)

        resetChannels()
        diff.takeDiff(read, ref2)