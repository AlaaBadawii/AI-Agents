"""Decorator functions for registering tools and agents."""

import inspect
from registery.agent_registry import registry as agent_registry
from registery.tool_registery import registry

TYPE_MAP = {
    int: "integer",
    float: "number",
    str: "string",
    bool: "boolean",
    list: "array",
    dict: "object",
}


def _build_parameters(func):
    sig = inspect.signature(func)
    parameters = {
        "type": "object",
        "properties": {},
        "required": [],
    }

    for param_name, param in sig.parameters.items():
        param_type = TYPE_MAP.get(param.annotation, "string")
        parameters["properties"][param_name] = {"type": param_type}
        if param.default is inspect.Parameter.empty:
            parameters["required"].append(param_name)

    return parameters


def register_tool(tags: list | None = None, terminal: bool = False):
    """
    Decorator that registers a function as a tool in the shared registery

    Args:
        tags: List of tags for filtering which agent gets this tool
        terminal: If True, calling this tool ends the agent loop

    Usage:
        @register_tool(tags=["question_generation"], terminal=False)
        def generate_question(topic: str, difficulty: str) -> dict:
            \"\"\"Generate a complete MCQ question.

            Args:
                topic:      The subject area e.g. Python loops
                difficulty: easy, medium, or hard
            \"\"\"
            ...
    """
    _tags = tags or []

    def decorator(func):
        schema = {
            "name": func.__name__,
            "description": (func.__doc__ or "").strip().split("\n")[0],
            "parameters": _build_parameters(func),
        }

        # Register the tool in the shared registry
        registry.register(func.__name__, func, schema, _tags, terminal)
        return func
    return decorator


def register_agent(
    name: str | None = None,
    tags: list | None = None,
    terminal: bool = False,
    description: str | None = None,
):
    """Decorator that registers a function as an agent in the shared registry."""
    _tags = tags or []

    def decorator(func):
        agent_name = name or func.__name__
        agent_schema = {
            "name": agent_name,
            "description": (description or func.__doc__ or "").strip().split("\n")[0],
            "parameters": _build_parameters(func),
        }

        agent_registry.register(agent_name, func, agent_schema, _tags, terminal)
        return func

    return decorator
