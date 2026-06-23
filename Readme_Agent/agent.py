"""Agent class"""

import json
from llm import generate_response

class Agent:
    def __init__(self, registry, environment, memory, generate_response):
        self.registry = registry
        self.environment = environment
        self.memory = memory
        self.generate_response = generate_response


    def run(self, user_input):
        self.memory.add_to_memory(
            {
                "role": "user",
                "content": user_input
            }
        )

        while True:

            messages = self.build_prompt()

            response = generate_response(messages)

            print("\nLLM Response:")
            print(response)

            # Clean markdown if the LLM wrapped JSON in ```json
            response = response.strip()

            if response.startswith("```"):
                response = response.replace("```json", "")
                response = response.replace("```", "")
                response = response.strip()

            decision = json.loads(response)

            action_name = decision["action"]

            args = decision.get("args", {})

            action = self.registry.get_action(
                action_name
            )

            result = self.environment.execute_action(
                action,
                **args
            )

            self.memory.add_to_memory(
                {
                    "role": "assistant",
                    "content": response
                }
            )

            self.memory.add_to_memory(
                {
                    "role": "tool",
                    "content": str(result)
                }
            )

            if action.terminate:
                return result

    def build_prompt(self):

        actions = []

        for action in self.registry.get_all_actions():

            actions.append(
                f"""
Action Name: {action.name}

Description:
{action.description}

Parameters:
{action.parameters}
"""
            )

        return [
            {
                "role": "system",
                "content": f"""
You are a README generation agent.

1. List all Python files.
2. Read every Python file.
3. Understand the project.
4. Generate a README.md.
5. Use write_file_content() to save README.md.
6. Call terminate() after README.md is written.

Available actions:

{''.join(actions)}

Always respond with JSON.

Format:

{{
    "action": "action_name",
    "args": {{}}
}}
"""
            }
        ] + self.memory.get_memory()