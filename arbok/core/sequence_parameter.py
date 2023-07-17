from qcodes.parameters import Parameter

class SequenceParameter(Parameter):
    """
    A parameter wrapper that adds the respective element as attribute
    """
    def __init__(self, element, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.element = element

    def return_qua_var(self):
        return