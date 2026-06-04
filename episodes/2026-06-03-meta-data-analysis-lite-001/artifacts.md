# Artifacts: 2026-06-03-meta-data-analysis-lite-001

## Prime Hosted Runs

| Run ID | Dashboard | Config | Status | Notes |
| --- | --- | --- | --- | --- |
| `ilb7rwevow9e1nzorv00rhxz` | https://app.primeintellect.ai/dashboard/training/ilb7rwevow9e1nzorv00rhxz | `configs/llama1b_1step_smoke_v01_mixed.toml` | completed | v0.1.1 mixed-rung smoke. Step 0 reward `0.1504`, parseable `0.396`, exact answer `0.0958`; cost `$0.0078`. |
| `lv05ttq2v7kd7l628qdstxjz` | https://app.primeintellect.ai/dashboard/training/lv05ttq2v7kd7l628qdstxjz | `configs/llama1b_20step_v011_mixed.toml` | completed | 20-step Llama 1B mixed-rung run. Final logged reward `0.4571`, parseable `0.992`, exact answer `0.1016`; cost `$0.10`. |
| `gvq9mq8ppx0a4g3rwsx77215` | https://app.primeintellect.ai/dashboard/training/gvq9mq8ppx0a4g3rwsx77215 | `configs/qwen2b_1step_v021_tools.toml` | completed | v0.2.1 Qwen 2B tool-mode smoke. Step 0 reward `0.5867`, exact answer `0.5938`, total tool calls `1.8438`; cost `$0.01`. |
| `cw41toqvv97d0ba5q8e199wx` | https://app.primeintellect.ai/dashboard/training/cw41toqvv97d0ba5q8e199wx | `configs/qwen2b_20step_v021_tools.toml` | stopped | First 20-step Qwen 2B tool attempt stalled before useful metrics; stopped manually; cost `$0.00`. |
| `x36l212xgveqr6qgnsske6jk` | https://app.primeintellect.ai/dashboard/training/x36l212xgveqr6qgnsske6jk | `configs/qwen2b_20step_v021_tools_b32r2.toml` | failed | Smaller 20-step Qwen 2B tool run produced useful metrics, then crashed at step 14 after all rollouts were zero-advantage on three attempts; cost `$0.08`. |
| `ic5nrtiex0w2zuuf421ox451` | https://app.primeintellect.ai/dashboard/training/ic5nrtiex0w2zuuf421ox451 | `configs/qwen2b_10step_v021_tools_b32r2.toml` | completed | Capped Qwen 2B tool run. Final logged step 9 reward `0.9978`, exact answer `1.0`, total tool calls `1.0`; final adapter `pdfn3guyfg0b35kvbxf3j2n6` deployed; cost `$0.06`. |

## Prime Evals

| Eval ID | Dashboard | Command/Config | Status | Notes |
| --- | --- | --- | --- | --- |
| - | - | `prime eval run ... --save-results --skip-upload` | local results saved | Evals were run through Prime CLI inference but not uploaded, so the durable artifacts are the local `metadata.json` and `results.jsonl` files below. |

## Local Evals

