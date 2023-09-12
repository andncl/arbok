import warnings
import copy

from qcodes.instrument import Instrument, InstrumentBase
from qcodes.validators import Arrays

from qm.qua import *
from qualang_tools.loops import from_array
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.simulate.credentials import create_credentials
from qm import SimulationConfig

from arbok.core.sequence_parameter import SequenceParameter

class Sequence(Instrument):
    """
    Class describing a subsequence of a QUA programm (e.g Init, Control, Read). 
    """
    def __init__(self, name: str, sample, param_config = {}):
        super().__init__(name = name)
        self.sample = sample
        self.elements = self.sample.elements
        self._parent = None
        self.settables = []
        self.setpoints_grid = []
        self.sweep_len = 1
        self.param_config = param_config

        self.add_qc_params_from_config(self.param_config)

    def qua_declare(self):
        """Contains raw QUA code to declare variable"""
        return

    def qua_sequence(self):
        """Contains raw QUA code to define the pulse sequence"""
        return

    def qua_stream(self):
        """Contains raw QUA code to define streams"""
        return

    def sweep_size(self) -> int:
        """ Returns the sweep size from the settables via the setpoints_grid"""
        sweep_size = 1
        for sweep_list in self.setpoints_grid:
            sweep_size *= len(sweep_list)
        return sweep_size

    @property
    def parent(self) -> InstrumentBase:
        return self._parent

    @property
    def root_instrument(self) -> InstrumentBase:
        if self._parent is None:
            return self
        return self._parent.root_instrument

    def add_subsequence(self, new_sequence):
        """
        Adds a subsequence to the entire programm. Subsequences are added as 
        QCoDeS 'Submodules'. Sequences are executed in order of them being added.

        Args:
            new_sequence (Sequence): Subsequence to be added
            verbose (bool): Flag to trigger debug printouts
            
        """
        new_sequence._parent = self
        self.add_submodule(new_sequence.name, new_sequence)

    def get_program(self, simulate = False):
        """
        Runs the entire sequence by searching recursively through init, 
        sequence and stream methods of all subsequences and their subsequences

        Args:
            simulate (bool): Flag whether program is simulated
        """
        with program() as prog:
                self.recursive_qua_generation(seq_type = 'declare')
                with infinite_loop_():
                    if not simulate: #not simulate: #not simulate:
                        pause()
                    if True or simulate: # self.wait_for_trigger()
                        self.recursive_sweep_generation(
                            copy.copy(self.settables),
                            copy.copy(self.setpoints_grid)
                            )

                with stream_processing():
                    self.recursive_qua_generation(seq_type = 'stream')
        return prog

    def recursive_sweep_generation(self, settables, setpoints_grid):
        """
        Recursively generates QUA parameter sweeps by introducing one nested QUA
        loops per swept parameter. The last given settables and its corresponding
        setpoints list is in the innermost loop.

        Args:
]           settables (list): List of QCodes parameter names to sweep
            setpoints_grid (list): List of QCodes parameter set values
            simulate (bool): Flag whether program is simulated
        """
        if len(settables) == 0:
            # this condition gets triggered if we arrive at the innermost loop
            self.recursive_qua_generation('sequence')
            return
        if len(settables) == len(self.settables):
            for i, par in enumerate(settables):
                par.batched = True
                par.vals= Arrays()
                par.set(self.setpoints_grid[i])
                self.sweep_len *= len(self.setpoints_grid[i])
                if par.get().dtype == float:
                    par.qua_var = declare(fixed)
                    globals()[par.name+'_sweep_val'] = declare(fixed)
                elif par.get().dtype == int:
                    par.qua_var = declare(int)
                    globals()[par.name+'_sweep_val'] = declare(int)
                else:
                    raise ValueError("Type not supported. Must be float or int")
    
        if len(settables) == len(setpoints_grid):
            parameter = settables[-1]
            sweep_value = globals()[parameter.name+'_sweep_val']
            with for_(*from_array(sweep_value, setpoints_grid[-1])):
                assign(parameter.qua_var, sweep_value)
                settables.pop()
                setpoints_grid.pop()
                self.recursive_sweep_generation(settables, setpoints_grid)
        else:
            raise ValueError(
                "settables and setpoints_grid must have same dimensions")

    def recursive_qua_generation(self, seq_type):
        """
        Recursively runs all QUA code stored in submodules of the given sequence

        Args:
            seq_type (str): Type of qua code containing method to look for
        """
        if not self.submodules:
            getattr(self, 'qua_' + str(seq_type))()
            return
        for seq_name, subsequence in self.submodules.items():
            if not subsequence.submodules:
                getattr(subsequence, 'qua_' + str(seq_type))()
            else:
                subsequence.recursive_qua_generation(seq_type)
           
    def add_qc_params_from_config(self, config):
        """ 
        Creates QCoDeS parameters for all entries of the config 
        
        Args:
            config (dict): Configuration containing all sequence parameters
        """
        for param_name, param_dict in config.items():
            if 'elements' in param_dict:
                for element, value in param_dict['elements'].items():
                    self.add_parameter(
                        name  = f'{param_name}_{element}',
                        unit = param_dict["unit"],
                        initial_value = value,
                        parameter_class = SequenceParameter,
                        element = element,
                        get_cmd = None,
                        set_cmd = None,
                    )
            elif 'value' in param_dict:
                self.add_parameter(
                    name  = param_name,
                    unit = param_dict["unit"],
                    initial_value = param_dict["value"],
                    parameter_class = SequenceParameter,
                    element = None,
                    set_cmd=None,
                )
            else:
                warnings.warn("Parameter " + str(param_name) +
                              " is not of type float int or list")
                      
    def run_remote_simulation(self, duration = 10000):
        """
        Simulates the MW sequence on a remote FPGA provided by Quantum Machines

        Args:
            duration (int): Amount of cycles (4ns/cycle) to simulate
        """
        QMM = QuantumMachinesManager(
            host='dzurak-6d066ea0.quantum-machines.co',
            port=443,
            credentials=create_credentials()
        )
        job = QMM.simulate(self.sample.config, self.get_program(simulate = True),
                           SimulationConfig(duration=duration))

        samples = job.get_simulated_samples()
        samples.con1.plot()
        return job
    