from arbok.core.sample import Sample
from qcodes import (
    Instrument,
)

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.simulate.credentials import create_credentials
from qm import SimulationConfig

import warnings

class SubSequence(Instrument):
    """
    Class describing a subsequence of a QUA programm (e.g Init, Control, Read). 
    """
    def __init__(self, name: str):
        super().__init__(name = name)
        self.sample = Sample()
        self.elements = []
    
    def qua_declare_vars(self):
        """Contains QUA code to declare variable"""
        return
    
    def qua_sequence(self):
        """Contains QUA code to define the pulse sequence"""
        return
    
    def qua_streams(self):
        """Contains QUA code to define streams"""
        return
    
    def init_qc_params(self):
        """Instanciates QCoDeS parameters from subsequence config"""
        return

    def add_qc_params_from_config(self, config, verbose = True):
        for key, value in config.items():
            if key == 'elements':
                self.elements = value
                if verbose: print("Added elements: " + str(self.elements))
                continue
            if key in self.parameters.keys():
                if verbose: print("Duplicate paramter \"" + key + "\" skipped")
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
                    self.add_parameter(
                        name  = par_name,
                        unit = value["unit"],
                        initial_value= item,
                        get_cmd=None,
                        set_cmd=None,
                    )
                    if verbose: print("Added " + getattr(self, par_name).name
                          + " successfully!") 
            else:
                warnings.warn("Parameter " + str(key) + 
                              " is not of type float int or list")
    def get_program(self):
        """Runs the entire sequence"""
        with program() as prog:
            pass
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