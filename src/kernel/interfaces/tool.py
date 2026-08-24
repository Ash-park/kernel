"""Abstract contract for tools that an agent can invoke."""

from __future__ import annotations

from abc import ABC, abstractmethod

from kernel.core.models import ToolResult


class Tool(ABC):
    """A single callable capability the agent runtime can execute mid-conversation.

    Phase 1 registers tools manually (see `cli/main.py`); dynamic discovery is a Phase 2
    concern and must not be added here.
    """

    name: str
    description: str

    @abstractmethod
    def run(self, arguments: dict[str, object]) -> ToolResult:
        """Execute the tool with the given arguments and return its result."""
        raise NotImplementedError
