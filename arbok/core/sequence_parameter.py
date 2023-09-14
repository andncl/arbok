from qcodes.parameters import Parameter, ParameterWithSetpoints
from qcodes.validators import Arrays
from qm.qua import *

import warnings

class SequenceParameter(Parameter):
    """
    A parameter wrapper that adds the respective element as attribute
    """
    def __init__(self, element, config_name, *args, **kwargs):
        """
        Constructor for 'SequenceParameter' class

        Args:
            elements (list): Elements that should be influenced by parameter
            batched (bool): Is the variab
        """
        super().__init__(*args, **kwargs)
        self.element = element
        self.config_name = config_name
        self.batched = False
        self.qua_var = None

    def __call__(self, *args, **kwargs):
        if len(args) == 1:
            self.set(*args)
        elif self.batched:
            return self.qua_var
        else: 
            return self.get()

    def set_on_program(self, *args):
        """ Adds parameter as settable on OPX program """
        self.root_instrument.settables.append(*args[0])

class GettableParameter:
    """
    This is a valid Gettable not because of inheritance, but because it has the
    expected attributes and methods.
    """
    def __init__(self, name, readout, *args, **kwargs) -> None:
        """
        Constructor class for ReadSequence class
        Args:
            name (dict): name of the GettableParameter
            readout (Readout): Readout class summarizing data streams and variables
        """
        self.name = name
        self.unit = ""
        self.label = ""
        self.batched = True
        self.delay = 0.0
        self.can_resume = False

        self.readout = readout
        self.program = None
        self.qm_job = None
        self.result = None
        self.buffer = None
        self.buffer_val = None
        self.shape = None
        self.count_so_far = 0
        self.last_result = None
        self.batch_size = 0
        self.count = 0

    def get(self):
        """ Get method to retrieve a single batch of data from a running measurement"""
        if self.result is None:
            # Will be executed on the first call of get()
            self.set_up_gettable_from_program()
            #if self.program.stream_mode == "pause_each" and not self.can_resume: 
            #    self.qm_job.resume()
      
        self._fetch_from_opx()
        if self.buffer_val is None:
            warnings.warn("NO VALUE STREAMED!")
        if self.program.stream_mode == "pause_each" and self.can_resume: 
            self.qm_job.resume()
        return self.buffer_val
    
    def set_up_gettable_from_program(self):
        """ Set up Gettable attributes from running OPX """
        self.program = self.readout.sequence.root_instrument
        if not self.readout.sequence.root_instrument.opx:
            raise LookupError("Results cant be retreived without OPX connected")
        self.qm_job = self.program.qm_job
        self.result = getattr( self.qm_job.result_handles, self.name )
        self.buffer = getattr( self.qm_job.result_handles, self.name + '_buffer')
        self.shape = tuple([len(x) for x in self.program.setpoints_grid])
        self.batch_size = self.program.sweep_size()

    def _fetch_from_opx(self):
        """ Fetches and returns data from OPX after results came in """
        self.count_so_far = self.result.count_so_far()
        print("FETC", self.count_so_far, (self.count + 1)*self.batch_size, self.name)
        if self.count_so_far > (self.count + 2)*self.batch_size:
            warnings.warn("OVERHEAD of data on OPX! Try larger batches or other sweep type!")

        self._wait_until_buffer_full()
        print("READ", self.result.count_so_far(), (self.count + 1)*self.batch_size)
        self._fetch_opx_buffer()

    def _wait_until_buffer_full(self):
        """ This function is running until a batch with self.batch_size is ready """
        while self.count_so_far < (self.count + 1)*self.batch_size:
            print("WAIT", self.count_so_far, (self.count + 1)*self.batch_size)
            self.count_so_far = self.result.count_so_far()

    def _fetch_opx_buffer(self):
        """
        Fetches the OPX buffer into the `buffer_val` and increments the internal
        counter `count`
        """
        self.buffer_val = self.buffer.fetch(-1)
        print("Buffersize", np.shape(self.buffer_val))
        if self.buffer_val is None:
            raise ValueError("NO VALUE STREAMED")
        self.count += 1

    def get_all(self):
        """ Fetches ALL (not buffered) data """
        if self.result:
            return self.result.fetch_all()
        else:
            raise LookupError("Results cant be retreived without OPX")