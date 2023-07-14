from arbok.core.sample import Sample
from qcodes.instrument import (
    Instrument,
    InstrumentBase
)

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.simulate.credentials import create_credentials
from qm import SimulationConfig

import warnings

class Sequence(Instrument):
    """
    Class describing a subsequence of a QUA programm (e.g Init, Control, Read). 
    """
    def __init__(self, name: str, param_config = {}, sample = Sample()):
        super().__init__(name = name)
        self.sample = sample
        self._parent = None
        self.elements = []
        self.subsequences = []
        self.param_config = param_config
        self.add_qc_params_from_config(self.param_config)
    
    def qua_declare_vars(self, simulate = False):
        """Contains raw QUA code to declare variable"""
        return
    
    def qua_sequence(self, cls = None, simulate = False):
        """Contains raw QUA code to define the pulse sequence"""
        return
    
    def qua_streams(self, simulate = False):
        """Contains raw QUA code to define streams"""
        return

    @property
    def parent(self) -> InstrumentBase:
        return self._parent
    
    @property
    def root_instrument(self) -> InstrumentBase:
        if not self._parent:
            return self
        else:
            return self._parent.root_instrument
    
    def add_subsequence(self, new_sequence, verbose = False):
        """
        Adds a subsequence to the entire programm. Subsequences are added as 
        QCoDeS 'Submodules'. Sequences are executed in order of them being added.

        Args:
            new_sequence (Sequence): Subsequence to be added
            verbose (bool): Flag to trigger debug printouts
            
        """
        #sub_sequence = SubSequence()
        new_sequence._parent = self
        self.add_submodule(new_sequence.name, new_sequence)

    def get_program(self, simulate = False):
        """
        Runs the entire sequence by searching recursively through init, 
        sequence and stream methods of all subsequences and their subsequences

        Args:
            simulate (bool): Whether program is simulated
        """
        with program() as prog:
                self.recursive_qua_generation(seq_type = 'declare_vars',
                                                simulate = simulate)

                with infinite_loop_():
                    if not simulate:
                        pause()
                    if True or simulate: # self.wait_for_trigger()
                        self.recursive_qua_generation(seq_type = 'sequence',
                                                    simulate = simulate)

                with stream_processing():
                    self.recursive_qua_generation(seq_type = 'declare_vars',
                                                    simulate = simulate)
        return prog
    
    def recursive_qua_generation(self, seq_type = 'sequence', simulate = False):
        """
        Recursively runs all QUA code stored in submodules of the given sequence

        Args:
            seq_type (str): Type of qua code containing method to look for
            simulate (bool): Whether sequence is simulated
        """
        if not self.submodules:
            getattr(self, 'qua_' + str(seq_type))(simulate=simulate)
            return
        for seq_name, subsequence in self.submodules.items():
            if not subsequence.submodules:
                getattr(subsequence, 'qua_' + str(seq_type))(simulate=simulate)
            else:
                subsequence.recursive_qua_generation(seq_type, simulate)
    
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
                if verbose: print("Added elements: " + str(self.elements))
                continue
            if isinstance(value["value"], float) or isinstance(value["value"], int):
                self.add_parameter(
                    name  = key,
                    unit = value["unit"],
                    initial_value= value["value"],
                    get_cmd=None,
                    set_cmd=None,
                )
                if verbose: print("Added " + getattr(self, key).name + " successfully!") 

            elif isinstance(value["value"], list):
                for i, item in enumerate(value["value"]):
                    par_name = key + '_' + self.elements[i]
                    if par_name in self.parameters.keys():
                        if verbose: print("Duplicate paramter \"" + par_name + "\" skipped")
                        continue
                    init_val = item/self.unit_amp() if value["unit"].lower() == 'v' else item
                    self.add_parameter(
                        name  = par_name,
                        unit = value["unit"],
                        initial_value = init_val,
                        get_cmd=None,
                        set_cmd=None,
                    )
                    if verbose: print("Added " + getattr(self, par_name).name
                          + " successfully!") 
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
        return
    