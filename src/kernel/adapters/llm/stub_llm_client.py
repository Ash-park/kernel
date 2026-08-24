"""Deterministic `LLMClient` implementation used by tests and as the CLI's offline default."""

from __future__ import annotations

from kernel.core.models import Message, Role, ToolCall

ECHO_TRIGGER_PREFIX = "echo:"


class StubLLMClient:
    """A canned, deterministic stand-in for a real LLM provider.

    Rules (no real inference):
    - If the last message is a tool result, summarize it in the final reply.
    - If the last user message starts with "echo:", request the `echo` tool.
    - Otherwise, echo the prompt back in a fixed template.

    This keeps unit/integration tests fast and network-free (see copilot-instructions.md).
    """

    def complete(self, messages: list[Message]) -> Message:
        """Return a canned assistant `Message` based on simple rules over the last message."""
        last = messages[-1]

        if last.role is Role.TOOL and last.tool_result is not None:
            return Message(role=Role.ASSISTANT, content=f"Tool said: {last.tool_result.output}")

        if last.role is Role.USER and last.content.startswith(ECHO_TRIGGER_PREFIX):
            text = last.content[len(ECHO_TRIGGER_PREFIX) :]
            return Message(
                role=Role.ASSISTANT,
                content="",
                tool_call=ToolCall(tool_name="echo", arguments={"text": text}),
            )

        return Message(role=Role.ASSISTANT, content=f"You said: {last.content}")
