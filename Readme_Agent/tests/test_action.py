from ..tools import read_file_content, list_files, terminate
from ..action import Action

read_file_content_action = Action(
    name="read_file_content",
    function=read_file_content,
    description="Read a Python file",
    parameters={"name": "tools.py"},
    terminate=False
)

list_files_action = Action(
    name="list_files",
    function=list_files,
    description="Return a list of Python files in the current directory",
    parameters={},
    terminate=False
)
terminate_action = Action(
    name="terminate",
    function=terminate,
    description="End the Agent execution",
    parameters={"message": "End of test"},
    terminate=True
)