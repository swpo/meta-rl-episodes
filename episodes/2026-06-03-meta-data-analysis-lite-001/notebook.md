# Episode Notebook: 2026-06-03-meta-data-analysis-lite-001

## Question

Can a small model learn reliable tabular arithmetic over generated CSVs using a
cheap deterministic reward, and where does the task become difficult enough to
produce useful RL dynamics?

This episode intentionally starts without tools or a sandbox. The goal is to
separate arithmetic, aggregation, parsing, and reward-design effects from
runtime/tool costs. A later version can add tool access over the same table
generator.

## Environment

- Env: `abugoot/meta-data-analysis-lite`
- Version: `0.1.1`
- Prime Hub: https://app.primeintellect.ai/dashboard/environments/abugoot/meta-data-analysis-lite
- Local path: `episodes/2026-06-03-meta-data-analysis-lite-001/env`
- Key args: `seed`, `num_examples`, `min_rows`, `max_rows`, `task_families`
- Reward signal: shaped deterministic score for one `<result>{"answer": ...}</result>` response
- Parser assumptions: score the selected final candidate, penalize multiple candidates and code fences
- Tooling: none in v0.1.1

Task families:

- `sum_units_by_region`
- `sum_revenue_by_product`
- `count_rows_filter`
- `max_region_revenue`
- `diff_product_revenue`
- `avg_unit_price_by_channel`

## Hypotheses

1. Llama 1B can learn result-tag/schema behavior quickly but should struggle
   with aggregation as rows/task mix scale.
2. Reward should expose separate curves for format compliance, exact answer
   rate, and numeric closeness; a reward increase without exact-answer movement
   would indicate mostly formatting or near-miss learning.
3. Row count and task-family mix should give a more interpretable difficulty
   ladder than model scaling alone.

## Difficulty Ladder

| Rung | Rows | Task Mix | Expected Use |
| --- | ---: | --- | --- |
| v0.1-easy | 6-8 | sum/count only | integration smoke and base eval |
| v0.1-mixed | 8-12 | all families | first non-trivial RL probe |
| v0.1-hard | 14-20 | all families | push smallest model toward failure |
| v0.2-tool | TBD | same generator with tool path | test tool benefit/coherence |

## Local And Hub Checks

