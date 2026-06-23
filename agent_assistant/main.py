"""
Entry point for the AI Agent system.
"""

from agent import Agent
from Prompts import SYSTEM_PROMPT


def main():
    print("\n🤖 AI Agent Started (type 'exit' to quit)\n")

    agent = Agent(
        model="openrouter/deepseek/deepseek-v4-flash",
        system_prompt=SYSTEM_PROMPT,
        max_iterations=10,
    )

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            print("\nGoodbye 👋")
            break

        agent.run(user_input)


if __name__ == "__main__":
    main()