# Agent Assistant

A general-purpose conversational AI agent that can explore and read files on demand.

Built from scratch without frameworks — no LangChain, no CrewAI.

---

## What It Does

You talk to it in a loop. It decides whether to answer directly or use a tool.
If it needs to look at files, it calls the right tool, gets the result, and
continues reasoning until it has a complete answer.

```
You: list files in the project folder
--- Iteration 1 ---
🔧 Calling tool: list_files({"directory": "."})
📦 Result: ['agent.py', 'main.py', 'memory.py', ...]
🤖 Agent: Here are the files in your project: ...
```

---

## Architecture

```
main.py
  └── Agent (agent.py)
        ├── Memory (memory.py)         — conversation history
        ├── TOOLS (tool_registry.py)   — LLM-facing schema
        ├── TOOL_FUNCTIONS             — Python callables
        └── tools/
              ├── file_tools.py        — list_files, read_file
              ├── utility_tools.py     — terminate
              └── search_tools.py      — extensible
```

**The agent loop (`agent.py`):**
1. Add user message to memory
2. Call LLM with full conversation history + tool schemas
3. If LLM returns a tool call → execute it, store result, go to step 2
4. If LLM calls `terminate` → print final message, stop
5. If LLM responds directly → print response, stop
6. Repeat until done or `max_iterations` reached

**Two separate registries:**
- `TOOLS` — JSON schema the LLM sees to decide what to call
- `TOOL_FUNCTIONS` — actual Python functions your code executes

This separation is intentional. The LLM never runs code directly — it just
returns a JSON object saying what to call. Your code does the execution.

---

## Tools

| Tool | Description |
|---|---|
| `list_files(directory)` | Lists files and folders in a directory |
| `read_file(file_name)` | Reads and returns file contents |
| `terminate(message)` | Signals task completion, ends the loop |

Adding a new tool takes two steps — add the function to `tools/`, add its
schema to `TOOLS` and its reference to `TOOL_FUNCTIONS` in `tool_registry.py`.

---

## Setup

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Create `.env` with your OpenRouter API key**
```
OPENROUTER_API_KEY=your_key_here
```

**3. Run**
```bash
python main.py
```

---

## How It Differs from README Agent

| | Agent Assistant | README Agent |
|---|---|---|
| Tool registration | Manual dict | Decorator-based auto-registration |
| Tool filtering | None | Tag-based filtering |
| Architecture | Direct, simple | Full GAME framework |
| Purpose | General purpose | Specific task (write README) |
| Entry point | Interactive loop | Single task run |

The README Agent is more structured. This one is more flexible.
Both implement the same core idea: LLM + tools + memory + loop.

---

## Extending It

**Add a new tool:**

```python
# tools/my_tools.py
def my_tool(arg: str) -> str:
    """Does something useful."""
    return f"Result: {arg}"
```

```python
# tool_registry.py
from tools.my_tools import my_tool

TOOL_FUNCTIONS = {
    ...
    "my_tool": my_tool,
}

TOOLS = [
    ...
    {
        "type": "function",
        "function": {
            "name": "my_tool",
            "description": "Does something useful.",
            "parameters": {
                "type": "object",
                "properties": {
                    "arg": {"type": "string", "description": "The argument."}
                },
                "required": ["arg"]
            }
        }
    }
]
```

That's it. The agent picks it up automatically on the next run.