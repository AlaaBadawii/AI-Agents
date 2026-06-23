"""
Tool registry for the AI Agent.
"""

from tools.file_tools import list_files, read_file
from tools.utility_tools import terminate


# Functions the Python code can execute
TOOL_FUNCTIONS = {
    "list_files": list_files,
    "read_file": read_file,
    "terminate": terminate,
}


# Tool definitions exposed to the LLM
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files and folders in a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory path."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "Name or path of the file."
                    }
                },
                "required": ["file_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "terminate",
            "description": "End the task when it is complete.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Final completion message."
                    }
                },
                "required": ["message"]
            }
        }
    }
]