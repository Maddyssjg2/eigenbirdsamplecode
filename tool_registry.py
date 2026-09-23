"""Explicit allow-list for worker actions.

The worker only receives a tool name and JSON-like arguments.  Registry owns
name lookup and argument checks, keeping connector and worker responsibilities
small and testable.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


Tool = Callable[..., Any]


class ToolError(RuntimeError):
    pass


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    required_arguments: frozenset[str]
    handler: Tool


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(
        self,
        name: str,
        description: str,
        *,
        required_arguments: set[str] | None = None,
    ) -> Callable[[Tool], Tool]:
        """Register a handler. Duplicate names fail at startup, not runtime."""
        if not name.isidentifier():
            raise ValueError("Tool names must be valid Python identifiers")

        def decorator(handler: Tool) -> Tool:
            if name in self._tools:
                raise ValueError(f"Tool already registered: {name}")
            self._tools[name] = ToolDefinition(
                name=name,
                description=description,
                required_arguments=frozenset(required_arguments or set()),
                handler=handler,
            )
            return handler

        return decorator

    def describe(self) -> list[dict[str, Any]]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "required_arguments": sorted(tool.required_arguments),
            }
            for tool in self._tools.values()
        ]

    def invoke(self, name: str, arguments: dict[str, Any]) -> Any:
        tool = self._tools.get(name)
        if tool is None:
            raise ToolError(f"Tool is not allow-listed: {name}")
        missing = tool.required_arguments.difference(arguments)
        if missing:
            raise ToolError(f"Missing arguments for {name}: {', '.join(sorted(missing))}")
        return tool.handler(**arguments)
