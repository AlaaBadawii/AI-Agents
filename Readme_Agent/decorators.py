import inspect
from typing import get_type_hints
import os

_tools = {}
_tools_by_tag = {}

def register_tool(tags=None, terminal=False):
    def decorator(func):
        tool_name = func.__name__
        description = func.__doc__.strip() if func.__doc__ else "No description"


        sig = inspect.signature(func)
        hints = get_type_hints(func)

        properities = {}
        requirred = []

        for param_name, param in sig.parameters.items():
            python_type = hints.get(param_name, str)
            json_type =  "string" if python_type is str else "number"
            properities[param_name] = {"type": json_type}

            if param.default is inspect.Parameter.empty:
                requirred.append(param_name)
            
        _tools[tool_name] = {
            "function": func,
            "description": description,
            "parameters": {
                "type": "object",
                "properities": properities,
                "required": requirred
            },
            "terminal": terminal
        }

        for tag in (tags or []):
            if tag not in _tools_by_tag:
                _tools_by_tag[tag] = []
            _tools_by_tag[tag].append(tool_name)
        
        return func
    
    return decorator