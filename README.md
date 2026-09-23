# Eigenbird Kanban Worker Sample

Small Python example for processing a kanban card through an allow-listed set of tools. It runs with the Python standard library only.

```text
mock board -> kanban worker -> tool registry -> mock board
```

## Files

- [`worker.py`](worker.py) moves one card through `todo`, `in_progress`, `done`, or `blocked`.
- [`tool_registry.py`](tool_registry.py) registers named tools and validates required arguments.
- [`mock_connector.py`](mock_connector.py) provides an in-memory board with no network access.
- [`demo.py`](demo.py) runs one card from start to finish.
- [`test_worker.py`](test_worker.py) covers normal completion, blocked cards, empty boards, and missing arguments.

## Run

Python 3.11 or newer is required. No installation or environment variables are needed.

```bash
python demo.py
python -m unittest -v test_worker
```

Example output:

```text
{'card_id': 'card-1', 'state': 'done', 'tool_results': [{'saved': 'Demo completed'}]}
{'card_state': 'done', 'notes': ['Demo completed']}
```

## Card flow

| Component | Responsibility |
| --- | --- |
| Worker | Picks one todo card and settles its final state |
| Registry | Allows registered tools and validates inputs |
| Connector | Stores cards and transition history in memory |
| Demo | Supplies one explicit tool call |

Tool errors set the card state to `blocked` and include the error message.

## Scope

This repository uses synthetic data only. It does not include production connectors, credentials, prompts, routing, persistence, API endpoints, or deployment configuration.

MIT licensed.
