"""A minimal example `Tool` that proves the tool-execution loop end-to-end."""

from __future__ import annotations

from kernel.core.models import ToolResult
from kernel.interfaces.tool import Tool


class EchoTool(Tool):
    """Returns the `text` argument it was given, unchanged.

    Deliberately trivial: Phase 1's goal is to prove the agent-runtime <-> tool round
    trip works, not to ship a useful tool (real tools arrive with plugins in Phase 2).
    """

    name = "echo"
    description = "Echoes back the given 'text' argument."

    def run(self, arguments: dict[str, object]) -> ToolResult:
        """Return a `ToolResult` containing `arguments['text']` verbatim."""
        text = str(arguments.get("text", ""))
        return ToolResult(tool_name=self.name, output=text)
