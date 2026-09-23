"""In-memory stand-in for a board service. No network or credentials."""
from __future__ import annotations

from models import Card, CardState


class MockKanbanConnector:
    def __init__(self, cards: list[Card]) -> None:
        self.cards = {card.id: card for card in cards}
        self.transitions: list[tuple[str, CardState]] = []

    def next_todo(self) -> Card | None:
        return next((card for card in self.cards.values() if card.state is CardState.TODO), None)

    def move(self, card_id: str, state: CardState, *, error: str | None = None) -> Card:
        card = self.cards[card_id]
        card.state = state
        card.error = error
        self.transitions.append((card_id, state))
        return card
