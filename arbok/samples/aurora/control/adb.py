from typing import Optional, List

from qm.qua import wait, amp, play, update_frequency, align

from arbok.core.sequence import Sequence
from arbok.core.sample import Sample
from arbok.samples.aurora.configs.aurora_qua_config import aurora_qua_config


class ADB(Sequence):
    """
    Class containing parameters and sequence for mixed down up initialization
    """
    def __init__(
            self,
            name: str,
            sample = Sample('aurora', aurora_qua_config),
            seq_config: dict = None
    ):
        """S
        Constructor method for 'MixedDownUpInit' class
        
        Args:
            name (str): name of sequence
            sample  (Sample): Sample class for physical device
            config (dict): config containing pulse parameters
        """
        super().__init__(name, sample)
        self.seq_config = seq_config
        if self.seq_config is None:
            self.seq_config = self.get_default_seq_config()
        self.add_qc_params_from_config(self.seq_config)
        self.chirp_rate(int(self.fChirp() / (self.tESRchirp()*4e-9) / 1e6))
    
    def qua_sequence(self):
        align()
        update_frequency('Q1',self.IfQ1())
        update_frequency('Q2',self.IfQ2())
        align()
        play('chirp'*amp(self.amp()), 'Q1', chirp=(self.chirp_rate(), 'MHz/sec'))
        align()
        wait(self.tPostControl(),'Q1')
        align()
        #self.control.shotTime = seq.tESRchirp

    def get_default_seq_config(
            self, elements: Optional[List[str]] = None) -> dict:
        """ 
        Generates the sequence configuration dictionary 
        
        Args:
            elements (list(str)): list of elements of importance for config

        Returns:
            dict: Configuration dictionairy for qua sequence
        """
        config = {
            'amp': {'unit': 'cycles', 'value': 455},
            'chirp_rate': {'unit': 'Hz', 'value': int(80e3/4)},
            'tESRchirp': {'unit': 'cycles', 'value': int(50e3/4)},
            'fChirp': {'unit': 'Hz', 'value': int(1.05e6)},
            'tPostControl': {'unit': 'cycles', 'value': int(80e3/4)},
            'IfQ1': {'unit': 'Hz', 'value': int(34.349e6)},
            'IfQ2': {'unit': 'Hz', 'value': int(71.119e6)},
        }
        return config