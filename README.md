# AI Agents From Scratch

Three autonomous AI agents built **without frameworks** like LangChain or CrewAI.

Every component — the agent loop, tool registry, memory, and environment — is
implemented manually in pure Python. The goal was to understand how agents actually
work before reaching for abstractions.

---

## Why AI Agents?

Traditional software follows predefined instructions.

AI agents introduce a different paradigm: instead of hardcoding every step, we provide goals, tools, memory, and an environment, allowing the system to decide how to achieve an objective.

The real power of AI agents isn't automation—it's adaptability. They allow software to move beyond rigid workflows and make decisions based on goals, context, and available tools.

---

## Agents

### 1. README Agent (`readme_agent/`)

An agent that reads an entire Python project and writes its own `README.md`.

**Architecture:** GAME framework (Goals, Actions, Memory, Environment) with a
decorator-based `ActionRegistry` that auto-registers tools from type hints and
docstrings. Tools are filtered by tags so the agent only sees what it needs.

**The README you're reading in that folder? The agent wrote it.**

**Key concepts demonstrated:**
- Decorator-based tool registration with JSON schema generation
- Tag-based tool filtering
- Full GAME loop implementation
- Terminal action pattern (agent decides when it's done)

---

### 2. Agent Assistant (`agent_assistant/`)

A general-purpose conversational agent that can explore and read files on demand.

**Architecture:** Simpler, more direct. Tool registry is a plain dict. The agent
loop handles multi-turn conversation, parallel tool calls, and memory across turns.

**Key concepts demonstrated:**
- OpenAI-style tool calling protocol (`tool_calls` + `tool` role messages)
- Multi-turn memory with full conversation history
- Parallel tool call handling
- Clean separation: `TOOLS` (LLM schema) vs `TOOL_FUNCTIONS` (Python callables)

---

### 3. Multi Agents (`Multi_Agents/`)

A lightweight multi-agent orchestrator that routes user requests to specialized agents.

**Architecture:** A top-level orchestrator delegates to a question generator agent,
which can then use registered tools to generate and validate multiple-choice questions.

**Key concepts demonstrated:**
- Multi-agent orchestration
- Agent registration and routing
- Tool-backed question generation and validation
- Simple terminal-based workflow with OpenRouter

---

## What I Learned

Building agents without frameworks forces you to understand:

**The agent loop** — it's just: call LLM → parse response → if tool call, execute
it and add result to memory → repeat. Frameworks hide this but it's only ~50 lines.

**Memory is just a list** — conversation history is a list of dicts with `role` and
`content`. The LLM has no memory of its own — you pass everything every time.

**Tool calling is a protocol** — the LLM returns a structured JSON object saying
which function to call with which arguments. Your code executes it and returns the
result. The LLM never runs code directly.

**Termination is explicit** — the agent doesn't know when to stop unless you give
it a terminate tool and tell it to call it when done.

---

## Structure

```
ai-agents-from-scratch/
│
├── readme_agent/               # Agent 1 — writes README files
│   ├── action.py               # Action dataclass
│   ├── action_registery.py     # Registry with decorator + tag filtering
│   ├── agent.py                # Core GAME loop
│   ├── decorators.py           # @register_tool decorator
│   ├── environment.py          # Executes actions, returns structured results
│   ├── llm.py                  # LLM client (litellm + OpenRouter)
│   ├── memory.py               # Conversation history
│   ├── tools.py                # list_files, read_file, write_file, terminate
│   ├── main.py                 # Entry point
│   └── README.md               # Written by the agent itself
│
├── agent_assistant/            # Agent 2 — general purpose file assistant
│   ├── agent.py                # Agent loop with multi-turn + tool handling
│   ├── memory.py               # Conversation history
│   ├── tool_registry.py        # TOOLS (LLM schema) + TOOL_FUNCTIONS (callables)
│   ├── tools/
│   │   ├── file_tools.py       # list_files, read_file
│   │   ├── utility_tools.py    # terminate
│   │   └── search_tools.py     # (extensible)
│   ├── Prompts.py              # System prompt
│   ├── main.py                 # Entry point with interactive loop
│   └── test_memory.py          # Memory unit tests
│
├── Multi_Agents/               # Agent 3 — multi-agent question workflow
│   ├── agents/                 # Orchestrator and question generator agents
│   ├── registery/              # Agent and tool registries/decorators
│   ├── tools/                  # Question generation tools
│   ├── llm.py                  # OpenRouter adapter
│   ├── main.py                 # Terminal entry point
│   └── README.md               # Project-specific documentation
│
└── README.md                   # This file
```

---

## Setup

Both agents use [OpenRouter](https://openrouter.ai) for LLM access.

**1. Install dependencies**

For README Agent:
```bash
cd readme_agent
pip install litellm python-dotenv
```

For Agent Assistant:
```bash
cd agent_assistant
pip install -r requirements.txt
```

For Multi Agents:
```bash
cd Multi_Agents
pip install -r requirements.txt
```

**2. Set your API key**

Create a `.env` file in each agent's directory:
```
OPENROUTER_API_KEY=your_key_here
```

**3. Run**

README Agent:
```bash
cd readme_agent
python main.py
```

Agent Assistant:
```bash
cd agent_assistant
python main.py
```

Multi Agents:
```bash
cd Multi_Agents
python main.py
```

---

## Running with Docker

Build and start the containers:

```bash
docker compose up --build
```

Run a specific agent:

```bash
docker compose run readme-agent
```

```bash
docker compose run agent-assistant
```

```bash
docker compose run multi-agents
```
---

## Why No Frameworks?

LangChain and CrewAI are useful but they hide the mechanics. When something breaks
or you need to customize behavior, you need to understand what's happening underneath.

Building from scratch first means:
- You understand what a "chain" actually is (just function calls)
- You understand what an "agent" actually is (just a loop)
- You can debug anything because you wrote everything
- Frameworks become tools you choose, not black boxes you depend on

---

## What's Next

- Connect these agents into a **multi-agent system** where agents delegate tasks
  to each other
- Integrate agents into [Quizey V2](https://github.com/alaabadawii/Quizey_V2) —
  a Flask quiz platform — to generate exams, provide feedback, and assist grading
