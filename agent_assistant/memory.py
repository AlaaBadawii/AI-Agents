"""
Memory management for the AI agent.
"""

class Memory:
    """A simple memory class to store and retrieve information."""

    def __init__(self):
        """Initialize the memory."""
        self.messages = []

    def add_user_message(self, content):
        """Add a user message to the memory."""
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content):
        """Add an assistant message to the memory."""
        self.messages.append({"role": "assistant", "content": content})

    def get_messages(self):
        """Retrieve all messages from the memory."""
        return self.messages
    
    def clear(self):
        """Clear memory"""
        self.messages.clear()

    def add_tool_message(self, tool_name, content, tool_call_id=None):
        """Add a tool message to the memory."""
        message = {
            "role": "tool",
            "name": tool_name,
            "content": content
        }

        if tool_call_id:
            message["tool_call_id"] = tool_call_id
        
        self.messages.append(message)
