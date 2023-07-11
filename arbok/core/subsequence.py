from arbok.core.sample import Sample
from qcodes import (
    Instrument,
    Parameter,
    MultiParameter,
)

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.simulate.credentials import create_credentials
from qm import SimulationConfig

class SubSequence(Instrument):
    """
    Class describing a subsequence of a QUA programm (e.g Init, Control, Read). 
    """
    def __init__(self):
        self.sample = Sample()
    
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
    
    def siumulate(self):
        """Simulates the MW sequence locally or on a remote FPGA"""
        QMM = QuantumMachinesManager(
            host='dzurak-6d066ea0.quantum-machines.co',
            port=443,
            credentials=create_credentials()
        )
        job = QMM.simulate(self.sample.config, self.get_prog(),
                           SimulationConfig(duration=2500))

        samples = job.get_simulated_samples()
        samples.con1.plot()
        return