"""Small state machine: todo -> in_progress -> done | blocked."""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .mock_connector import MockKanbanConnector
from .models import Card, CardState, ToolCall
from .tool_registry import ToolRegistry


Planner = Callable[[Card], list[ToolCall]]


class KanbanWorker:
    def __init__(self, connector: MockKanbanConnector, registry: ToolRegistry) -> None:
        self.connector = connector
        self.registry = registry

    def process_next(self, planner: Planner) -> dict[str, Any] | None:
        """Process one card. State settles even if planning or a tool fails."""
        card = self.connector.next_todo()
        if card is None:
            return None

        self.connector.move(card.id, CardState.IN_PROGRESS)
        try:
            calls = planner(card)
            results = [self.registry.invoke(call.name, call.arguments) for call in calls]
        except Exception as exc:
            self.connector.move(card.id, CardState.BLOCKED, error=str(exc))
            return {"card_id": card.id, "state": CardState.BLOCKED.value, "error": str(exc)}

        self.connector.move(card.id, CardState.DONE)
        return {"card_id": card.id, "state": CardState.DONE.value, "tool_results": results}