Local unit test command:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest episodes/2026-06-03-meta-data-analysis-lite-001/env/test_meta_data_analysis_lite.py
```

Result:

- `15 passed, 1 skipped` locally for v0.1.1.
- The skipped test is the optional `datasets` Arrow compatibility test because
  the local Python environment does not include `datasets`.
- The same Arrow compatibility check passed under the Prime CLI Python runtime.

Hub integration:

- v0.1.0 pushed successfully as `abugoot/meta-data-analysis-lite@0.1.0`;
  content hash prefix `12bf0e1e`.
- v0.1.0 easy numeric eval completed, but mixed-task eval failed during dataset
  construction because `info.answer` and `info.target` mixed numeric,
  string, and dict shapes across examples.
- v0.1.1 fixes this by storing heterogeneous metadata as JSON strings while
  keeping the hidden answer payload unchanged.
- v0.1.1 pushed successfully as `abugoot/meta-data-analysis-lite@0.1.1`;
  content hash prefix `755796fa`, wheel SHA
  `ca04d3cf7522bcf5bf14b5199a868e30bd3b7c1836302393be937bae110ff12a`.

## Eval Matrix

All evals use 16 examples, 1 rollout/example, temperature `0.7`, and
`max_tokens=512`.

| Eval | Model | Seed/Split | Rows / Tasks | Reward | Parseable | Exact One Result | Exact Answer | Answer Score | Output Tokens | Notes |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| base-easy-v011 | `meta-llama/Llama-3.2-1B-Instruct` | `20260603` train seed | 6-8 / sum+count | `0.0567` | `0.250` | `0.000` | `0.000` | `0.0156` | `18.0` | Official easy baseline after v0.1.1 fix. |
| base-mixed-v011 | `meta-llama/Llama-3.2-1B-Instruct` | `20260603` train seed | 8-12 / all | `0.0225` | `0.125` | `0.000` | `0.000` | `0.0000` | `20.0` | Mixed baseline is near-zero and not parseable enough. |
| base-heldout-v011 | `meta-llama/Llama-3.2-1B-Instruct` | `424242` held-out seed | 8-12 / all | `0.0113` | `0.0625` | `0.000` | `0.000` | `0.0000` | `34.9` | Held-out baseline is also near-zero. |
| trained-mixed-v011 | `meta-llama/Llama-3.2-1B-Instruct:tdygoem4x7kvo97ghqcpxtss` | `20260603` train seed | 8-12 / all | `0.6541` | `1.000` | `0.375` | `0.1875` | `0.5972` | `37.1` | Strong reward jump; still not reliable arithmetic. |
| trained-heldout-v011 | `meta-llama/Llama-3.2-1B-Instruct:tdygoem4x7kvo97ghqcpxtss` | `424242` held-out seed | 8-12 / all | `0.4647` | `1.000` | `0.250` | `0.1250` | `0.3578` | `46.1` | Generalizes format and some arithmetic signal, but exact answers remain sparse. |

## Runs

| Run | Model | Steps | Batch / Rollouts | Max Tokens | Status | Cost | Reward Read | Notes |
| --- | --- | ---: | --- | ---: | --- | ---: | --- | --- |
| `ilb7rwevow9e1nzorv00rhxz` | Llama 1B | 1 | 128 / 8 | 512 | completed | `$0.0078` | step 0 reward `0.1504` | Hosted smoke on v0.1.1 mixed rung; no checkpoints listed, adapter READY. |
| `lv05ttq2v7kd7l628qdstxjz` | Llama 1B | 20 | 128 / 8 | 512 | completed | `$0.10` | step 0 `0.1447`, step 15 `0.5586`, final step 19 `0.4571` | First non-trivial RL run; final adapter `tdygoem4x7kvo97ghqcpxtss` deployed and evaluated. |

20-step metrics snapshots:

| Step | Reward | Parseable | Exact One Result | Exact Answer | Answer Score | Multi Candidate | Truncation | Output Chars |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | `0.1447` | `0.379` | `0.075` | `0.050` | `0.0976` | `0.004` | `0.000` | `233.6` |
| 1 | `0.1648` | `0.458` | `0.067` | `0.054` | `0.1145` | `0.042` | `0.033` | `376.6` |
| 5 | `0.2465` | `0.663` | `0.096` | `0.075` | `0.1740` | `0.058` | `0.067` | `400.2` |
| 9 | `0.3448` | `0.900` | `0.158` | `0.075` | `0.2403` | `0.033` | `0.000` | `163.7` |
| 15 | `0.5586` | `1.000` | `0.121` | `0.208` | `0.4944` | `0.000` | `0.000` | `144.5` |
| 19 | `0.4571` | `0.992` | `0.219` | `0.102` | `0.3534` | `0.000` | `0.000` | `217.8` |

The trained eval on the same seed scores higher than the final logged training
step because the deployed final adapter is evaluated with a separate 16-example
sample. The held-out trained eval remains well above the base held-out eval,
which makes this a useful RL episode despite low exact-answer rates.

## Observations

- v0.1.1 fixed the data-loading issue cleanly. The bug was not model behavior:
  it was Arrow schema incompatibility in mixed `info` metadata.
- The 20-step run learned parseability strongly: base mixed parseability was
  `0.125`, trained train-seed parseability was `1.000`, and trained held-out
  parseability was `1.000`.
- Reward increase was not just formatting. `answer_score` moved from `0.000`
  on the base mixed evals to `0.597` train-seed and `0.358` held-out.
- Exact arithmetic remains the limiting behavior. Exact-answer eval rates after
  RL are only `0.188` train-seed and `0.125` held-out.
- The model often emits valid JSON outside the required `<result>` tags. The
  reward gives correctness credit with a format penalty, so exact-one-result
  lags parseability.
- Candidate stuffing did not emerge here: final multi-candidate rate is `0.0`.
- No sandbox or judge costs were involved. The 20-step hosted RL run cost about
  `$0.10`; the one-step smoke cost `$0.0078`.

## Failure Modes

- Heterogeneous `info` metadata can break dataset construction on Prime Hub if
  fields mix strings, numbers, and dicts. Store mixed metadata as JSON strings.
- Format learning can dominate early improvements. Track parseability,
  exact-one-result, exact-answer, and answer-score separately.
- Numeric shaped reward can show useful near-miss learning while exact answer
  rate stays low.
- The current reward accepts JSON outside tags with a penalty. This may be a
  useful shaped signal, but future variants may tighten it if exact tag
  compliance is the research target.
- Final adapter deployment was only reliable through the step-null READY
  adapter record. Step 19/20 adapter records were still `UPLOADING` when
  checked.

## Interpretation

`meta-data-analysis-lite` is a better second corpus environment than another
already-solvable state-tracking run. It gives a cheap, non-tool RL signal where
Llama 1B learns output structure and some computation, but does not solve the
task. That makes it useful for later meta-learning examples about distinguishing
format learning, shaped partial-credit learning, and exact task competence.

This also supports a practical next-step design: keep v0.1.1 as the no-tool
baseline, then build a separate tool-enabled version over the same table
generator without adding a paid judge or sandbox dependency at first.

## Next Steps

1. Commit and push this completed first-pass episode record on
   `codex/meta-data-analysis-lite`.
2. For this env, consider a small difficulty ablation before model scaling:
   14-20 rows, all task families, still no tools.
3. For a new env or v0.2, add cheap deterministic tools where useful while
   steering clear of sandbox costs until the no-tool baseline is clear.
