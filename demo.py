from mock_connector import MockKanbanConnector
from models import Card, ToolCall
from tool_registry import ToolRegistry
from worker import KanbanWorker


def main() -> None:
    card = Card(id="card-1", title="Prepare release note")
    connector = MockKanbanConnector([card])
    registry = ToolRegistry()

    @registry.register("add_note", "Append a reviewer-visible note", required_arguments={"text"})
    def add_note(text: str) -> dict[str, str]:
        card.notes.append(text)
        return {"saved": text}

    worker = KanbanWorker(connector, registry)
    result = worker.process_next(lambda _: [ToolCall("add_note", {"text": "Demo completed"})])

    print(result)
    print({"card_state": card.state.value, "notes": card.notes, "transitions": connector.transitions})


if __name__ == "__main__":
    main()
