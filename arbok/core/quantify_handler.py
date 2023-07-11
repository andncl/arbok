import warnings
from qm.qua import *
from qcodes.utils.dataset.doNd import do2d, do1d, do0d
from qcodes import (
    Instrument,
    Parameter,
    MultiParameter
)

class QuantifyHandler(Instrument):
    """
    Class describing a QUA program including (Init, Control, Read) 
    """
    def __init__(self, name: str, config: dict):
        """
        Constructor class for 'QuaProgram' class.

        Args:
            name (str): Name of the program
            config (dict): configuration for used sample
        """
        self.name = name
        self.config = config
        self.subsequences = []
        self.qua_programm = None
        self.sweep_params = {}
        self.batch_size = 1 

    def get(self):
        """Return the gettable value."""
        return np.sin(t() / np.pi)

    def prepare(self) -> None:
        """Optional methods to prepare can be left undefined."""
        print("Preparing the WaveGettable for acquisition.")

    def finish(self) -> None:
        """Optional methods to finish can be left undefined."""
        print("Finishing WaveGettable to wrap up the experiment.")

    def add_subsequence(self, new_sequence):
        """ Adds a subsequence to the entire programm. Subsequences are executed
        in order of the list 'self.subsequences' """
        self.subsequences.append(new_sequence)
        self.add_subsequence_qc_params(self, new_sequence)

    def add_subsequence_qc_params(self,new_sequence):
        for key, value in new_sequence.config:
            if isinstance(value["value"], float):
                self.add_parameter(
                    name  = key,
                    unit = value["unit"],
                    initial_value= value["value"],
                    get_cmd=None,
                    set_cmd=None,
                )
            else:
                warnings.warn("Parameter " + str(key) + " is not of type float")

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

    def get_program(self):
        """Runs the entire sequence"""
        with program() as prog:
            for sequence in self.subsequences:
                sequence.qua_declare_vars()

            with program() as prog:
                with infinite_loop_():
                    if not simulate:
                        pause()
                    if self.wait_for_trigger():
                        self.create_measurement_loop()

                with stream_processing():
                    for sequence in self.subsequences:
                            sequence.qua_streams()

    def create_measurement_loop(self):
