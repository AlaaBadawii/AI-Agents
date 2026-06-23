"""Test action registery"""
from ..action import Action
from ..action_registery import ActionRegistry
from ..tools import read_file_content, list_files, terminate


def test_action_registry():
    """Test ActionRegistry functionality"""
    registry = ActionRegistry()

    # Create actions
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

    # Register actions
    registry.register_action(read_file_content_action)
    registry.register_action(list_files_action)
    registry.register_action(terminate_action)

    # Test get_action
    assert registry.get_action("read_file_content") == read_file_content_action
    assert registry.get_action("list_files") == list_files_action
    assert registry.get_action("terminate") == terminate_action

    # Test list_actions
    assert set(registry.list_actions()) == {"read_file_content", "list_files", "terminate"}