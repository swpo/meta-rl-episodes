# Track: Multi-Turn State

## Objective

Build a `meta-` environment that tests whether a model can maintain state across
several turns and update its answer as new facts arrive.

## Environment Shape

Examples:

- Maintain a small inventory, ledger, schedule, or set of constraints.
- Apply updates over 2-5 turns.
- Final answer depends on all turns, not only the latest prompt.

## Reward Ideas

- Exact final state.
- Partial credit for each correctly tracked item.
- Format compliance.
- Optional penalty for hallucinated state entries.

## Cost Notes

This should be cheap: deterministic scoring, no judge, no sandbox. Token cost
comes mostly from longer conversations.

## Initial Smoke Plan

- Llama 1B, 1 step, `max_tokens=512`.
- Increase turn count only after reward variance looks useful.

## Collision Avoidance

Differentiate from alphabet-sort by using richer state updates rather than only
sorted accumulated lists.
