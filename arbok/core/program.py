from arbok.core.sequence import Sequence
from qm.QuantumMachinesManager import QuantumMachinesManager

class Program(Sequence):
    def __init__(self, name: str, sample, param_config=...):
        super().__init__(name, sample, param_config)

        self.opx = None
        self.job = None

    def run(self):
        return
    
    def connect_OPX(self, host_ip: str, name):
        QMm = QuantumMachinesManager(host = host_ip, cluster_name = name)
        Qm1 = QMm.open_qm(self.sample.config)