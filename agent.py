#!/usr/bin/env python3
"""
AI Agent Exercise:
Sequential prompting with memory using LiteLLM
"""

import re
from typing import List, Dict
from litellm import completion


SYSTEM_PROMPT = """
You are an expert Python software engineer.

Rules:
- Always generate clean and readable Python code.
- Use functional programming when appropriate.
- Return valid executable Python code.
- Keep explanations concise.
"""


def generate_response(messages: List[Dict]) -> str:
    """
    Send messages to the LLM and return the response content.
    """

    try:
        response = completion(
            model="openrouter/deepseek/deepseek-v4-flash",
            messages=messages,
            max_tokens=2048,
        )

        return response.choices[0].message.content

    except Exception as error:
        print(f"\n[ERROR] Failed to generate response:\n{error}")
        return ""


def extract_python_code(text: str) -> str:
    """
    Extract Python code from markdown code blocks.

    If no code block exists, return the raw text.
    """

    pattern = r"```python(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)

    if matches:
        return "\n\n".join(match.strip() for match in matches)

    return text.strip()


def print_section(title: str):
    """
    Print formatted section headers.
    """

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60 + "\n")


def main():

    # -------------------------------
    # Initialize conversation memory
    # -------------------------------

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # -------------------------------
    # User Input
    # -------------------------------

    user_request = input("What Python function do you want to create?\n> ")

    # -------------------------------
    # Prompt 1: Generate function
    # -------------------------------

    first_prompt = f"""
Write a basic Python function based on this request:

{user_request}

Requirements:
- Return ONLY Python code
- No markdown
- No explanations
"""

    messages.append({
        "role": "user",
        "content": first_prompt
    })

    response1 = generate_response(messages)

    raw_function_code = extract_python_code(response1)

    print_section("STEP 1 - GENERATED FUNCTION")

    print(raw_function_code)

    # Store assistant response in memory
    messages.append({
        "role": "assistant",
        "content": response1
    })

    # -------------------------------
    # Prompt 2: Add documentation
    # -------------------------------

    documentation_prompt = """
Improve the previous Python code by adding comprehensive documentation.

Include:
- Function description
- Parameter descriptions
- Return value description
- Example usage
- Edge cases

Requirements:
- Return ONLY Python code
- Add proper docstrings
- No markdown
"""

    messages.append({
        "role": "user",
        "content": documentation_prompt
    })

    response2 = generate_response(messages)

    documented_code = extract_python_code(response2)

    print_section("STEP 2 - DOCUMENTED FUNCTION")

    print(documented_code)

    messages.append({
        "role": "assistant",
        "content": response2
    })

    # -------------------------------
    # Prompt 3: Add unit tests
    # -------------------------------

    test_prompt = """
Add comprehensive unit tests using Python's unittest framework.

The tests must cover:
- Basic functionality
- Edge cases
- Error handling
- Various input scenarios

Requirements:
- Return ONLY executable Python code
- Include imports
- Keep the original function
- Add the tests below the function
- No markdown
"""

    messages.append({
        "role": "user",
        "content": test_prompt
    })

    response3 = generate_response(messages)

    final_code = extract_python_code(response3)

    print_section("STEP 3 - FINAL CODE WITH TESTS")

    print(final_code)

    # -------------------------------
    # Save final output
    # -------------------------------

    output_file = "generated_function.py"

    try:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(final_code)

        print_section("FILE SAVED")

        print(f"Final code saved to: {output_file}")

    except Exception as error:
        print(f"\n[ERROR] Failed to save file:\n{error}")


if __name__ == "__main__":
    main()