| Eval | Output Path | Model | Env Args | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| local-unit-tests-v011 | - | n/a | v0.1.1 local helpers | passed | `PYTHONDONTWRITEBYTECODE=1 python -m pytest episodes/2026-06-03-meta-data-analysis-lite-001/env/test_meta_data_analysis_lite.py`; `15 passed, 1 skipped` locally. |
| local-unit-tests-v021 | - | n/a | v0.2.1 tool helpers | passed | Same pytest command after tool-mode changes; `19 passed, 2 skipped` locally. |
| arrow-compat-v011 | - | n/a | mixed tasks | passed | Prime CLI Python successfully built a `datasets.Dataset` from mixed-task generated examples after the v0.1.1 JSON-string metadata fix. |
| base-easy-v010-legacy | `evals/base_easy_seed20260603_llama1b_n16/evals/meta-data-analysis-lite--meta-llama--Llama-3.2-1B-Instruct/e6878d66/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct` | v0.1.0, seed `20260603`, rows 6-8, sum/count | completed | Legacy pre-fix easy eval; reward `0.0567`. |
| base-easy-v011 | `evals/base_easy_seed20260603_llama1b_n16_v011/evals/meta-data-analysis-lite--meta-llama--Llama-3.2-1B-Instruct/706e854a/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct` | seed `20260603`, rows 6-8, sum/count | completed | Reward `0.0567`; parseable `0.250`; exact answer `0.000`; answer score `0.0156`. |
| base-mixed-v011 | `evals/base_mixed_seed20260603_llama1b_n16_v011/evals/meta-data-analysis-lite--meta-llama--Llama-3.2-1B-Instruct/8833d2d8/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct` | seed `20260603`, rows 8-12, all task families | completed | Reward `0.0225`; parseable `0.125`; exact answer `0.000`; answer score `0.000`. |
| base-heldout-v011 | `evals/base_mixed_seed424242_llama1b_n16_v011/evals/meta-data-analysis-lite--meta-llama--Llama-3.2-1B-Instruct/2d7d8e33/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct` | seed `424242`, rows 8-12, all task families | completed | Reward `0.0113`; parseable `0.0625`; exact answer `0.000`; answer score `0.000`. |
| trained-mixed-v011 | `evals/run_lv05ttq2v7kd7l628qdstxjz/trained_mixed_seed20260603_llama1b_n16_v011/evals/meta-data-analysis-lite--meta-llama--Llama-3.2-1B-Instruct:tdygoem4x7kvo97ghqcpxtss/56b2131f/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct:tdygoem4x7kvo97ghqcpxtss` | seed `20260603`, rows 8-12, all task families | completed | Reward `0.6541`; parseable `1.000`; exact-one-result `0.375`; exact answer `0.1875`; answer score `0.5972`. |
| trained-heldout-v011 | `evals/run_lv05ttq2v7kd7l628qdstxjz/trained_mixed_seed424242_llama1b_n16_v011/evals/meta-data-analysis-lite--meta-llama--Llama-3.2-1B-Instruct:tdygoem4x7kvo97ghqcpxtss/b299410c/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct:tdygoem4x7kvo97ghqcpxtss` | seed `424242`, rows 8-12, all task families | completed | Reward `0.4647`; parseable `1.000`; exact-one-result `0.250`; exact answer `0.125`; answer score `0.3578`. |
| base-tools-llama1b-v020 | `evals/base_mixed_tools_seed20260603_llama1b_n16_v020/evals/meta-data-analysis-lite--meta-llama--Llama-3.2-1B-Instruct/a801924c/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct` | seed `20260603`, tools true, turns 3 | failed-provider | Provider returned 404 before generation; avg error `1.0`; confirms hosted Llama 1B tool path was not usable. |
| base-notools-qwen2b-v021 | `evals/base_mixed_notools_seed20260603_qwen2b_n16_v021/evals/meta-data-analysis-lite--Qwen--Qwen3.5-2B/575387dd/results.jsonl` | `Qwen/Qwen3.5-2B` | seed `20260603`, tools false | completed | Reward `0.4317`; parseable `1.000`; exact-one-result `0.5625`; exact answer `0.0625`; answer score `0.2831`. |
| base-tools-qwen2b-v021 | `evals/base_mixed_tools_seed20260603_qwen2b_n16_v021_t3/evals/meta-data-analysis-lite--Qwen--Qwen3.5-2B/46e3caac/results.jsonl` | `Qwen/Qwen3.5-2B` | seed `20260603`, tools true, turns 3 | completed | Reward `0.3125`; exact answer `0.3125`; total tool calls `2.375`; tool errors `0.0625`; many rollouts looped tool calls. |
| trained-tools-train-qwen2b-v021 | `evals/run_ic5nrtiex0w2zuuf421ox451/trained_mixed_tools_seed20260603_qwen2b_n16_v021/evals/meta-data-analysis-lite--Qwen--Qwen3.5-2B:pdfn3guyfg0b35kvbxf3j2n6/6748d292/results.jsonl` | `Qwen/Qwen3.5-2B:pdfn3guyfg0b35kvbxf3j2n6` | seed `20260603`, tools true, turns 3 | completed | Reward `0.9780`; parseable `1.000`; exact-one-result `0.750`; exact answer `1.000`; total tool calls `1.000`; tool errors `0.000`. |
| trained-tools-heldout-qwen2b-v021 | `evals/run_ic5nrtiex0w2zuuf421ox451/trained_mixed_tools_seed424242_qwen2b_n16_v021/evals/meta-data-analysis-lite--Qwen--Qwen3.5-2B:pdfn3guyfg0b35kvbxf3j2n6/85b26645/results.jsonl` | `Qwen/Qwen3.5-2B:pdfn3guyfg0b35kvbxf3j2n6` | seed `424242`, tools true, turns 3 | completed | Reward `1.0000`; parseable `1.000`; exact-one-result `1.000`; exact answer `1.000`; total tool calls `1.000`; tool errors `0.000`. |

