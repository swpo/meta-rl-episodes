# meta-data-analysis-lite

`meta-data-analysis-lite` is a deterministic Verifiers environment for small
tabular arithmetic questions.

Each example contains a generated CSV with rows for region, product, channel,
units, returns, net units, unit price, and revenue. The model answers one
question by returning exactly one JSON object inside a `<result>...</result>`
tag:

```text
<result>{"answer": 123}</result>
```

The initial v0.1 task families are:

- total `net_units` by region
- total `revenue` by product
- filtered row counts
- highest-revenue region with deterministic tie-breaking
- product revenue differences
- average `unit_price` by channel

The reward is deterministic and shaped:

- answer correctness, including numeric closeness for arithmetic mistakes
- schema adherence for the single required `answer` key
- format credit for valid JSON inside exactly one result tag
- penalties for multiple candidates, repeated tags, code fences, or very long
  outputs

By default the environment uses no tools, no sandbox, and no judge model.
Version 0.2.1 can also run with `tools=true`, which exposes a cheap
deterministic `analyze_table(csv_text, question)` helper. The tool computes the
answer from the CSV text and exact generated question, then the model must still
finish with one `<result>...</result>` answer. This is meant to test whether
tool access improves computation without hurting final-answer coherence.

## Usage

```python
from verifiers import load_environment

env = load_environment(
    "meta-data-analysis-lite",
    seed=20260603,
    num_examples=128,
    min_rows=8,
    max_rows=12,
)
```

Tool mode:

```python
env = load_environment(
    "meta-data-analysis-lite",
    seed=20260603,
    num_examples=128,
    min_rows=8,
    max_rows=12,
    tools=True,
    max_tool_turns=3,
)
```
