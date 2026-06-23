import tools

from action_registery import ActionRegistry
from environment import Environment
from memory import Memory
from agent import Agent
from llm import generate_response
from decorators import _tools
from action import Action


registry = ActionRegistry(tags=["file_operations"])

terminate_tool = _tools["terminate"]
registry._actions["terminate"] = Action(
    name="terminate",
    function=terminate_tool["function"],
    description=terminate_tool["description"],
    parameters=terminate_tool["parameters"],
    terminate=terminate_tool["terminal"]
)


memory = Memory()
environment = Environment()

agent = Agent(
    registry,
    environment,
    memory,
    generate_response
)

print(agent.run("write a README.md file for this project."))