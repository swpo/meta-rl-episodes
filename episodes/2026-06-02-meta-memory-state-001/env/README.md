# meta-memory-state

`meta-memory-state` is a small deterministic Verifiers environment for testing
multi-turn state tracking.

Each example gives a pocket ledger with signed balances across a small set of
accounts. The model receives 2-5 debit, credit, or transfer updates across user
turns and must reply after each update with the full ledger inside a
`<ledger>...</ledger>` JSON block.

The recommended first smoke uses only two accounts and one to two turns. Harder
multi-turn settings are available through `min_turns`, `max_turns`, and
`account_count` once the smoke shows useful reward variance.

The reward is shaped and defensive:

- per-account balance correctness
- total correctness
- schema adherence, including penalties for hallucinated accounts and extra
  keys inside `balances`
- format credit for one valid tagged JSON block
- anti-stuffing penalty for multiple ledger candidates, repeated tags, long
  outputs, or code fences
- malformed, empty, or `None` outputs return low reward instead of raising

The environment also reports auxiliary metrics for parseability, exact one-ledger
format adherence, multiple-candidate outputs, code fences, candidate count, and
mean assistant output length. These metrics are intended for diagnosing reward
hacking without making held-out evals optimize a different objective.

The environment uses no tools, no sandbox, and no judge model.

## Usage

```python
from verifiers import load_environment

env = load_environment(
    "meta-memory-state",
    seed=1337420,
    num_examples=128,
    min_turns=1,
    max_turns=2,
    account_count=2,
)
```
