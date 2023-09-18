#\\ COMMERCIAL-IN-CONFIDENCE
#\\ DO NOT DISTRIBUTE WITHOUT PRIOR CONSENT FROM PROF ANDREW DZURAK.
#\\ Copyright Dzurak Research Group, UNSW.
"""
General readout class to manage measurements

SSR
24/06/2022
"""

from qm.qua import *
import matplotlib.pyplot as plt
from arbok.core.sequence import Sequence

class SetRead():
    """ Helper class for SET readout """
    def __init__(self, name: str, sequence: Sequence, read_label: str, 
        streaming: bool = False):
        """ 
        Constructor method to initialize SET current readout 
        
        Args:
            name (str): name of Readout object
            sequence (Sequence): `ReadSequence` containing this instance
            read_label (str): Name of readout element 
        """
        self.name = name
        self.sequence =  sequence
        self.read_label = read_label
        
        self.read_I = None
        self.read_Q = None
        self.stream_list = []

    #def get(self):
    #    return self.program_handler.get_result(self.name)
    
    def init_qua_vars(self):
        """ Initializes QUA variables in which streams are saved""" 
        self.read_I = declare(fixed)
        self.read_Q = declare(fixed)

        self.read_I_stream = declare_stream()
        self.read_Q_stream = declare_stream()


        #for stream_name in self.stream_list:
        #    setattr(self, stream_name, declare_stream)

    def measure(self):
        """ Runs measure operation on self.read_label (readout) element"""
        measure('measure', self.read_label, None,
                demod.full('x',self.read_I),
                demod.full('y',self.read_Q))
        
    def save(self):        
        """ Saves I and Q on their respective streams """
        save(self.read_I, self.read_I_stream)
        save(self.read_Q, self.read_Q_stream)

    
    def measureAndSave(self):
        """ Performs a measurement and saves results on their streams """
        align()
        self.measure()
        self.save()
        align()
        
    
    def save_streams(self):
        """ Saves the streams to be fetchable from instrument """
        self.read_I_stream.save_all(self.name+"_read_I")
        self.read_Q_stream.save_all(self.name+"_read_Q")