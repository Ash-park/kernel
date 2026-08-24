"""Real `LLMClient` implementation backed by any OpenAI-compatible chat completions API.

Configuration is read from environment variables (never hardcoded), matching the
`LLM-agnostic` principle in copilot-instructions.md:

- `KERNEL_LLM_BASE_URL` — e.g. http://localhost:18011/v1
- `KERNEL_LLM_API_KEY`  — bearer token for the endpoint
- `KERNEL_LLM_MODEL`    — model name, e.g. qwen2.5-7b

See `.env.example` for a template; real values belong in a local, gitignored `.env`.
"""

from __future__ import annotations

import os

from openai import OpenAI

from kernel.core.models import Message, Role


class OpenAICompatibleLLMClient:
    """Calls any OpenAI-compatible `/chat/completions` endpoint via the `openai` SDK.

    Used for locally hosted models (e.g. vLLM, LM Studio, or a tunneled local server)
    that expose the OpenAI chat completions API shape.
    """

    def __init__(
        self,
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> None:
        self._model = model or os.environ["KERNEL_LLM_MODEL"]
        self._client = OpenAI(
            base_url=base_url or os.environ["KERNEL_LLM_BASE_URL"],
            api_key=api_key or os.environ["KERNEL_LLM_API_KEY"],
        )

    def complete(self, messages: list[Message]) -> Message:
        """Send `messages` to the configured endpoint and return the assistant's reply."""
        payload = [{"role": message.role.value, "content": message.content} for message in messages]
        response = self._client.chat.completions.create(model=self._model, messages=payload)
        content = response.choices[0].message.content or ""
        return Message(role=Role.ASSISTANT, content=content)
