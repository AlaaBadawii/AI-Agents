"""
File-related tools for the AI Agent
"""

import os
from pathlib import Path


def list_files(directory: str = ".") -> list[str]:
    """
    list files and folders in a directory
    Args:
        directory: Directory path.
    Returns:
        List of files and folder names.
    """
    try:
        return os.listdir(directory)
    except FileNotFoundError:
        return [f"Error: File Not Found Error"]
    except Exception as e:
        return [f"Error:  {str(e)}"]

def read_file(file_name: str) -> str:
    """
    Read a files's contents.
    If the file is not found directly,
    search from the current directory.

    Args:
        file_name: File name or path.
    Returns:
        File contents or error message.
    """
    try:
        path = Path(file_name)

        if path.exists():
            return path.read_text(encoding="utf-8")
        
        return f"Error: {file_name} not found"
    except Exception as e:
        return f"Error: {str(e)}"




    