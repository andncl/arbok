from arbok.core.subsequence import SubSequence
from arbok.QMv2.Readout import Readout
import numpy as np
from qm.qua import *

readJ = 0

class OtherStReadout():
    """
    Class containing parameters and sequence for mixed down up initialization
    Args:
    program_parameters (dict): Dict containing all program parameters 
    unit_amp (float): unit amplitude of all pulses
    """
    def __init__(
        self, 
        # program_parameters = {
        # 'unit_amp': {'value': 0.499, 'unit': 'V'},
        # 'vHome':{
        #         'value': [0, 0, 0], 'elements': ['P1', 'J1', 'P2'], 'unit': 'V'
        # }
        # },
        unit_amp = 0.499,
        vHome = [0, 0, 0],
        vReference = [0.0, 0.0, -0.0],
        tReadReferenceRamp = int(17),
        vPreRead = [0.065, readJ, -0.065],
        tPreReadRamp = int(17),
        vPreReadPoint = [0.0925, readJ, -0.0925],
        tPreReadPoint = int(6),
        vRead = [0.0925, readJ, -0.0925],
        tReadRamp = int(12),
        tPreRead = int(0.1e3/4),
        tPostRead = int(0.1e3/4),
    ):
      """
      Constructor method for 'DummyReadout' class
      
      Args:
      unit_amp (float): unit amplitude of all pulses
      """
      #self.program_parameters = program_parameters
      self.unit_amp = unit_amp
      self.vHome = vHome
      self.vReference = [x/self.unit_amp for x in vReference]
      self.tReadReferenceRamp = tReadReferenceRamp
      self.vPreRead = vPreRead 
      self.tPreReadRamp = tPreReadRamp
      self.vPreReadPoint = [x/self.unit_amp for x in vPreReadPoint]
      self.tPreReadPoint = tPreReadPoint
      self.vRead = [x/self.unit_amp for x in vRead]
      self.tReadRamp = tReadRamp
      self.tPreRead = tPreRead
      self.tPostRead = tPostRead

      self.ref2 = Readout('ref2_')
      self.ref2.read_label =  'SDC'
      self.read = Readout('read_')
      self.read.read_label = 'SDC'
      self.diff = Readout('diff_')
      self.diff.read_label = 'SDC'
      self.diff.threshold = 0.004
      self.gettables = [self.ref2, self.read, self.diff]


    def create_qc_params_from_program_dict(self):
        pass

    def qua_declare(self):
        for gettable in self.gettables:
            gettable.init_qua_vars()

    def qua_stream(self):
        for gettable in self.gettables:
            gettable.init_qua_vars()

    def qua_sequence(self, cls = None):
        """QUA sequence to perform mixed down up initialization"""
        if cls == None:
                cls = self
        print(cls)
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        play('unit_ramp_20ns'*amp(cls.vReference[0] - cls.vHome[0]),
                'P1',duration=cls.tReadReferenceRamp)
        play('unit_ramp_20ns'*amp(cls.vReference[1] - cls.vHome[1]),
                'J1',duration=cls.tReadReferenceRamp)
        play('unit_ramp_20ns'*amp(cls.vReference[2] - cls.vHome[2]),
                'P2',duration=cls.tReadReferenceRamp)
        
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        wait(cls.tPreRead,'SDC')
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        #cls.ref2.measureAndSave()
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        wait(cls.tPostRead,'SDC')
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        
        play('unit_ramp_20ns'*amp(-cls.vReference[0] + cls.vHome[0]),
                'P1',duration=cls.tReadReferenceRamp)
        play('unit_ramp_20ns'*amp(-cls.vReference[1] + cls.vHome[1]),
                'J1',duration=cls.tReadReferenceRamp)
        play('unit_ramp_20ns'*amp(-cls.vReference[2] + cls.vHome[2]),
                'P2',duration=cls.tReadReferenceRamp)
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        
        play('unit_ramp_20ns'*amp(cls.vPreRead[0] - cls.vHome[0]),'P1',
                duration = cls.tPreReadRamp)
        play('unit_ramp_20ns'*amp(cls.vPreRead[1] - cls.vHome[1]),'J1',
                duration = cls.tPreReadRamp)
        play('unit_ramp_20ns'*amp(cls.vPreRead[2] - cls.vHome[2]),'P2',
                duration = cls.tPreReadRamp)
        
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky'
                ,'Qoff','J1_not_sticky')
        wait(cls.tPreReadPoint)
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        
        play('unit_ramp_20ns'*amp(cls.vRead[0] - cls.vPreRead[0]),'P1',
                duration = cls.tReadRamp)
        play('unit_ramp_20ns'*amp(cls.vRead[1] - cls.vPreRead[1]),'J1',
                duration = cls.tReadRamp)
        play('unit_ramp_20ns'*amp(cls.vRead[2] - cls.vPreRead[2]),'P2',
                duration = cls.tReadRamp)
                
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        wait(cls.tPreRead,'SDC')       
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        #self.read.measureAndSave() 
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        wait(cls.tPostRead,'SDC')
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        
        play('unit_ramp_20ns'*amp(cls.vHome[0]-cls.vRead[0]),'P1')
        play('unit_ramp_20ns'*amp(cls.vHome[1]-cls.vRead[1]),'J1')
        play('unit_ramp_20ns'*amp(cls.vHome[2]-self.vRead[2]),'P2')

        align()
                    
        #setVars.feedback_SSR(ref2.read,set_pt=SETFB_DCsetpt, fb_gate='SDC',
        #                      gain = SETFB_DCalpha)

        ramp_to_zero('P1')
        ramp_to_zero('J1')
        ramp_to_zero('P2')
        ramp_to_zero('J2')
        ramp_to_zero('P3')
        #self.diff.takeDiff(self.read, self.ref2)