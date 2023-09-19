import copy

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import (
    program, infinite_loop_, pause, stream_processing, declare, for_, assign
)
from qm import SimulationConfig

from qcodes.parameters import Parameter
from qcodes.validators import Arrays
from qcodes.dataset import Measurement

from arbok.core.sequence import Sequence
from arbok.core.sample import Sample

class Program(Sequence):
    """
    Class containing all functionality to manage and run modular sequences on a 
    physical OPX instrument
    """
    def __init__(self, name: str, sample: Sample, param_config: dict = {}):
        """
        Constructor class for `Program` class
        
        Args:
            name (str): Name of the program
            sample (Sample): Sample class describing phyical device
            param_config (dict): Dictionary containing all device parameters
        """
        super().__init__(name, sample, param_config)

        self.qmm = None
        self.opx = None
        self.qm_job = None
        self.result_handles = None

        self.stream_mode = "pause_each"
    
    def connect_opx(self, host_ip: str):
        """
        Creates QuantumMachinesManager and opens a quantum machine on it with
        the given IP address
        
        Args:
            host_ip (str): Ip address of the OPX
        """
        self.qmm = QuantumMachinesManager(host = host_ip)
        self.opx = self.qmm.open_qm(self.sample.config)

    def run(self, program):
        """
        Sends the program for execution to the OPX and sets the programs 
        result handles 
        
        Args:
            program (program): QUA program to be executed
        """
        self.qm_job = self.opx.execute(program)
        self.result_handles = self.qm_job.result_handles
        if self.stream_mode == "pause_each": 
           self.qm_job.resume()

    def get_running_qm_job(self):
        """ Finds qm_job on the connected opx and returns it. Also sets program 
        attributes qm_job and result_handles """
        # FIXME: not really working .. retreived job is not functional after 
        #   restarting python environment
        self.qm_job = self.opx.get_running_job()
        self.result_handles = self.qm_job.result_handles
        return self.qm_job

    def prepare_meas_ctrl(self, meas_ctrl):
        """ DEPRECATED due to move from quantify to QCoDeS measuring
        Prepares quantify-core MeasurementControl object meas_ctrl
        
        Args: 
            meas_ctrl (MeasurementControl): quantify measurement context
        """
        meas_ctrl.settables(self.settables)
        meas_ctrl.setpoints_grid(self.setpoints_grid)
        meas_ctrl.gettables(self.gettables)
        self.prepare_gettables()

    def prepare_gettables(self):
        """
        Prepares the `SequenceParameter`s and `GettableParameters`.
        `GettableParameters` are QCoDeS ParameterWithSetpoints. Those are
        defined with setpoints which are in our case the se
        """
        self.settables.reverse()
        self.setpoints_grid.reverse()
        iteration = ShotNumber(name='iteration', instrument=self)
        self.add_parameter(iteration)
        for i, settable in enumerate(self.settables):
            settable.vals = Arrays(shape=(len(self.setpoints_grid[i]),))
            print(settable.vals)
            #settable.vals = Arrays(
            #    shape = tuple(len(x) for x in self.setpoints_grid))
            #settable.set_raw(settable_value_grid[i])

        for i, gettable in enumerate(self.gettables):
            gettable.batch_size = self.sweep_size()
            gettable.can_resume = True if i==(len(self.gettables) -1) else False
            gettable.setpoints = tuple(self.settables)
            gettable.vals = Arrays(
                shape = tuple(len(x) for x in list(self.setpoints_grid))
                )
        """
        Configures and runs QCoDeS measurement object from the arbok program
        
        Args:
            measurement (Object): QCoDeS measurement object
        """
        iteration = ShotNumber(name='iteration', instrument=self)
        measurement.register_parameter(iteration)

        add_result_args = ((iteration, iteration.get()))
        for i, settable in enumerate(self.settables):
            measurement.register_parameter(settable)
            add_result_args += (settable, self.setpoints_grid[i])

        for gettable in self.gettables:
            measurement.register_parameter(
                gettable, setpoints = tuple(self.settables))
            add_result_args += (gettable, gettable.get())

        print(add_result_args)
        with measurement.run() as datasaver:
            for shot in range(shots):
                iteration.set(shot)
                datasaver.add_result(
                    (iteration, shot),
                    (self.settables[0], self.setpoints_grid[0]),
                    (self.settables[1], self.setpoints_grid[1]),
                    (self.gettables[0], self.gettables[0].get()),
                    (self.gettables[1], self.gettables[1].get()),
                    )
            dataset = datasaver.dataset
        return dataset

    def get_program(self, simulate = False):
        """
        Runs the entire sequence by searching recursively through init, 
        sequence and stream methods of all subsequences and their subsequences

        Args:
            simulate (bool): Flag whether program is simulated
        
        Returns:
            program: Program compiled into QUA language
        """
        with program() as prog:
            self.recursive_qua_generation(seq_type = 'declare')
            with infinite_loop_():
                if not simulate:
                    pause()
                self.recursive_sweep_generation(
                    copy.copy(self.settables),
                    copy.copy(self.setpoints_grid)
                    )
            with stream_processing():
                self.recursive_qua_generation(seq_type = 'stream')
        return prog
    
    def run_local_simulation(self, duration: int):
        """
        Simulates the given program of the sequence for `duration` cycles

        Args:
            duration (int): 

        Returns:
            simulated_job (SimulatedJob): QM job with waveform simulation result
        """
        if not self.qmm:
            raise ConnectionError(
                "No QMM found! Connect an OPX via `connect_OPX`")
        simulated_job = self.qmm.simulate(
            self.sample.config,
            self.get_program(simulate = True),
            SimulationConfig(duration=duration))
     
        samples = simulated_job.get_simulated_samples()
        self._plot_simulation_results(samples)
        return simulated_job
    
class ShotNumber(Parameter):
    """ Parameter that keeps track of averaging during measurement """
    def __init__(self, name, instrument):
        super().__init__(name, instrument = instrument)
        self._count = 0

    def get_raw(self): return self._count
    def set_raw(self, x): self._count = x