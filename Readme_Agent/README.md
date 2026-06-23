# Agentic README Generator

## Why I Built This

This project was built as a learning exercise to understand 
AI Agents from the ground up, without using frameworks like 
LangChain or CrewAI.

Every component — Action, ActionRegistry, Memory, Environment, 
and the agent loop — was implemented manually following the 
GAME framework (Goals, Actions, Memory, Environment).

The agent itself then wrote this README.

This project implements an **autonomous AI agent** that can read, understand, and generate documentation for Python projects. It uses an LLM (via OpenRouter) to reason about the codebase and produce a `README.md` file.

## How It Works

1. The agent is given a user prompt (e.g., "write a README.md file for this project.")
2. It lists all Python files in the current directory.
3. It reads each file to understand the project structure and logic.
4. It generates a comprehensive `README.md` file.
5. It calls the `terminate` action to end execution.

## Architecture

The project is composed of the following modules:

### `action.py`
Defines the `Action` class, which encapsulates a callable function with metadata:
- `name`: action identifier
- `function`: the underlying Python function
- `description`: human-readable description
- `parameters`: JSON schema for expected arguments
- `terminate`: boolean flag indicating if this action ends the agent loop

### `action_registery.py`
Implements `ActionRegistry`, which collects all registered tools (optionally filtered by tags) and wraps them into `Action` objects. It provides methods to retrieve actions by name or list all available actions.

### `agent.py`
Contains the `Agent` class, the core loop:
- Maintains conversation memory (user, assistant, tool messages).
- Builds a system prompt with available actions.
- Sends the prompt to the LLM and parses the JSON response.
- Executes the chosen action with provided arguments.
- Stores results back into memory.
- Continues until a terminal action is executed.

### `decorators.py`
Provides the `@register_tool` decorator, which:
- Extracts function name, docstring, and type hints.
- Builds a JSON schema for parameters.
- Registers the function in `_tools` and optionally in `_tools_by_tag`.
- Supports marking a tool as terminal.

### `environment.py`
Defines `Environment`, which executes an `Action` and returns a structured result (success or error with traceback).

### `llm.py`
Configures the LLM client using `litellm` with OpenRouter. Loads the API key from a `.env` file and sends messages to the model.

### `main.py`
Entry point that:
- Creates an `ActionRegistry` filtered by the `"file_operations"` tag.
- Manually adds the `terminate` action.
- Instantiates `Memory`, `Environment`, and `Agent`.
- Runs the agent with the user prompt.

### `memory.py`
Implements `Memory`, a simple list-based store for conversation history. Supports adding, retrieving, and clearing messages.

### `tools.py`
Defines the actual tools the agent can use:
- `list_files()` – returns sorted list of `.py` files in the current directory.
- `read_file_content(name)` – reads and returns the content of a file.
- `write_file_content(name, content)` – writes content to a file.
- `terminate(message)` – ends the agent execution.

## Setup

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install python-dotenv litellm
   ```
3. Create a `.env` file with your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_key_here
   ```
4. Run the agent:
   ```bash
   python main.py
   ```

## Usage

The agent is designed to generate a `README.md` for any Python project. Simply run `main.py` and the agent will:
- List all Python files.
- Read each file.
- Understand the project.
- Generate and save a `README.md`.
- Terminate.

## Customization

- **Tags**: You can filter which tools are available to the agent by passing a list of tags to `ActionRegistry`.
- **LLM Model**: Change the model in `llm.py` to any model supported by OpenRouter.
- **New Tools**: Add new functions decorated with `@register_tool` in `tools.py` to extend the agent's capabilities.

## License

MIT