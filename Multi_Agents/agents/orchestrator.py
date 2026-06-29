import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import agents

from llm import call_llm, extract_tool_call
from registery.agent_registry import registry as agent_registry

AGENT_TOOLS = agent_registry.get_schemas()
AGENT_FUNCTIONS = agent_registry.get_functions()

AVAILABLE_AGENTS = agent_registry.all_agents()

SYSTEM_PROMPT_TEMPLATE = """
You are the Orchestrator for Quizey, an assessment and training platform.
You coordinate specialized agents to fulfill user requests.

Available agents:
{available_agents}

Delegate to the appropriate agent with a clear detailed task description,
then present the result clearly and nicely formatted to the user.
"""


def _build_available_agents_text() -> str:
    lines = []
    for name, agent in AVAILABLE_AGENTS.items():
        lines.append(f"- {name}: {agent['schema']['description']}")
    return "\n".join(lines) if lines else "- No agents registered"


SYSTEM_PROMPT = SYSTEM_PROMPT_TEMPLATE.format(available_agents=_build_available_agents_text())


def run(user_request: str) -> str:
    messages       = [{"role": "user", "content": user_request}]
    max_iterations = 10

    for _ in range(max_iterations):
        response = call_llm(messages, AGENT_TOOLS, SYSTEM_PROMPT)

        if response["stop_reason"] == "tool_use":
            tool_call = extract_tool_call(response)
            result    = AGENT_FUNCTIONS[tool_call["name"]](**tool_call["input"])

            assistant_message = response["content"]
            messages.append({
                "role": "assistant",
                "content": assistant_message.get("content"),
                "tool_calls": assistant_message.get("tool_calls"),
            })
            # messages content is expected to be a string; serialize the tool result
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": json.dumps(result)
            })

        else:
            final_message = response["content"]
            final_content = final_message.get("content")

            if isinstance(final_content, str):
                return final_content

            if isinstance(final_content, list):
                for block in final_content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        return block.get("text", "")

            return str(final_content)

    return "Error: Orchestrator exceeded max iterations"