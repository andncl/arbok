from qm.qua import *
from Configuration import *

class BaseClass:
    def __init__(self):
        self.name = 'base'
        
class PulseSequence(BaseClass):
    
    
    
    def __init__(self, parent):
        self.parent = parent
        self.control = parent.control
        self.shotTime = int(0)
        
        self.gateElements = parent.parent.gateElements
        
    def edit_seq(self,**kwargs): 
        ### Read all the input arguments and assign
        ### the labels and values to two lists: keys and values.
        keys = list(kwargs.keys())
        values = list(kwargs.values())
        
        ### Go through the inputs and, if an input is given, replace the
        ### default value with the QUA variable
        for k in range(0,len(values)):
            val = values[k]
            assignString = 'self.' + keys[k] + ' = val'
            exec(assignString)
                
        # self.seq()    
    
    def addLevel(self, seq, level_string):
        
        level = self.parent.parent.levels[level_string]
        
        for nn in range(len(self.gateElements)):
            element = self.gateElements[nn]
            play('unit_ramp_20ns'*amp(eval('seq.v_'+ level_string)[nn]), element, duration = eval('seq.tRamp_'+ level_string))
            
        align()
        if level.time != 0:
            wait(eval('seq.t_'+ level_string),self.gateElements)
            align()