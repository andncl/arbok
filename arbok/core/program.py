from arbok.core.sequence import Sequence

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *

import copy

class Program(Sequence):
    def __init__(self, name: str, sample, param_config = {}):
        super().__init__(name, sample, param_config)

        self.qmm = None
        self.opx = None
        self.qm_job = None
        self.result_handles = None

        self.stream_mode = "pause_each"
    
    def connect_OPX(self, host_ip: str):
        self.qmm = QuantumMachinesManager(host = host_ip)
        self.opx = self.qmm.open_qm(self.sample.config)


    def run(self):
        self.qm_job = self.opx.execute(self.get_program())
        self.result_handles = self.qm_job.result_handles
        #self.qm_job.resume()

    def prepare_meas_ctrl(self, meas_ctrl):
        meas_ctrl.settables(self.settables)
        meas_ctrl.setpoints_grid(self.setpoints_grid)
        return self.settables

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
                    #if True: #not simulate: # and self.stream_mode == "pause_each":
                    pause()
                    if True or simulate: # self.wait_for_trigger()
                        self.recursive_sweep_generation(
                            copy.copy(self.settables),
                            copy.copy(self.setpoints_grid)
                            )

                with stream_processing():
                    self.recursive_qua_generation(seq_type = 'stream')
        return prog