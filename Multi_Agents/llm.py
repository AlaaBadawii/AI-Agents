"""OpenRouter chat-completions helpers used by the agents."""

import json
import os

from dotenv import load_dotenv
from litellm import completion


load_dotenv()

MODEL = "openrouter/deepseek/deepseek-v4-flash"
API_KEY = os.getenv("OPENROUTER_API_KEY")


def call_llm(messages: list, tools: list, system_prompt: str) -> dict:
    api_key = API_KEY or os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    response = completion(
        model=MODEL,
        api_key=api_key,
        messages=[{"role": "system", "content": system_prompt}] + messages,
        tools=[{"type": "function", "function": tool} for tool in tools],
        tool_choice="auto",
    )

    message = response["choices"][0]["message"]
    if hasattr(message, "model_dump"):
        message = message.model_dump()
    elif hasattr(message, "dict"):
        message = message.dict()

    return {
        "stop_reason": "tool_use" if message.get("tool_calls") else "end_turn",
        "content": message,
    }


def extract_tool_call(response: dict) -> dict:
    message = response["content"]
    tool_call = message["tool_calls"][0]

    return {
        "id": tool_call["id"],
        "name": tool_call["function"]["name"],
        "input": json.loads(tool_call["function"]["arguments"]),
    }