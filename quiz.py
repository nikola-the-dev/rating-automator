class Quiz:

    # Instance initialization

    def __init__(self):
        self._step = 0


    # Variables

    @property
    def step(self):
        return self._step
    @step.setter
    def step(self, step):
        self._step = step