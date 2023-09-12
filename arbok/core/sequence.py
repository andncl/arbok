import site
from arbok.core.sample import Sample
from arbok.core.sequence_parameter import SequenceParameter
from qcodes.instrument import (
    Instrument,
    InstrumentBase
)
from qcodes.validators import Arrays

from qm.qua import *
from qualang_tools.loops import from_array
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.simulate.credentials import create_credentials
from qm import SimulationConfig

import warnings
import copy

class Sequence(Instrument):
    """
    Class describing a subsequence of a QUA programm (e.g Init, Control, Read). 
    """
    def __init__(self, name: str, sample, param_config = {}):
        super().__init__(name = name)
        self.sample = sample
        self._parent = None
        self.settables = []
        self.setpoints_grid = []
        self.sweep_len = 1
        self.param_config = param_config

        self.add_qc_params_from_config(self.param_config)
        self.elements = self.sample.config['elements'].keys()
    
    def qua_declare(self):
        """Contains raw QUA code to declare variable"""
        return
    
    def qua_sequence(self):
        """Contains raw QUA code to define the pulse sequence"""
        returns
    
    def qua_stream(self):
        """Contains raw QUA code to define streams"""
        return
    
    def sweep_size(self) -> int:
        """ Returns the sweep size from the settables via the setpoints_grid"""
        sweep_size = 1
        for sweep_list in self.setpoints_grid:
            sweep_size *= len(sweep_list)
        return sweep_size

    def sweep_size(self):
        sweep_dim = 1
        for sweep_list in self.setpoints_grid:
            sweep_dim *= len(sweep_list)
        return sweep_dim
    
    @property
    def parent(self) -> InstrumentBase:
        return self._parent
    
    @property
    def root_instrument(self) -> InstrumentBase:
        if not self._parent:
            return self
        else:
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
            #for par in self.settables: par.batched = False
            return
        elif len(settables) == len(self.settables):
            for i, par in enumerate(settables):
                par.batched = True
                #par.vals = Arrays(shape= np.shape(self.setpoints_grid[i] ))
                par.vals= Arrays()
                par.set(self.setpoints_grid[i])
                self.sweep_len *= len(self.setpoints_grid[i])
                if par.get().dtype == float:#
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

    def recursive_qua_generation(self, seq_type = 'sequence'):
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
    
    def add_qc_params_from_config(self, config, verbose = False):
        """ 
        Creates QCoDeS parameters for all entries of the config 
        
        Args:
            config (dict): Configuration containing all sequence parameters
            verbose (bool): Flag to trigger debug printouts
        """
        for key, value in config.items():
            if key == 'elements':
                self.elements = value
                if verbose:
                    print(f'Added elements: {str(self.elements)}')
                continue
            if isinstance(value["value"], float) or isinstance(value["value"], int):
                self.add_parameter(
                    name  = key,
                    unit = value["unit"],
                    initial_value = value["value"],
                    parameter_class = SequenceParameter,
                    elements = ['Q1'],
                    get_cmd = None,
                    set_cmd=None,
                )
                if verbose: 
                    print(f'Added {getattr(self, key).name} successfully!') 

            elif isinstance(value["value"], list):
                for i, item in enumerate(value["value"]):
                    par_name = f'{key}_{self.elements[i]}'
                    if par_name in self.parameters:
                        if verbose: 
                            print("Duplicate paramter \"" + par_name + "\" skipped")
                        continue
                    init_val = item/self.unit_amp() if value["unit"].lower() == 'v' else item
                    self.add_parameter(
                        name  = par_name,
                        unit = value["unit"],
                        initial_value = init_val,
                        parameter_class = SequenceParameter,
                        elements = ['Q1'],
                        set_cmd=None,
                    )
                    if verbose:
                        print(f'Added {getattr(self, par_name).name} successfully!')
            else:
                warnings.warn("Parameter " + str(key) + 
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
    