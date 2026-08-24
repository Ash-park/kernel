# Kernel

An extensible, event-driven AI Agent Platform — clean-architecture agent runtime built
incrementally in phases. **Phase 1** (current): CLI, LLM-agnostic client, conversation
state, context manager, tool execution loop, event bus.

Not a chatbot, not a LangChain wrapper, not an MCP-only client — see [idea.md](idea.md) for
the full vision and 8-phase roadmap, and [references.md](references.md) for architectural
inspiration (studied, never copied).

## Docs

- [docs/PRD.md](docs/PRD.md) — problem, goals, non-goals, success criteria
- [docs/HLD.md](docs/HLD.md) — system architecture
- [docs/phase-1/LLD.md](docs/phase-1/LLD.md) — Phase 1 low-level design
- [mermaids/](mermaids/) — one module-level diagram per source file, mirroring `src/`
- [.github/copilot-instructions.md](.github/copilot-instructions.md) — coding standards enforced in this repo

## Setup

```powershell
python -m venv .venv
.venv\Scripts\pip install -e ".[dev]"
```

## Usage

```powershell
# Offline, deterministic (default) — no LLM required
kernel chat "hello"

# Trigger the example tool round-trip (stub convention)
kernel chat "echo:hello world"

# Real local LLM via Ollama
kernel chat "hello" --provider ollama --model llama3

# Any OpenAI-compatible endpoint (configure KERNEL_LLM_* in a local .env — see .env.example)
kernel chat "hello" --provider openai
```

## Development

```powershell
.venv\Scripts\python -m pytest -q          # tests
.venv\Scripts\python -m ruff check .       # lint
.venv\Scripts\python -m black --check .    # format check
```

## License

MIT
