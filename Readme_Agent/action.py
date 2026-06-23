"""Action class"""

class Action:
    def __init__(
        self,
        name: str,
        function,
        description: str,
        parameters: dict | None = None,
        terminate: bool = False
    ):
        self.name = name
        self.function = function
        self.description = description
        self.parameters = parameters if parameters is not None else {}
        self.terminate = terminate
    
    def execute(self, **kwargs):
        return self.function(**kwargs)

    def __repr__(self):
        return f"Action(name={self.name},\
            description={self.description},\
            parameters={self.parameters},\
            terminate={self.terminate})"
    