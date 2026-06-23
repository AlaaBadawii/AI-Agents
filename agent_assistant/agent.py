"""
AI agent implementation that interacts with the memory and tools.
"""
import json
from litellm import completion
from memory import Memory
from tool_registry import TOOLS, TOOL_FUNCTIONS


class Agent:
    """An AI agent that interacts with memory and tools."""

    def __init__(
        self,
        model: str,
        system_prompt: str,
        max_iterations: int = 10,
    ):
        self.model = model
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations
        self.memory = Memory()

    def run(self, user_task: str):
        """
        Run the agent loop until the task is complete or max iterations reached.

        Loop:
        1. Add user task to memory
        2. Call LLM with available tools
        3. If LLM calls a tool — execute it, store result, continue
        4. If LLM calls terminate — print final message, stop
        5. If no tool call — print response, stop
        """
        self.memory.add_user_message(user_task)

        for iteration in range(self.max_iterations):
            print(f"\n--- Iteration {iteration + 1} ---")

            # ── Call LLM ─────────────────────────────────────────────────────
            response = completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    *self.memory.get_messages(),
                ],
                tools=TOOLS,
                tool_choice="auto",
            )

            message = response.choices[0].message

            # ── No tool call — LLM responded directly ─────────────────────
            if not message.tool_calls:
                content = message.content or ""
                print(f"\n🤖 Agent: {content}")
                self.memory.add_assistant_message(content)
                break

            # ── Tool call — execute each tool the LLM requested ───────────
            # Store the assistant message with tool_calls first
            self.memory.messages.append({
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        }
                    }
                    for tc in message.tool_calls
                ]
            })

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_call_id = tool_call.id

                # Parse arguments safely
                try:
                    arguments = json.loads(tool_call.function.arguments or "{}")
                except json.JSONDecodeError:
                    arguments = {}

                print(f"🔧 Calling tool: {tool_name}({arguments})")

                # ── Terminate ────────────────────────────────────────────────
                if tool_name == "terminate":
                    message_arg = arguments.get("message", "Task complete.")
                    print(f"\n✅ Agent finished: {message_arg}")
                    return

                # ── Execute tool ─────────────────────────────────────────────
                tool_fn = TOOL_FUNCTIONS.get(tool_name)

                if not tool_fn:
                    result = f"Error: Tool '{tool_name}' not found."
                else:
                    try:
                        result = tool_fn(**arguments)
                    except Exception as e:
                        result = f"Error: {str(e)}"

                print(f"📦 Result: {str(result)[:200]}")

                # Store tool result in memory
                self.memory.add_tool_message(
                    tool_name=tool_name,
                    content=str(result),
                    tool_call_id=tool_call_id,
                )

        else:
            print(f"\n⚠️  Max iterations ({self.max_iterations}) reached.")