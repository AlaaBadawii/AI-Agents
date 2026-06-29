"""Registry for managing and storing registered agents."""


class AgentRegistry:
    """A registry for managing and storing registered agents."""

    def __init__(self):
        self._agents = {}

    def register(self, name: str, function, schema: dict, tags: list, terminal: bool = False):
        """Register an agent with a given name."""
        if name in self._agents:
            raise ValueError(f"Agent '{name}' is already registered.")
        self._agents[name] = {
            "function": function,
            "schema": schema,
            "tags": tags,
            "terminal": terminal,
        }

    def get_schemas(self, tags: list | None = None) -> list:
        """Retrieve the schemas of registered agents by tags."""
        result = []
        for name, agent in self._agents.items():
            if not tags or any(tag in agent["tags"] for tag in tags):
                result.append(agent["schema"])
        return result

    def get_functions(self, tags: list | None = None) -> dict:
        """Retrieve the functions of registered agents by tags."""
        result = {}
        for name, agent in self._agents.items():
            if not tags or any(tag in agent["tags"] for tag in tags):
                result[name] = agent["function"]
        return result

    def is_terminal(self, name: str) -> bool:
        """Check if an agent is marked as terminal."""
        agent = self._agents.get(name)
        return agent["terminal"] if agent else False

    def all_agents(self):
        """Return all registered agents."""
        return self._agents


registry = AgentRegistry()