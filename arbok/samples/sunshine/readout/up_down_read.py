from qm.qua import *

from arbok.core.sample import Sample
from arbok.core.read_sequence import ReadSequence
from arbok.QMv2.Readout import Readout
from arbok.samples.sunshine.configs.rf2v_config import rf2v_config

readJ = 0

class UpDownReadout(ReadSequence):
    """
    Class containing parameters and sequence for mixed down up initialization
    Args:
        param_config (dict): Dict containing all program parameters 
    """
    def __init__(
            self, 
            name: str,
            sample = Sample('sunshine', rf2v_config),
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

        self.ref2 = Readout('ref2', self)
        self.ref2.read_label =  'SDC'
        self.read = Readout('read', self)
        self.read.read_label = 'SDC'
        self.diff = Readout('diff', self)
        self.diff.read_label = 'SDC'
        self.diff.threshold = 0.004
        self.readouts = [self.ref2, self.read, self.diff]
        #self.add_qc_read_params()
        self.add_gettables_from_readouts()

    def qua_declare(self):
        """ QUA variable declaration for mixed down up initialization """
        for readout in self.readouts:
            readout.init_qua_vars()
        
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

        self.diff.takeDiff(self.read, self.ref2)

    def get_default_seq_config(self, elements: list = None) -> dict:
        """ Generates the sequence configuration dictionary """
        if elements is None:
            elements = ['P1', 'J1', 'P2']
        P1 = elements[0]
        J1 = elements[1]
        P2 = elements[2]

        config = {
            'unit_amp': {'unit': 'V', 'value': 0.5},
            'tReadReferenceRamp': {'unit': 's', 'value': int(17)},
            'tReadRamp': {'unit': 's', 'value': int(12)},
            'tPreRead': {'unit': 's', 'value': int(0.1e3/4)},
            'tPostRead': {'unit': 's', 'value': int(0.1e3/4)},
            'tPreReadPoint': {'unit': 's', 'value': int(6)},
            'tPreReadRamp': {'unit': 's', 'value': int(17)},

            'vHome':{'unit': 'V', 'elements': {
                P1: 0.0,
                J1: 0.0,
                P2: 0.0,
            }},
            'vReference': {'unit': 'V', 'elements': {
                P1: 0.1,
                J1: 0.1,
                P2: 0.1,
            }},
            'vPreRead': {'unit': 'V', 'elements': {
                P1: 0.065,
                J1: 0,
                P2: 0.065,
            }},
            'vPreReadPoint': {'unit': 'V', 'elements': {
                P1: 0.0925,
                J1: -0.095,
                P2: -0.0925,
            }},
            'vRead': {'unit': 'V', 'elements': {
                P1: 0.0925,
                J1: -0.095,
                P2: -0.0925,
            }}
        }
        return dict(config)