## Checkpoints

| Run ID | Step | Checkpoint ID / Adapter ID | Status | Notes |
| --- | ---: | --- | --- | --- |
| `ilb7rwevow9e1nzorv00rhxz` | final | `lhfaj6lw7f293qokts9knyyu` | READY adapter | Smoke final adapter was READY but not deployed. `prime train checkpoints` listed no checkpoints. |
| `lv05ttq2v7kd7l628qdstxjz` | 10 | `bpdntmq7qqsac8odiy1x4j9w` | READY checkpoint | Listed by `prime train checkpoints`; size `172.3 MB`. |
| `lv05ttq2v7kd7l628qdstxjz` | final | `tdygoem4x7kvo97ghqcpxtss` | READY adapter, deployed | Step-null final adapter deployed successfully and was used for trained evals. |
| `lv05ttq2v7kd7l628qdstxjz` | 19 | `k1ekfx56ina5agrzva9ax4mn` | UPLOADING adapter | Listed after run completion but not usable for eval. |
| `lv05ttq2v7kd7l628qdstxjz` | 20 | `o9ac2ohv104rug6wtfi4jtqx` | UPLOADING adapter | Deployment attempts failed while status remained `UPLOADING`. |
| `gvq9mq8ppx0a4g3rwsx77215` | final | `dj38fts7fksyyn5az0dyqswj` | READY adapter | Qwen 2B 1-step smoke adapter; not deployed because the smoke was not a meaningful trained result. |
| `x36l212xgveqr6qgnsske6jk` | 5 | `ji7eu94pufsgzpc8dm93suyf` | READY checkpoint | Smaller 20-step Qwen tool run checkpoint. |
| `x36l212xgveqr6qgnsske6jk` | 10 | `rlp6o99npkgwkbh4hn4jqre0` | READY checkpoint | Smaller 20-step Qwen tool run checkpoint near peak reward. |
| `x36l212xgveqr6qgnsske6jk` | 13 | `d3nlotc6wr3esj6qgv142amq` | UPLOADING adapter | Not deployed; run failed after zero-advantage collapse. |
| `x36l212xgveqr6qgnsske6jk` | 14 | `a27eolds2h7md0bv3zfoq3wp` | UPLOADING adapter | Not deployed; run failed after zero-advantage collapse. |
| `ic5nrtiex0w2zuuf421ox451` | 5 | `itl3z69y6fy8uc86zlxji3n5` | UPLOADING checkpoint | Step checkpoint remained uploading when checked. |
| `ic5nrtiex0w2zuuf421ox451` | final | `pdfn3guyfg0b35kvbxf3j2n6` | READY adapter, deployed | Final capped-run adapter deployed at `2026-06-04 11:47:51 UTC` and used for train/held-out tool evals. |

## Rollout Samples

| Run ID | Step | Command | Notes |
| --- | ---: | --- | --- |
| `ilb7rwevow9e1nzorv00rhxz` | 0 | `prime train rollouts ilb7rwevow9e1nzorv00rhxz --step 0 --num 5 --plain` | Smoke rollouts were available even though the first progress check initially reported no samples. |
| `lv05ttq2v7kd7l628qdstxjz` | 0, 10 | `prime train rollouts lv05ttq2v7kd7l628qdstxjz --step <step> --num 5 --plain` | Samples show format learning and some exact answers, but also JSON outside tags and arithmetic mistakes with partial reward. |
| `gvq9mq8ppx0a4g3rwsx77215` | 0 | `prime train rollouts gvq9mq8ppx0a4g3rwsx77215 --step 0 --num 3 --plain` | CLI returned no samples even though metrics/logs showed 64 samples logged. |
| `ic5nrtiex0w2zuuf421ox451` | 0 | `prime train rollouts ic5nrtiex0w2zuuf421ox451 --step 0 --num 3 --plain` | Step 0 samples are the main run-scoped rollout artifacts available through Prime progress. |

## Metrics And Distributions

