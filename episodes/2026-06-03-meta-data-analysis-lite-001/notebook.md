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
| v0.2-tool | 8-12 | same generator with deterministic tool path | test tool benefit/coherence |

## Local And Hub Checks

Local unit test command:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest episodes/2026-06-03-meta-data-analysis-lite-001/env/test_meta_data_analysis_lite.py
```

Result:

- `15 passed, 1 skipped` locally for v0.1.1.
- `19 passed, 2 skipped` locally for v0.2.1 after adding tool mode.
- The skipped tests are optional compatibility checks for dependencies not
  present in the local Python environment.
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
- v0.2.1 pushed successfully as `abugoot/meta-data-analysis-lite@0.2.1`;
  content hash prefix `fd2e9aec`, wheel SHA
  `81674c42cb183d2ee5c70a7fbc26b06f35a94a272f51e5b1ceacb8ba1f70f600`.

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

## Tool-Mode Extension

Version `0.2.1` adds a cheap deterministic tool:

```text
analyze_table(csv_text, question) -> {"answer": ..., "task_family": ..., "target": ..., "num_rows": ...}
```

The tool computes the generated question directly from the CSV. The model still
has to make a coherent final answer with exactly one `<result>{"answer": ...}</result>`
tag. This isolates a tool-use protocol question: can RL teach the model to call
the tool once and then stop, without paying for a sandbox or judge model?

### Tool-Mode Base Evals

| Eval | Model | Tool Args | Reward | Parseable | Exact One Result | Exact Answer | Tool Calls | Tool Errors | Notes |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| llama1b-tools-v020 | `meta-llama/Llama-3.2-1B-Instruct` | tools, turns 3 | `0.000` | `0.000` | `0.000` | `0.000` | `0.000` | `0.000` | Provider returned 404 before generation; diagnostic only. |
| llama1b-notools-v020 | `meta-llama/Llama-3.2-1B-Instruct` | no tools | `0.000` | n/a | n/a | n/a | `0.000` | `0.000` | Confirms the package itself worked without tools. |
| qwen2b-tools-v020-n4 | `Qwen/Qwen3.5-2B` | tools, turns 3 | `0.732` | `0.750` | `0.500` | `0.750` | `1.750` | n/a | Tool works; some rollouts loop tool calls. |
| qwen2b-tools-v021-n4 | `Qwen/Qwen3.5-2B` | tools, turns 2 | `0.250` | `0.250` | `0.250` | `0.250` | `1.750` | n/a | Two tool turns were too tight; many rollouts ended before final answer. |
| qwen2b-notools-v021-n16 | `Qwen/Qwen3.5-2B` | no tools | `0.4317` | `1.000` | `0.5625` | `0.0625` | `0.000` | `0.000` | Formats well but exact arithmetic is low. |
| qwen2b-tools-v021-n16 | `Qwen/Qwen3.5-2B` | tools, turns 3 | `0.3125` | `0.3125` | `0.3125` | `0.3125` | `2.375` | `0.0625` | Exact when it finalizes, but tool loops dominate. |

### Tool-Mode Runs

| Run | Model | Steps | Batch / Rollouts | Status | Cost | Reward Read | Notes |
| --- | --- | ---: | --- | --- | ---: | --- | --- |
| `gvq9mq8ppx0a4g3rwsx77215` | Qwen 2B | 1 | 64 / 4 | completed | `$0.01` | step 0 reward `0.5867` | Hosted smoke; no checkpoint listed; final adapter READY but not used. |
| `cw41toqvv97d0ba5q8e199wx` | Qwen 2B | 20 | 64 / 4 | stopped | `$0.00` | no metrics | Stalled before useful samples; stopped manually. |
| `x36l212xgveqr6qgnsske6jk` | Qwen 2B | 20 | 32 / 2 | failed | `$0.08` | step 0 `0.6785`, step 10 `0.9977`, step 13 `0.8750` | Useful dynamics trace; crashed at step 14 after all rollouts were zero-advantage on three attempts. |
| `ic5nrtiex0w2zuuf421ox451` | Qwen 2B | 10 | 32 / 2 | completed | `$0.06` | step 0 `0.3882`, step 9 `0.9978` | Capped rerun stopped before zero-advantage crash region; final adapter deployed as `pdfn3guyfg0b35kvbxf3j2n6`. |

10-step capped run metrics:

| Step | Reward | Parseable | Exact One Result | Exact Answer | Tool Calls | Tool Errors | Zero-Advantage Filter | Total Tokens |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | `0.3882` | `0.417` | `0.367` | `0.383` | `2.067` | `0.100` | `0.5625` | `47,925` |
| 1 | `0.5429` | `0.595` | `0.405` | `0.548` | `1.750` | `0.048` | `0.4375` | `94,312` |
| 2 | `0.3731` | `0.400` | `0.167` | `0.400` | `2.333` | `0.067` | `0.4375` | `147,609` |
| 3 | `0.7268` | `0.857` | `0.196` | `0.732` | `1.268` | `0.036` | `0.5000` | `186,912` |
| 4 | `0.9120` | `1.000` | `0.438` | `0.906` | `1.000` | `0.000` | `0.4375` | `224,394` |
| 5 | `0.8896` | `1.000` | `0.571` | `0.893` | `1.000` | `0.000` | `0.3125` | `261,130` |
| 6 | `0.9028` | `1.000` | `0.683` | `0.900` | `1.033` | `0.067` | `0.6250` | `299,169` |
| 7 | `0.9622` | `0.969` | `0.875` | `0.969` | `0.969` | `0.000` | `0.8125` | `336,202` |
| 8 | `0.8953` | `0.900` | `0.833` | `0.900` | `0.967` | `0.000` | `0.6875` | `373,857` |
| 9 | `0.9978` | `1.000` | `0.969` | `1.000` | `1.000` | `0.000` | `0.9375` | `410,303` |

### Tool-Mode Trained Evals

| Eval | Model | Seed/Split | Reward | Parseable | Exact One Result | Exact Answer | Tool Calls | Tool Errors | Output Tokens | Notes |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| trained-tools-train-v021 | `Qwen/Qwen3.5-2B:pdfn3guyfg0b35kvbxf3j2n6` | `20260603` train seed | `0.9780` | `1.000` | `0.750` | `1.000` | `1.000` | `0.000` | `373.3` | Correct answers and one tool call throughout; some extra text/tag-shape issues remain. |
| trained-tools-heldout-v021 | `Qwen/Qwen3.5-2B:pdfn3guyfg0b35kvbxf3j2n6` | `424242` held-out seed | `1.0000` | `1.000` | `1.000` | `1.000` | `1.000` | `0.000` | `327.4` | Perfect 16-example held-out eval. |

### Tool-Mode Observations

- Qwen 2B is the practical starting model for this tool-mode version. Llama 1B
  tool calls failed at the provider layer, while the same package worked without
  tools.
- Base Qwen 2B with tools had lower reward than no-tool Qwen 2B despite better
  exactness, because it often called the tool repeatedly and failed to finalize.
- RL quickly taught the desired protocol: one tool call, no tool errors, then a
  final result. Exact answer reached `1.0` on train and held-out evals.
- The task became too easy for a long 20-step run with enforced zero-advantage
  filtering. The run `x36l212xgveqr6qgnsske6jk` failed at step 14 after three
  all-filtered batches.
- A capped 10-step run completed cleanly and produced a deployable adapter. This
  is the better default config for future agents using this env version.

### Tool-Mode Interpretation

The tool-enabled version is a clean example of RL improving tool-use protocol
rather than raw arithmetic. The base model can sometimes use the deterministic
tool, but it does not reliably stop and synthesize the final answer. After a
short RL run, the model uses exactly one tool call and generalizes to a held-out
seed. This is a useful meta-learning case because the decisive metrics are not
just reward and exact answer; `total_tool_calls`, `tool_error_count`,
`exact_one_result`, and zero-advantage filtering explain the training dynamics.

## Next Steps

1. Commit and push the v0.2.1 tool-mode extension on
   `codex/meta-data-analysis-tools`.
2. For this env, increase difficulty before more model scaling: larger tables,
   hidden irrelevant columns, or tasks where the tool is sometimes unnecessary.
3. For future tool envs, include tool-call count, tool errors, max-turn exits,
   and zero-advantage filtering in the default metric schema.
