from qcodes.instrument import Instrument, InstrumentModule

class GettableSet(Instrument):
    def __init__(self, name, sequence = None):
        super().__init__(name = name)
        self.gettables = {}
        self.sequence = sequence

    def add_qc_gettables(self):
        for name, val in self.gettables.items():
            par_name = self.name + '_' + name
            if par_name not in self.parameters.keys():
                self.add_parameter(
                    name = par_name,
                    unit = val,
                    set_cmd = None,
                    get_cmd = None
                )
            else:
                raise NameError("Gettable \"" + par_name + "\" exists already")
    