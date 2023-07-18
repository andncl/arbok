from qcodes.parameters import Parameter
from qm.qua import *

class SequenceParameter(Parameter):
    """
    A parameter wrapper that adds the respective element as attribute
    """
    def __init__(self, element, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.element = element
        self.batched = False
        self.qua_var = None

    def __call__(self, *args, **kwargs):
        if len(args) == 1:
            self.set(*args)
        elif self.batched:
            return self.qua_var
        else: 
            return self.get()
            
    def return_qua_var(self):
        return