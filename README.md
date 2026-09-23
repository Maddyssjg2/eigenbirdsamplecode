# Eigenbird sample: kanban worker + tool registry

Small, dependency-free Python sample. Reviewer can read core in a few minutes.

It shows one narrow design:

```text
mock board -> worker state machine -> allow-listed tools -> mock board
```

It is **not** a copy of, or guide to, full Eigenbird product flow. No production connectors, credentials, prompts, routing, persistence, API endpoints, or deployment configuration included.

## What to read

1. [`kanban_sample/worker.py`](kanban_sample/worker.py) — deterministic card lifecycle: `todo -> in_progress -> done | blocked`.
2. [`kanban_sample/tool_registry.py`](kanban_sample/tool_registry.py) — explicit tool allow-list and required-argument guard.
3. [`kanban_sample/mock_connector.py`](kanban_sample/mock_connector.py) — in-memory board adapter, zero network calls.
4. [`demo.py`](demo.py) — one-card happy-path demo.
5. [`tests/test_worker.py`](tests/test_worker.py) — completion, block, empty-board, and argument-validation behavior.

## Run

Requires Python 3.11+. No install or environment variables needed.

```bash
python demo.py
python -m unittest discover -s tests -v
```

Expected demo shape:

```text
{'card_id': 'card-1', 'state': 'done', 'tool_results': [{'saved': 'Demo completed'}]}
{'card_state': 'done', 'notes': ['Demo completed'], 'transitions': [('card-1', <CardState.IN_PROGRESS: 'in_progress'>), ('card-1', <CardState.DONE: 'done'>)]}
```

## Why these boundaries

| Part | Owns | Does not own |
| --- | --- | --- |
| Worker | One-card lifecycle; success/failure settling | Network access; tool policy |
| Registry | Tool allow-list; required input checks; dispatch | Picking cards; state transitions |
| Connector | Card lookup; state updates; transition log | Business actions |
| Demo planner | Explicit `ToolCall` list | Model use, background loop, hidden side effects |

Keeping these roles separate makes failure behavior visible and unit-testable. A tool error becomes a `blocked` card with the error text; it cannot leave a card in `in_progress`.

## Security and sharing posture

- Uses Python standard library only; mock connector never opens network connections.
- `.env` and `.env.*` ignored. No environment values read.
- Tool dispatch is allow-listed: unknown tools and missing required inputs fail closed.
- Repo intentionally contains synthetic card IDs and demo text only.

Before sharing, run the tests above and inspect `git status --ignored` to ensure no local files are staged. This sample is MIT-licensed.
