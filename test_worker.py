import unittest

from mock_connector import MockKanbanConnector
from models import Card, CardState, ToolCall
from tool_registry import ToolError, ToolRegistry
from worker import KanbanWorker


class WorkerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.card = Card(id="1", title="Example")
        self.connector = MockKanbanConnector([self.card])
        self.registry = ToolRegistry()

    def test_completes_card_and_returns_tool_result(self) -> None:
        @self.registry.register("echo", "Return supplied text", required_arguments={"text"})
        def echo(text: str) -> str:
            return text

        result = KanbanWorker(self.connector, self.registry).process_next(
            lambda _: [ToolCall("echo", {"text": "ok"})]
        )

        self.assertEqual(result, {"card_id": "1", "state": "done", "tool_results": ["ok"]})
        self.assertEqual(self.card.state, CardState.DONE)
        self.assertEqual(self.connector.transitions, [("1", CardState.IN_PROGRESS), ("1", CardState.DONE)])

    def test_blocks_card_when_tool_is_not_allow_listed(self) -> None:
        result = KanbanWorker(self.connector, self.registry).process_next(
            lambda _: [ToolCall("erase_everything")]
        )

        self.assertEqual(result["state"], "blocked")
        self.assertIn("not allow-listed", result["error"])
        self.assertEqual(self.card.state, CardState.BLOCKED)

    def test_returns_none_when_board_has_no_todo_card(self) -> None:
        self.card.state = CardState.DONE
        self.assertIsNone(KanbanWorker(self.connector, self.registry).process_next(lambda _: []))

    def test_registry_rejects_missing_required_arguments(self) -> None:
        @self.registry.register("echo", "Return supplied text", required_arguments={"text"})
        def echo(text: str) -> str:
            return text

        with self.assertRaises(ToolError):
            self.registry.invoke("echo", {})


if __name__ == "__main__":
    unittest.main()
