import numpy as np
from qm.qua import *

from arbok.core.sequence import Sequence
from arbok.core.sample import Sample
from arbok.core.sequence_parameter import ReadParameter
from arbok.QMv2.Readout import Readout

from arbok.core.helpers.dummy_gettable_set import DummyGettableSet
from arbok.samples.sunshine.configs.rf2v_config import rf2v_config

from qcodes.parameters import ParameterWithSetpoints
from qcodes.validators import Arrays

readJ = 0

class OtherStReadout(Sequence):
    """
    Class containing parameters and sequence for mixed down up initialization
    Args:
    program_parameters (dict): Dict containing all program parameters 
    unit_amp (float): unit amplitude of all pulses
    """
    def __init__(
            self, 
            name: str,
            sample = Sample('sunshine', rf2v_config),
            param_config = {
                'elements': ['P1', 'J1', 'P2'],
                'unit_amp': {'unit': 'V', 'value': 0.5},
                'vHome':{'value': [0, 0, 0], 'unit': 'V'},
                'vReference': {'unit': 'V', 'value': [0.1, 0.1, 0.1]},
                'tReadReferenceRamp': {'unit': 's', 'value': int(17)},
                'vPreRead': {'unit': 'V', 'value': [0.065, 0, -0.065]},
                'tPreReadRamp': {'unit': 's', 'value': int(17)},
                'vPreReadPoint': {'unit': 'V', 'value': [0.0925, -0.095, -0.0925]},
                'tPreReadPoint': {'unit': 's', 'value': int(6)},
                'vRead': {'unit': 'V', 'value': [0.0925, -0.095, -0.0925]},
                'tReadRamp': {'unit': 's', 'value': int(12)},
                'tPreRead': {'unit': 's', 'value': int(0.1e3/4)},
                'tPostRead': {'unit': 's', 'value': int(0.1e3/4)},
            },
    ):
        """
        Constructor method for 'DummyReadout' class
        
        Args:
        unit_amp (float): unit amplitude of all pulses
        """
        super().__init__(name, sample)
        self.config = param_config
        self.add_qc_params_from_config(self.config)

        self.ref2 = Readout('ref2_', self)
        self.ref2.read_label =  'SDC'
        self.read = Readout('read_', self)
        self.read.read_label = 'SDC'
        self.diff = Readout('diff_', self)
        self.diff.read_label = 'SDC'
        self.diff.threshold = 0.004
        self.gettables = [self.ref2, self.read, self.diff]
        self.add_qc_read_params()

    def add_qc_read_params(self):
        for gettable in self.gettables:
                for stream in gettable.stream_list:
                        self.add_parameter(
                        name = gettable.name + stream,
                        #setpoints = (),
                        label = 'empty',
                        parameter_class = ReadParameter,
                        #vals = Arrays(shape = (1,))
                        )

    def qua_declare(self):
        for gettable in self.gettables:
            gettable.init_qua_vars()

    def qua_stream(self):
        for gettable in self.gettables:
            gettable.save_streams()
            continue
        

    def qua_sequence(self):
        """QUA sequence to perform mixed down up initialization"""

        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        play('unit_ramp_20ns'*amp(self.vReference_P1() - self.vHome_P1()),
                'P1',duration=self.tReadReferenceRamp())
        play('unit_ramp_20ns'*amp(self.vReference_J1() - self.vHome_J1()),
                'J1',duration=self.tReadReferenceRamp())
        play('unit_ramp_20ns'*amp(self.vReference_P2() - self.vHome_P2()),
                'P2',duration=self.tReadReferenceRamp())
        
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        wait(self.tPreRead(),'SDC')
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        self.ref2.measureAndSave()
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        wait(self.tPostRead(),'SDC')
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        
        play('unit_ramp_20ns'*amp(-self.vReference_P1() + self.vHome_P1()),
                'P1',duration=self.tReadReferenceRamp())
        play('unit_ramp_20ns'*amp(-self.vReference_J1() + self.vHome_J1()),
                'J1',duration=self.tReadReferenceRamp())
        play('unit_ramp_20ns'*amp(-self.vReference_P2() + self.vHome_P2()),
                'P2',duration=self.tReadReferenceRamp())
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        
        play('unit_ramp_20ns'*amp(self.vPreRead_P1() - self.vHome_P1()),'P1',
                duration = self.tPreReadRamp())
        play('unit_ramp_20ns'*amp(self.vPreRead_J1() - self.vHome_J1()),'J1',
                duration = self.tPreReadRamp())
        play('unit_ramp_20ns'*amp(self.vPreRead_P2() - self.vHome_P2()),'P2',
                duration = self.tPreReadRamp())
        
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky'
                ,'Qoff','J1_not_sticky')
        wait(self.tPreReadPoint())
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        
        play('unit_ramp_20ns'*amp(self.vRead_P1() - self.vPreRead_P1()),'P1',
                duration = self.tReadRamp())
        play('unit_ramp_20ns'*amp(self.vRead_J1() - self.vPreRead_J1()),'J1',
                duration = self.tReadRamp())
        play('unit_ramp_20ns'*amp(self.vRead_P2() - self.vPreRead_P2()),'P2',
                duration = self.tReadRamp())
                
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        wait(self.tPreRead(),'SDC')       
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        self.read.measureAndSave() 
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        wait(self.tPostRead(),'SDC')
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        
        play('unit_ramp_20ns'*amp(self.vHome_P1()-self.vRead_P1()),'P1')
        play('unit_ramp_20ns'*amp(self.vHome_J1()-self.vRead_J1()),'J1')
        play('unit_ramp_20ns'*amp(self.vHome_P2()-self.vRead_P2()),'P2')

        align()
                    
        #setVars.feedback_SSR(ref2.read,set_pt=SETFB_DCsetpt, fb_gate='SDC',
        #                      gain = SETFB_DCalpha)

        # ramp_to_zero('P1')
        # ramp_to_zero('J1')
        # ramp_to_zero('P2')
        # ramp_to_zero('J2')
        # ramp_to_zero('P3')
        self.diff.takeDiff(self.read, self.ref2)