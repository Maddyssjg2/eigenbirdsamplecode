from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CardState(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"


@dataclass
class Card:
    id: str
    title: str
    description: str = ""
    state: CardState = CardState.TODO
    notes: list[str] = field(default_factory=list)
    error: str | None = None


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any] = field(default_factory=dict)
