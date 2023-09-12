from arbok.core.sequence import Sequence
from qm.QuantumMachinesManager import QuantumMachinesManager

class Program(Sequence):
    def __init__(self, name: str, sample, param_config = {}):
        super().__init__(name, sample, param_config)

        self.qmm = None
        self.opx = None
        self.qm_job = None
        self.result_handles = None

    def run(self):
        return
    
    def connect_OPX(self, host_ip: str):
        self.qmm = QuantumMachinesManager(host = host_ip)
        self.opx = self.qmm.open_qm(self.sample.config)


    def run(self):
        self.qm_job = self.opx.execute(self.get_program())
        self.result_handles = self.qm_job.result_handles
        self.qm_job.resume()

    def prepare_meas_ctrl(self, meas_ctrl):
        meas_ctrl.settables(self.settables)
        meas_ctrl.setpoints_grid(self.setpoints_grid)
        return self.settables