| Run ID | Step | Metric | Value |
| --- | ---: | --- | ---: |
| `ilb7rwevow9e1nzorv00rhxz` | 0 | reward / parseable / exact-answer | `0.1504 / 0.3958 / 0.0958` |
| `ilb7rwevow9e1nzorv00rhxz` | 0 | exact-one-result / answer-score / truncation | `0.0542 / 0.1053 / 0.0` |
| `lv05ttq2v7kd7l628qdstxjz` | 0 | reward / parseable / exact-answer | `0.1447 / 0.3792 / 0.0500` |
| `lv05ttq2v7kd7l628qdstxjz` | 5 | reward / parseable / exact-answer | `0.2465 / 0.6625 / 0.0750` |
| `lv05ttq2v7kd7l628qdstxjz` | 9 | reward / parseable / exact-answer | `0.3448 / 0.9000 / 0.0750` |
| `lv05ttq2v7kd7l628qdstxjz` | 15 | reward / parseable / exact-answer | `0.5586 / 1.0000 / 0.2083` |
| `lv05ttq2v7kd7l628qdstxjz` | 19 | reward / parseable / exact-answer | `0.4571 / 0.9922 / 0.1016` |
| `lv05ttq2v7kd7l628qdstxjz` | 19 | exact-one-result / answer-score / truncation | `0.2188 / 0.3534 / 0.0` |
| `gvq9mq8ppx0a4g3rwsx77215` | 0 | reward / exact-answer / tool-calls | `0.5867 / 0.5938 / 1.8438` |
| `x36l212xgveqr6qgnsske6jk` | 0 | reward / exact-answer / tool-calls / zero-advantage | `0.6785 / 0.6833 / 1.3833 / 0.2500` |
| `x36l212xgveqr6qgnsske6jk` | 10 | reward / exact-answer / tool-calls / zero-advantage | `0.9977 / 1.0000 / 1.0000 / 0.9375` |
| `x36l212xgveqr6qgnsske6jk` | 13 | reward / exact-answer / tool-calls / zero-advantage | `0.8750 / 0.8750 / 1.0313 / 0.8750` |
| `ic5nrtiex0w2zuuf421ox451` | 0 | reward / exact-answer / tool-calls / zero-advantage | `0.3882 / 0.3833 / 2.0667 / 0.5625` |
| `ic5nrtiex0w2zuuf421ox451` | 4 | reward / exact-answer / tool-calls / zero-advantage | `0.9120 / 0.9063 / 1.0000 / 0.4375` |
| `ic5nrtiex0w2zuuf421ox451` | 9 | reward / exact-answer / tool-calls / zero-advantage | `0.9978 / 1.0000 / 1.0000 / 0.9375` |

## Local Files

| Path | Kind | Notes |
| --- | --- | --- |
| `episodes/2026-06-03-meta-data-analysis-lite-001/env/meta_data_analysis_lite.py` | environment source | v0.2.1 deterministic table QA environment with optional `analyze_table` tool mode. |
| `episodes/2026-06-03-meta-data-analysis-lite-001/env/test_meta_data_analysis_lite.py` | tests | parser/reward/generation checks, mixed-task Arrow metadata regression, and tool-mode smoke tests. |
| `episodes/2026-06-03-meta-data-analysis-lite-001/env/README.md` | env docs | local usage, reward summary, and tool-mode usage. |
| `episodes/2026-06-03-meta-data-analysis-lite-001/env/pyproject.toml` | package metadata | Prime Hub package metadata, version `0.2.1`. |
| `episodes/2026-06-03-meta-data-analysis-lite-001/configs/llama1b_1step_smoke_v01_mixed.toml` | training config | v0.1.1 smoke config. |
| `episodes/2026-06-03-meta-data-analysis-lite-001/configs/llama1b_20step_v011_mixed.toml` | training config | v0.1.1 first non-trivial RL config. |
| `episodes/2026-06-03-meta-data-analysis-lite-001/configs/qwen2b_10step_v021_tools_b32r2.toml` | training config | Recommended v0.2.1 Qwen 2B tool-mode capped run config. |

## External Links

| Label | URL | Notes |
| --- | --- | --- |
| Prime environment | https://app.primeintellect.ai/dashboard/environments/abugoot/meta-data-analysis-lite | `abugoot/meta-data-analysis-lite@0.2.1` is latest. |
| Smoke run | https://app.primeintellect.ai/dashboard/training/ilb7rwevow9e1nzorv00rhxz | 1-step Llama 1B hosted smoke. |
| 20-step run | https://app.primeintellect.ai/dashboard/training/lv05ttq2v7kd7l628qdstxjz | First non-trivial Llama 1B hosted RL run. |
| Qwen tool capped run | https://app.primeintellect.ai/dashboard/training/ic5nrtiex0w2zuuf421ox451 | Completed v0.2.1 tool-mode run with deployed final adapter. |
