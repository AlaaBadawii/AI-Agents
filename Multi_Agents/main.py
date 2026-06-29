import sys
import os

sys.path.append(os.path.dirname(__file__))

from agents.orchestrator import run


def main():
    print("=== Quizey Multi-Agent System ===")
    print("Try: 'Generate a medium Python question about for loops'")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        print("\n[Orchestrator thinking...]\n")
        result = run(user_input)
        print(f"Quizey: {result}\n")
        print("-" * 50 + "\n")


if __name__ == "__main__":
    main()