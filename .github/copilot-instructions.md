# Copilot Instructions — Kernel (AI Agent Platform)

## Project Context

This is a phased, resume-grade open-source AI Agent Platform (see [idea.md](../idea.md) and [references.md](../references.md)).
Language: **Python**. Currently building **Phase 1 only** (minimal agent runtime: CLI, LLM interface,
conversation state, context manager, tool execution loop, event bus). Do not add functionality belonging
to later phases (plugins, RAG, memory, multi-agent, web UI, enterprise connectors) unless explicitly asked.

## Architecture Rules

1. **Runtime first** — the core runtime must never depend on a specific plugin, LLM provider, or tool. Depend
   on abstractions (interfaces/protocols), not concrete implementations.
2. **Clean architecture / modular boundaries** — organize by layer:
   - `core/` — domain logic, orchestration, no I/O, no third-party SDKs.
   - `interfaces/` (or `ports/`) — abstract base classes / `Protocol`s (LLM client, tool, event sink, etc.).
   - `adapters/` (or `infra/`) — concrete implementations of interfaces (e.g., Ollama client, SQLite store).
   - `cli/` — entry points only; no business logic.
   - Never let `core/` import from `adapters/` or `cli/`.
3. **Event-driven** — significant actions (agent started, prompt received, tool started/completed, LLM
   response generated, errors) must emit events through the event bus, not ad-hoc logging.
4. **LLM-agnostic** — all LLM calls go through the `LLMClient` interface. Never call a provider SDK directly
   from `core/`.
5. **Small, composable units** — one class/function = one responsibility. Prefer composition over inheritance.
6. **No premature abstraction** — do not build plugin systems, registries, or config layers before Phase 1
   requires them. Build the smallest thing that satisfies the current phase's acceptance criteria.

## Code Standards

- Python 3.11+, full type hints on all public functions/methods (`from __future__ import annotations` where useful).
- Use `Protocol` / `abc.ABC` for interfaces, not duck-typing without a contract.
- Formatting: `black` (line length 100). Linting: `ruff`. Both must pass with zero warnings before a change is
  considered done.
- Docstrings (Google style) required on all public modules, classes, and functions — one-line summary minimum.
- Naming: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants.
- No bare `except:`; catch specific exceptions and re-raise with context when appropriate.
- No global mutable state; pass dependencies explicitly (constructor injection).
- Every new module must include a corresponding test module under `tests/` mirroring its path
  (e.g., `src/kernel/core/context.py` → `tests/core/test_context.py`).
- Prefer `dataclasses` / `pydantic` models for structured data over dicts.
- Keep functions short (~40 lines guideline); extract helpers instead of nesting deeply.

## Mermaid Diagram Convention

Every source file under `src/` must have a companion **module-level** Mermaid diagram describing:
- What the file/module is responsible for.
- Its public inputs (what calls into it) and outputs (what it calls/returns/emits).
- Which other modules/files it directly interacts with (imports, events, calls).

Do **not** diagram internal function-by-function control flow — module-level relationships only.

Rules:
1. Diagrams live under `mermaids/`, mirroring the `src/` folder structure 1:1.
   - `src/kernel/core/agent_runtime.py` → `mermaids/kernel/core/agent_runtime.md`
2. Each diagram file contains one ` ```mermaid ` fenced block (prefer `flowchart TD` or `classDiagram`,
   whichever best communicates the relationship) plus a short paragraph explaining the file's role.
3. When a source file is created, its diagram must be created in the same change.
4. When a source file's responsibilities or dependencies change, its diagram must be updated in the same change.
5. Never let a diagram go stale — if unsure whether an edit changes the file's role/relationships, update the diagram.

## Testing

- `pytest` for all tests. Every phase's acceptance criteria must be covered by at least one test.
- Unit tests for `core/` logic must not require network/filesystem/LLM access — mock the interfaces.
- Integration tests (if any) live under `tests/integration/` and are allowed to hit local adapters (e.g., local LLM).

## Workflow Discipline

- Only implement the current phase. Future phases stay as placeholders/notes.
- Any new architectural decision that deviates from idea.md/references.md must be called out explicitly, not
  silently introduced.
- Do not copy code or replicate APIs from the reference projects in references.md — architectural inspiration only.
