import warnings
from qm.qua import *
from qcodes.utils.dataset.doNd import do2d, do1d, do0d

from qualang_tools.external_frameworks.qcodes.opx_driver import OPX
from qm.QuantumMachinesManager import QuantumMachinesManager

from arbok.core.sequence import Sequence
from arbok.core.sample import Sample

class QuantifyHandler(Sequence):
    """
    Class describing a QUA program including (Init, Control, Read) 
    """
    def __init__(self, name: str, sample: Sample):
        """
        Constructor class for 'QuaProgram' class.

        Args:
            name (str): Name of the program
            config (dict): configuration for used sample
        """
        super().__init__(name = name)
        self.sample = sample
        self.param_config = {'unit_amp': {'unit': 'V', 'value': 0.5}}
        self.gettables = []
        self.sweep_params = {}
        self.batch_size = 1 

        self.Qm1 = None
        self.job = None
        self.result_handles = None

    def prepare(self) -> None:
        """Optional methods to prepare can be left undefined."""
        print("Preparing the WaveGettable for acquisition.")

        self.QmJob = self.get_QM().execute(self.get_program())
        self.result_handles = self.QmJob.result_handles

        self.start_opx_if_not_running()
        self.wait_for_buffer()

    def get_result(self, name):
        """Return the gettable value with a certain name"""
        if getattr(self.result_handles, name):
            wait_for_values(name)
            getattr(self.result_handles, name)
            return name
        else:
            NameError(str(name) + "is not ")
        
    def prepare_quantify_measurement(self, meas_ctrl):
        """Sets the batch_size correctly and adds the gettables as specified in 
        the respective subsequences"""
        self.batch_size = 1
        for i, par in enumerate(meas_ctrl._settable_pars):
            getattr(par).batched = True
            self.batch_size *= len(meas_ctrl._setpoints_input[i])
        
        for par in meas_ctrl._gettable_pars:
            getattr(par).batched = True

        for par in self.gettables:
            meas_ctrl.gettables(par)
            getattr(par.name).batch_size = self.batch_size

    def get_program(self, simulate = False):
        """Runs the entire sequence"""
        with program() as prog:
            for sequence in self.subsequences:
                sequence.qua_declare_vars()

            with infinite_loop_():
                if not simulate:
                    pause()
                if True: #self.wait_for_trigger():
                    self.create_measurement_loop(simulate)

            with stream_processing():
                for sequence in self.subsequences:
                        sequence.qua_streams()
        return prog
    
    def create_measurement_loop(self, simulate = False):
        for sequence in self.subsequences:
            sequence.qua_sequence(cls = self, simulate = simulate)

    def get_QM(self):
        QMm = QuantumMachinesManager(store=MyStore(self.dictator, __file__))
        self.Qm1 = QMm.open_qm(config)

    def set_QMprog(self):
        self.Qm1.execute(self.program())