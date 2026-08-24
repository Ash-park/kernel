## `kernel/cli/main.py`

The Typer CLI entry point and **composition root**. The `chat` command parses arguments
and delegates entirely to `AgentRuntime`; `_build_runtime` wires concrete adapters
(`StubLLMClient`/`OllamaLLMClient`, `InMemoryEventBus`, `EchoTool`) into `core/` via
constructor injection. No business logic lives here.

```mermaid
flowchart TD
    User -->|kernel chat "..." --provider ...| Typer[Typer app]
    Typer --> chat[chat command]
    chat -->|_build_runtime| Composition[composition root]
    Composition --> StubLLMClient
    Composition --> OllamaLLMClient
    Composition --> OpenAICompatibleLLMClient
    Composition --> InMemoryEventBus
    Composition --> EchoTool
    Composition --> AgentRuntime
    chat -->|handle_turn prompt| AgentRuntime
    AgentRuntime -->|reply| chat
    chat -->|prints| User
```

**Inputs:** command-line invocation (`kernel chat <prompt> [--provider stub|ollama|openai] [--model NAME]`).
**Outputs:** printed assistant reply to stdout; event log lines to stderr.
**Depends on:** every `adapters/*` module and `core.agent_runtime.AgentRuntime`,
`core.conversation.ConversationState`, `core.context_manager.ContextManager`,
`core.tool_executor.ToolExecutor`, `interfaces.llm_client.LLMClient`, `interfaces.tool.Tool`,
`python-dotenv` (loads `.env` for `KERNEL_LLM_*` config before adapters are constructed).
