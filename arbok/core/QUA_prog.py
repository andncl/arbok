
class QuaProgram():
    """
    Class describing a QUA programmincluding (Init, Control, Read) 
    """
    def __init__(self, config: dict):
        """
        Constructor class for 'QuaProgram' class.

        Args:
            name (str): Name of the program
            init_seq (func): QUA sequence for qubit initialization
            control_seq (func): QUA sequence for qubit control
            readout_seq (func): QUA sequence for qubit readout
        """
        self.name = name
        self.config = config
        self.qua_programm = None
        self.elements = None
    
    def get_program(self):
        """Runs the entire sequence"""
        self.init_seq
        self.control_seq
        self.readout_seq

    def init_seq(self):
        """QUA sequence for qubit initialization"""
        pass

    def control_seq(self):
        """QUA sequence for qubit control"""
        pass

    def readout_seq(self):
        """QUA sequence for qubit readout"""
        pass


