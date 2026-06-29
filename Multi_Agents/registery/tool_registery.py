"""Registry for managing and storing registered components."""

class ToolRegistry:
    """A registry for managing and storing registered tools."""

    def __init__(self):
        self._tools = {}

    def register(self, name: str, function, schema:dict, tags: list, terminal: bool = False):
        """Register a tool with a given name."""
        if name in self._tools:
            raise ValueError(f"Tool '{name}' is already registered.")
        self._tools[name] = {
            "function": function,
            "schema": schema,
            "tags": tags,
            "terminal": terminal
        }

    def get_schemas(self, tags: list | None = None) -> list:
        """Retrieve the schemas of registered tools by tags."""
        result = []
        for name, tool in self._tools.items():
            if not tags or any(tag in tool["tags"] for tag in tags):
                result.append(tool["schema"])
        return result


    def get_functions(self, tags: list | None = None) -> dict:
        """Retrieve the functions of registered tools by tags."""
        result = {}
        for name, tool in self._tools.items():
            if not tags or any(tag in tool["tags"] for tag in tags):
                result[name] = tool["function"]
        return result
    
    def is_terminal(self, name: str) -> bool:
        """Check if a tool is marked as terminal."""
        tool = self._tools.get(name)
        return tool["terminal"] if tool else False
    
    def all_tags(self):
        """Retrieve all unique tags from registered tools."""
        tags_set = set()
        for tool in self._tools.values():
            tags_set.update(tool["tags"])
        return list(tags_set)

registry = ToolRegistry()
