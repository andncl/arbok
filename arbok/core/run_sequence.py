from arbok.core.sequence import Sequence
from qm.qua import *

class RunSequence(Sequence):
    def __init__(self, name: str, sample):
        super().__init__(name = name, sample = sample)
        self.gettables = []
        self.settables = []
        self.setpoints = []

        self.QM_job = None
        self.result_handles = None

    def get_program(self, simulate = False):
        """Runs the entire sequence"""
        with program() as prog:
            for sequence in self.subsequences:
                sequence.qua_declare_vars()

            with infinite_loop_():
                if not simulate:
                    pause()
                if True: #self.wait_for_trigger():
                    self.create_measurement_loop(simulate)

            with stream_processing():
                for sequence in self.subsequences:
                        sequence.qua_streams()
        return prog
    
    def create_measurement_loop(self, simulate = False):
        for sequence in self.subsequences:
            sequence.qua_sequence(cls = self, simulate = simulate)