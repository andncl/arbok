from qcodes.parameters import Parameter, ParameterWithSetpoints
from qm.qua import *

class SequenceParameter(Parameter):
    """
    A parameter wrapper that adds the respective element as attribute
    """
    def __init__(self, elements, *args, **kwargs):
        """
        Constructor for 'SequenceParameter' class

        Args:
            elements (list): Elements that should be influenced by parameter
            batched (bool): Is the variab
        """
        super().__init__(*args, **kwargs)
        self.element = elements
        self.batched = False
        self.qua_var = None


    def __call__(self, *args, **kwargs):
        if len(args) == 1:
            self.set(*args)
        elif self.batched:
            return self.qua_var
        else: 
            return self.get()

class ReadParameter(ParameterWithSetpoints):
    """
    A read parameter wrapper containing OPX result fetching logic
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor for 'ReadParameter' class
        """
        self.result = None
        self.counts_so_far = 0
        self.last_result = None

    def get_raw(self):
        if not self.root_instrument.opx:
            raise LookupError("Results cant be retreived without OPX")
        
        if self.result == None:
            self.result = getattr(
                self.root_instrument.job.results_handler,self.name)
            self.sweep_size = self.root_instrument.sweep_size()
            self.setpoints = tuple(self.root_instrument.settables)

        else:
            return self._fetch_from_opx()

    def _fetch_from_opx(self):
        self.result.fetch
        
