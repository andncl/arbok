from qcodes.parameters import Parameter, ParameterWithSetpoints
from qcodes.validators import Arrays
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
        super().__init__(*args, **kwargs)
        self.result = None
        self.counts_so_far = 0
        self.last_result = None
        self.buffer = None
        self.result = None
        self.batched = True
        self.batch_size = self.root_instrument.sweep_size()
        self.count = 0

    def get_raw(self):
        if not self.root_instrument.opx:
            raise LookupError("Results cant be retreived without OPX")
        
        if self.result == None:
            self.buffer = getattr(
                self.root_instrument.qm_job.result_handles,self.name + '_buffer')
            self.result = getattr(
                self.root_instrument.qm_job.result_handles,self.name)
            self.setpoints = tuple(self.root_instrument.settables) 
            self.shape = tuple([len(x) for x in self.root_instrument.setpoints_grid])
            self.batch_size = self.root_instrument.sweep_size()
            #self.vals = Arrays(shape = self.shape) 
            self.count += 1
            

        else:
            return self._fetch_from_opx()

    def _fetch_from_opx(self):
        if not self.root_instrument.qm_job.is_paused() or self.result.count_so_far() < self.count*self.batch_size :
            print(
                'busy \n',
                'paused;  ' + str(self.root_instrument.qm_job.is_paused()) + '\n',
                'total counts: ' + str(self.result.count_so_far()) + '\n',
                'registerd; ' + str(self.count*self.batch_size) + '\n',
                end = '\r')
            self._fetch_from_opx()

        else:
            print(
                'New result! \n',
                'paused;  ' + str(self.root_instrument.qm_job.is_paused()) + '\n',
                'total counts: ' + str(self.result.count_so_far()) + '\n',
                'registerd; ' + str(self.count*self.batch_size) + '\n',
                end = '\r')
            self.root_instrument.qm_job.resume()
            buffer_val = self.buffer.fetch_all()
            if buffer_val is None:
                self._fetch_from_opx()
            else:
                self.count +=1
                print(buffer_val.reshape(list(self.shape)).astype(int))
                return buffer_val.reshape(list(self.shape)).astype(int)
        
    def get_all(self):
        if self.result:
            return self.result.fetch_all()
        else:
            raise LookupError("Results cant be retreived without OPX")
