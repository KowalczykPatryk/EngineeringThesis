
class Agent:
    def __init__(self, model, environment):
        self.model = model
        self.environment = environment

    def act(self, state):
        raise NotImplementedError("Subclasses must implement this method")
