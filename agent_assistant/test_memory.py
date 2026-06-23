from memory import Memory

memory = Memory()


memory.add_user_message("hello")
memory.add_tool_message("read_file", "content", 10)
memory.add_assistant_message("Hit there")

print(memory.get_messages())

memory.clear()

print(memory.get_messages())