import warnings
from qm.qua import *
from qcodes.utils.dataset.doNd import do2d, do1d, do0d
from qcodes import (
    Instrument,
    Parameter,
    MultiParameter,0
)

class ProgramHandler(Instrument):
    """
    Class describing a QUA program including (Init, Control, Read) 
    """
    def __init__(self, name: str, config: dict):
        """
        Constructor class for 'QuaProgram' class.

        Args:
            name (str): Name of the program
            config (dict): configuration for used sample
            init_seq (SubSequence): Class describing QUA sequence for qubit initialization
            control_seq (SubSequence): Class describing QUA sequence for qubit control
            readout_seq (SubSequence): Class describing QUA sequence for qubit readout
        """
        self.name = name
        self.config = config
        self.subsequences = []
        self.qua_programm = None
        self.last_parameter_dict = None
        self.elements = None
        self.add_parameter(
            "outer_averaging_loop",
            unit="",
            initial_value=True,
            get_cmd=None,
            set_cmd=None,
        )

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
        if self.outer_averaging_loop:


    def stream_results(self):
        if sweep_params.keys.len() == 2:
            if (
                self.acquisition_mode() == "full_integration"
                or self.acquisition_mode() == "full_demodulation"
            ):
                if self.outer_averaging_loop():
                    variables[2].buffer(self.axis1_npoints()).buffer(
                        self.axis2_npoints()
                    ).buffer(self.n_avg()).map(FUNCTIONS.average()).save_all("I")
                    variables[3].buffer(self.axis1_npoints()).buffer(
                        self.axis2_npoints()
                    ).buffer(self.n_avg()).map(FUNCTIONS.average()).save_all("Q")
                else:
                    variables[2].buffer(self.axis1_npoints()).buffer(self.n_avg()).map(
                        FUNCTIONS.average()
                    ).buffer(self.axis2_npoints()).save_all("I")
                    variables[3].buffer(self.axis1_npoints()).buffer(self.n_avg()).map(
                        FUNCTIONS.average()
                    ).buffer(self.axis2_npoints()).save_all("Q")
            else:
                raise Exception(
                    "It is advises to use 'full_integration' or 'full_demodulation' only for performing 2d scans on the OPX to avoid memory overflow."
                )

    def do2d(
        self,
        sweep_params = {},
        show_progress = True,
        do_plot = True,
        exp = experiment,
        ):
        """Function wrapper for QCoDeS 'do2d'"""

        if isinstance(my_dict, dict):
            if sweep_params.keys.len() == 2:
                axis_1 = sweep_params.values[0],
                axis_2 = sweep_params.values[1],
                axis_1_setpoints = np.linspace(axis_1['start'], axis_1['stop'], axis_1['step'])
                axis_2_setpoints = np.linspace(axis_2['start'], axis_2['stop'], axis_2['step'])
                opx_instrument.set_sweep_parameters(sweep_params.items[0], axis_1_setpoints, "V", sweep_params.items[0])
                opx_instrument.set_sweep_parameters(sweep_params.items[1], axis_2_setpoints, "V", sweep_params.items[1])
                opx_instrument.get_prog = self.get_prog

                do2d(
                param_set1 = axis_1,
                start1 = sweep_params.values[0]['start'],
                stop1 = sweep_params.values[0]['stop'],
                num_points = sweep_params.values[0]['n_points'],
                delay1 = sweep_params.values[0]['delay'],
                param_set2 = sweep_params.keys[1],
                start2 = sweep_params.values[1]['start'],
                stop2 = sweep_params.values[1]['stop'],
                num_points2 = sweep_params.values[1]['n_points'],
                delay2 = sweep_params.values[1]['delay'],
                enter_actions = opx_instrument.resume,
                param_meas = opx_instrument.get_measurement_parameter(),
                enter_actions = [opx_instrument.run_exp],
                exit_actions = [opx_instrument.halt],
                show_progress = True,
                do_plot = True,
                exp = experiment,
                )
            else:
                print("'sweep_param' dict does not have length 2, has length: ")
        else:
            print("'sweep_param' should be a dict, is: ")

    


