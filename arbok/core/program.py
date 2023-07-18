from arbok.core.sequence import Sequence

class Program(Sequence):
    def __init__(self, name: str, sample, param_config=...):
        super().__init__(name, sample, param_config)

    def run(self):
        return