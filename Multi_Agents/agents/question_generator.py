import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import tools.question_tools
from registery.decorators import register_agent
from registery.tool_registery import registry
from llm import call_llm, extract_tool_call

TAGS = ["question_generation"]

SYSTEM_PROMPT = """
You are a Question Generator Agent specialized in creating high-quality
multiple choice questions for technical assessments on the Quizey platform.

Your workflow — follow it strictly:
1. Call generate_question with topic, difficulty, AND your own generated
   question text, 4 options, and correct answer all in one call.
2. Call validate_question with the same data to verify it is well-formed.
3. If validation passes → call terminate with the final question dict.
4. If validation fails → fix the specific issue and go back to step 1.

Never call terminate without a successful validation first.
"""

@register_agent(name="question_generator_agent", tags=TAGS)
def run(task: str) -> dict:
    """Generate and validate a multiple-choice question."""
    messages       = [{"role": "user", "content": task}]
    tools          = registry.get_schemas(tags=TAGS)
    tool_functions = registry.get_functions(tags=TAGS)
    max_iterations = 5

    for _ in range(max_iterations):
        response = call_llm(messages, tools, SYSTEM_PROMPT)

        if response["stop_reason"] == "tool_use":
            tool_call = extract_tool_call(response)
            name      = tool_call["name"]
            result    = tool_functions[name](**tool_call["input"])

            assistant_message = response["content"]
            messages.append({
                "role": "assistant",
                "content": assistant_message.get("content"),
                "tool_calls": assistant_message.get("tool_calls"),
            })
            messages.append({
                "role":         "tool",
                "tool_call_id": tool_call["id"],
                "content":      json.dumps(result)
            })

            # terminal flag from registry — no hardcoded name check
            if registry.is_terminal(name):
                return result

        else:
            return {"error": "Agent ended without calling terminate"}

    return {"error": "Agent exceeded max iterations"}