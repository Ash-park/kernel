"""Tests for `EchoTool`."""

from __future__ import annotations

from kernel.adapters.tools.echo_tool import EchoTool


def test_run_returns_text_argument_unchanged() -> None:
    tool = EchoTool()

    result = tool.run({"text": "hello"})

    assert result.output == "hello"
    assert result.is_error is False


def test_run_defaults_to_empty_string_when_missing() -> None:
    tool = EchoTool()

    result = tool.run({})

    assert result.output == ""
