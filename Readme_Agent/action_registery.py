"""Registry for managing available actions"""
from decorators import _tools, _tools_by_tag
from action import Action


class ActionRegistry:
    """Registry for managing available actions"""

    def __init__(self, tags =None):
        self._actions = {}
        if tags:
            tool_name = set()
            for tag in tags:
                tool_name.update(_tools_by_tag.get(tag, []))
        else:
            tool_name = set(_tools.keys())
        
        for name in tool_name:
            tool = _tools[name]
            self._actions[name] = Action(
                name=name,
                function=tool["function"],
                description=tool["description"],
                parameters=tool["parameters"],
                terminate=tool["terminal"]
            )


    def get_action(self, name):
        return self._actions.get(name)

    def get_all_actions(self):
        return list(self._actions.values())

    def list_actions(self):
        return list(self._actions.keys())