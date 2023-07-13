from arbok.core.sample import Sample
from qcodes import (
    Instrument,
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
        self.elements = []
        self.subsequences = []
        self.param_config = param_config
        self.add_qc_params_from_config(self.param_config)
    
    def qua_declare_vars(self):
        """Contains raw QUA code to declare variable"""
        return
    
    def qua_sequence(self, cls = None, simulate = False):
        """Contains raw QUA code to define the pulse sequence"""
        return
    
    def qua_streams(self):
        """Contains raw QUA code to define streams"""
        return

    def add_qc_params_from_config(self, config, verbose = True):
        for key, value in config.items():
            if key == 'elements':
                self.elements = value
                if verbose: print("Added elements: " + str(self.elements))
                continue
            if key in self.parameters.keys():
                if verbose: print("Existing paramter  \"" + key + "\" SKIPPED")
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
                
    def add_subsequence(self, new_sequence, verbose = False):
        """
        Adds a subsequence to the entire programm. Subsequences are executed
        in order of the list 'self.subsequences'
        """
        self.subsequences.append(new_sequence)
        self.add_subsequence_qc_params(new_sequence, verbose = verbose)

    def add_subsequence_qc_params(self, new_sequence, verbose = False):
        for name, par in new_sequence.parameters.items():
            if name not in self.parameters.keys():
                print(par())
                print(name)
                self.add_parameter(
                    name = name,
                    unit = par.unit,
                    intial_value = par(),
                    set_cmd = par.set_raw,
                    get_cmd = par.get_raw,
                )
                #setattr(self, name, par
                if verbose: print("Added " + name + " successfully!!" + str(par())) 
            else:
                if verbose: print("Existing paramter \"" + name + "\" SKIPPED")

    def get_program(self, simulate = False):
        """Runs the entire sequence wrapped as a QUA program"""
        with program() as prog:
            self.qua_sequence(simulate = simulate)
        return prog
    
    def run_remote_simulation(self, duration = 10000):
        """Simulates the MW sequence locally or on a remote FPGA"""
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