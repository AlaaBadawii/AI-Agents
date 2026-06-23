"""Tools for Agent to use"""

import os
from decorators import register_tool


@register_tool(tags=["file_operations"])
def list_files() -> list[str]:
    """Return a list of Python files in the current directory"""
    return sorted(
        file for file in os.listdir(".")
        if file.endswith(".py")
    )

@register_tool(tags=["file_operations", "read"])
def read_file_content(name: str) -> str:
    """Read a Python file"""
    with open(name, "r") as f:
        return f.read()

@register_tool(tags=["file_operations", "write"])
def write_file_content(name: str, content: str) -> str:
    """Write content to a file."""
    with open(name, "w") as f:
        f.write(content)
    return name


@register_tool(terminal=True)
def terminate(message: str) -> str:
    """End the Agent execution"""
    return message
