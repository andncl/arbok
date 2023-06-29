
class Sample():
    """
    Class describing the used sample by its config and the used sequence. 
    """
    def __init__(self, name: str, config: dict):
        """
        Constructor class for 'Sample' class.

        Args:
            name (str): Name of the used sample
            config (dict): OPX configuration file for sample
            qua_program (func): QUA function to be uploaded to OPX
            self.elements (list): List of all quantum elements
        """
        self.name = name
        self.config = config
        self.qua_programm = None
        self.elements = None
    
    def set_programm(self, programm):
        """Sets the qua programm"""
        self.qua_programm = programm
