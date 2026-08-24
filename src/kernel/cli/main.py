"""CLI entry point and composition root: wires adapters into the core runtime.

No business logic lives here — only argument parsing and dependency wiring, per
copilot-instructions.md.
"""

from __future__ import annotations

import typer
from dotenv import load_dotenv

from kernel.adapters.events.console_event_logger import attach_console_logger
from kernel.adapters.events.in_memory_event_bus import InMemoryEventBus
from kernel.adapters.llm.ollama_llm_client import OllamaLLMClient
from kernel.adapters.llm.openai_compatible_llm_client import OpenAICompatibleLLMClient
from kernel.adapters.llm.stub_llm_client import StubLLMClient
from kernel.adapters.tools.echo_tool import EchoTool
from kernel.core.agent_runtime import AgentRuntime
from kernel.core.context_manager import ContextManager
from kernel.core.conversation import ConversationState
from kernel.core.tool_executor import ToolExecutor
from kernel.interfaces.llm_client import LLMClient
from kernel.interfaces.tool import Tool

load_dotenv()

app = typer.Typer(help="Kernel — a minimal, extensible AI agent runtime (Phase 1).")


def _build_llm_client(provider: str, model: str | None) -> LLMClient:
    """Select the concrete `LLMClient` adapter for the requested `provider`."""
    if provider == "stub":
        return StubLLMClient()
    if provider == "ollama":
        return OllamaLLMClient(model=model) if model else OllamaLLMClient(model="llama3")
    if provider == "openai":
        return OpenAICompatibleLLMClient(model=model)
    raise typer.BadParameter(f"Unknown provider: {provider}")


def _build_runtime(provider: str, model: str | None) -> AgentRuntime:
    """Compose an `AgentRuntime` from concrete adapters (the composition root)."""
    llm_client = _build_llm_client(provider, model)

    event_bus = InMemoryEventBus()
    attach_console_logger(event_bus)

    tools: dict[str, Tool] = {}
    echo_tool = EchoTool()
    tools[echo_tool.name] = echo_tool

    return AgentRuntime(
        llm_client=llm_client,
        conversation=ConversationState(),
        context_manager=ContextManager(),
        tool_executor=ToolExecutor(tools=tools, event_bus=event_bus),
        event_bus=event_bus,
    )


@app.command()
def chat(
    prompt: str = typer.Argument(..., help="The prompt to send to the agent."),
    provider: str = typer.Option(
        "stub",
        "--provider",
        help="LLM provider: 'stub' (offline, default), 'ollama', or 'openai' "
        "(any OpenAI-compatible endpoint, configured via KERNEL_LLM_* env vars / .env).",
    ),
    model: str = typer.Option(
        None,
        "--model",
        help="Model name override for 'ollama'/'openai' providers.",
    ),
) -> None:
    """Send a single prompt to the agent and print its reply."""
    runtime = _build_runtime(provider, model)
    reply = runtime.handle_turn(prompt)
    typer.echo(reply.content)


if __name__ == "__main__":
    app()
