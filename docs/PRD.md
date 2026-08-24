# Product Requirements Document — Kernel

## 1. Problem / Motivation

Most public "AI agent" projects are thin wrappers around an LLM API or a single framework (LangChain-style
chains, ChatPDF clones, MCP-only clients). They don't demonstrate platform engineering: extensibility,
observability, or clean architecture under a changing set of capabilities.

**Kernel** is an open-source AI Agent Platform built to demonstrate senior-level system design: a runtime that
never changes when new capabilities (plugins, tools, connectors, retrieval, memory) are added.

## 2. Goals

- Ship a working product at the end of every phase (see [idea.md](../idea.md) for the 8-phase roadmap).
- Demonstrate clean architecture, event-driven design, and provider-agnostic abstractions.
- Be resume-grade: a project a principal/staff engineer would recognize as well-designed, not a toy.

## 3. Non-Goals (for now)

- Not a chatbot product, not a LangChain wrapper, not an MCP-only client.
- No plugin system, RAG, memory, multi-agent orchestration, or web UI until their respective phases.
- No enterprise connectors (GitHub/Jira/Confluence) until Phase 3.

## 4. Target Users

AI engineers, developer productivity teams, platform engineers, enterprise AI teams, and developers who want
to build custom agents on a stable runtime.

## 5. Scope of Phase 1

**In scope:** CLI, LLM client interface (+ one real local-LLM adapter and one stub adapter for tests),
conversation state, context manager (window/pruning), tool execution loop (with one example tool), event bus
(with a console subscriber for visibility).

**Out of scope:** plugin discovery/lifecycle, any enterprise connector, retrieval/RAG, persistent memory,
multi-agent orchestration, REST API / web UI.

## 6. Success Criteria (Phase 1)

- A user can run a CLI command, send a prompt, and get a response from a locally running LLM (or a stub in
  test mode).
- The agent can invoke at least one tool mid-conversation and incorporate the tool result into its response.
- Every significant action (agent started, prompt received, tool started/completed, LLM response generated)
  is emitted as an event and observable (printed to console in Phase 1; replaced by real tracing in Phase 6).
- `core/` has zero dependency on any concrete adapter or third-party SDK; this is enforced by import
  direction and covered by unit tests that run without network/filesystem/LLM access.
- `black` and `ruff` pass with zero warnings; `pytest` passes with coverage of every acceptance criterion.

## 7. Risks

- Over-building Phase 1 (e.g., sneaking in plugin discovery) — mitigated by explicit non-goals above and by
  copilot-instructions.md workflow discipline rules.
- Local LLM adapter (e.g., Ollama) may not be installed on every dev machine — mitigated by a stub LLM
  client used by default in tests and as a fallback.

## 8. Reference Material

Architectural inspiration only (no code/API copying) — see [references.md](../references.md). Phase 1 draws
primarily from Orion-Core (runtime/context/tool-loop/event-streaming/LLM abstraction) and GitHub CLI (CLI UX).
