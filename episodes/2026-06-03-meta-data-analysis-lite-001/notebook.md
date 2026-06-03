# Episode Notebook: 2026-06-03-meta-data-analysis-lite-001

## Question

Can a small model learn reliable tabular arithmetic over generated CSVs using a
cheap deterministic reward, and where does the task become difficult enough to
produce useful RL dynamics?

This episode is intentionally not yet a sandbox/tool-use episode. v0.1 starts
with no tools so we can separate basic arithmetic, aggregation, parsing, and
reward-design effects from sandbox runtime/cost. A later version can add a tool
path over the same table generator.

## Environment

- Env: `meta-data-analysis-lite`
- Version/source: local v0.1.0 candidate
- Local path or Hub URL: `episodes/2026-06-03-meta-data-analysis-lite-001/env`
- Key args: `seed`, `num_examples`, `min_rows`, `max_rows`, `task_families`
- Reward signal: shaped deterministic score for one `<result>{"answer": ...}</result>` response
- Parser assumptions: score the selected final candidate, penalize multiple candidates and code fences
- Tooling: none in v0.1.0

## Hypotheses

1. Llama 1B may learn the result-tag/schema behavior quickly but struggle with
   aggregation as rows/task mix scale.
2. Reward should expose separate curves for format compliance, exact answer
   rate, and numeric closeness; a reward increase without exact-answer movement
   would indicate mostly formatting or near-miss learning.
3. Row count and task-family mix should give a more interpretable difficulty
   ladder than model scaling alone.

## Planned Difficulty Ladder

| Rung | Rows | Task Mix | Expected Use |
| --- | ---: | --- | --- |
| v0.1-easy | 6-8 | sum/count only | integration smoke and base eval |
| v0.1-mixed | 8-12 | all families | first non-trivial RL probe |
| v0.1-hard | 14-20 | all families | push smallest model toward failure |
| v0.2-tool | TBD | same generator with sandbox/tool path | test tool benefit/coherence |

## Smoke Tests

### Local Unit Tests

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest episodes/2026-06-03-meta-data-analysis-lite-001/env/test_meta_data_analysis_lite.py
```

Result:

- Status: passed
- Result: 15 tests passed in 0.02s
- Notes: deterministic generation, all task-family generation, exact numeric and string scoring, malformed-output handling, partial numeric credit, format/schema penalties, candidate-stuffing penalties, hosted-style answer signature, object-style messages, and diagnostics.

## Eval Matrix

Use the same reward/objective for base and trained evals. Record auxiliary
metrics separately when they explain what the reward is doing.

| Eval | Model | Seed/Split | Examples | Reward | Truncation | Aux Metrics | Notes |
| --- | --- | --- | ---: | --- | ---: | --- | --- |

## Runs

| Run | Model | Steps | Max Tokens | Status | Cost | Reward Read | Notes |
| --- | --- | ---: | ---: | --- | ---: | --- | --- |

## Observations

- Local tests passed on the first scaffold.
- A sample generated prompt is compact enough for Llama 1B and uses a plain CSV,
  one question, and one required result shape.
- No hosted eval or RL run has been launched yet.

## Failure Modes

- Parser/reward errors: watch for multiple JSON objects or code-fenced JSON.
- Truncation: unlikely in no-tool v0.1, but verbose reasoning may become an issue.
- Empty or malformed outputs: should score zero rather than raise.
- Zero-advantage filtering: possible on easy format-only rungs; use mixed tasks for variance.
- Tool-use issues: not applicable until a later sandbox/tool version.
- Cost/runtime surprises: expected cheap; no judge or sandbox in v0.1.
- Platform/client issues: none observed yet.

## Interpretation

This environment is meant to complement `meta-memory-state`: instead of
multi-turn state tracking, it tests single-turn computation over tabular
evidence with exact grading and difficulty knobs.

## Next Steps

1. Push `meta-data-analysis-lite@0.1.0` to Prime Hub.
2. Run base evals on easy and mixed rungs before the first hosted RL smoke.
3. Use the mixed rung for the first 1-step Llama 1B hosted smoke if evals are clean.
