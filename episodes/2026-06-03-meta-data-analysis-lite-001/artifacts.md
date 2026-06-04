# Artifacts: 2026-06-03-meta-data-analysis-lite-001

## Prime Hosted Runs

| Run ID | Dashboard | Config | Status | Notes |
| --- | --- | --- | --- | --- |
| `ilb7rwevow9e1nzorv00rhxz` | https://app.primeintellect.ai/dashboard/training/ilb7rwevow9e1nzorv00rhxz | `configs/llama1b_1step_smoke_v01_mixed.toml` | completed | v0.1.1 mixed-rung smoke. Step 0 reward `0.1504`, parseable `0.396`, exact answer `0.0958`; cost `$0.0078`. |
| `lv05ttq2v7kd7l628qdstxjz` | https://app.primeintellect.ai/dashboard/training/lv05ttq2v7kd7l628qdstxjz | `configs/llama1b_20step_v011_mixed.toml` | completed | 20-step Llama 1B mixed-rung run. Final logged reward `0.4571`, parseable `0.992`, exact answer `0.1016`; cost `$0.10`. |

## Prime Evals

| Eval ID | Dashboard | Command/Config | Status | Notes |
| --- | --- | --- | --- | --- |
| - | - | `prime eval run ... --save-results --skip-upload` | local results saved | Evals were run through Prime CLI inference but not uploaded, so the durable artifacts are the local `metadata.json` and `results.jsonl` files below. |

## Local Evals

| Eval | Output Path | Model | Env Args | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| local-unit-tests-v011 | - | n/a | v0.1.1 local helpers | passed | `PYTHONDONTWRITEBYTECODE=1 python -m pytest episodes/2026-06-03-meta-data-analysis-lite-001/env/test_meta_data_analysis_lite.py`; `15 passed, 1 skipped` locally. |
| arrow-compat-v011 | - | n/a | mixed tasks | passed | Prime CLI Python successfully built a `datasets.Dataset` from mixed-task generated examples after the v0.1.1 JSON-string metadata fix. |
| base-easy-v010-legacy | `evals/base_easy_seed20260603_llama1b_n16/evals/meta-data-analysis-lite--meta-llama--Llama-3.2-1B-Instruct/e6878d66/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct` | v0.1.0, seed `20260603`, rows 6-8, sum/count | completed | Legacy pre-fix easy eval; reward `0.0567`. |
| base-easy-v011 | `evals/base_easy_seed20260603_llama1b_n16_v011/evals/meta-data-analysis-lite--meta-llama--Llama-3.2-1B-Instruct/706e854a/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct` | seed `20260603`, rows 6-8, sum/count | completed | Reward `0.0567`; parseable `0.250`; exact answer `0.000`; answer score `0.0156`. |
| base-mixed-v011 | `evals/base_mixed_seed20260603_llama1b_n16_v011/evals/meta-data-analysis-lite--meta-llama--Llama-3.2-1B-Instruct/8833d2d8/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct` | seed `20260603`, rows 8-12, all task families | completed | Reward `0.0225`; parseable `0.125`; exact answer `0.000`; answer score `0.000`. |
| base-heldout-v011 | `evals/base_mixed_seed424242_llama1b_n16_v011/evals/meta-data-analysis-lite--meta-llama--Llama-3.2-1B-Instruct/2d7d8e33/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct` | seed `424242`, rows 8-12, all task families | completed | Reward `0.0113`; parseable `0.0625`; exact answer `0.000`; answer score `0.000`. |
| trained-mixed-v011 | `evals/run_lv05ttq2v7kd7l628qdstxjz/trained_mixed_seed20260603_llama1b_n16_v011/evals/meta-data-analysis-lite--meta-llama--Llama-3.2-1B-Instruct:tdygoem4x7kvo97ghqcpxtss/56b2131f/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct:tdygoem4x7kvo97ghqcpxtss` | seed `20260603`, rows 8-12, all task families | completed | Reward `0.6541`; parseable `1.000`; exact-one-result `0.375`; exact answer `0.1875`; answer score `0.5972`. |
| trained-heldout-v011 | `evals/run_lv05ttq2v7kd7l628qdstxjz/trained_mixed_seed424242_llama1b_n16_v011/evals/meta-data-analysis-lite--meta-llama--Llama-3.2-1B-Instruct:tdygoem4x7kvo97ghqcpxtss/b299410c/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct:tdygoem4x7kvo97ghqcpxtss` | seed `424242`, rows 8-12, all task families | completed | Reward `0.4647`; parseable `1.000`; exact-one-result `0.250`; exact answer `0.125`; answer score `0.3578`. |

## Checkpoints

| Run ID | Step | Checkpoint ID / Adapter ID | Status | Notes |
| --- | ---: | --- | --- | --- |
| `ilb7rwevow9e1nzorv00rhxz` | final | `lhfaj6lw7f293qokts9knyyu` | READY adapter | Smoke final adapter was READY but not deployed. `prime train checkpoints` listed no checkpoints. |
| `lv05ttq2v7kd7l628qdstxjz` | 10 | `bpdntmq7qqsac8odiy1x4j9w` | READY checkpoint | Listed by `prime train checkpoints`; size `172.3 MB`. |
| `lv05ttq2v7kd7l628qdstxjz` | final | `tdygoem4x7kvo97ghqcpxtss` | READY adapter, deployed | Step-null final adapter deployed successfully and was used for trained evals. |
| `lv05ttq2v7kd7l628qdstxjz` | 19 | `k1ekfx56ina5agrzva9ax4mn` | UPLOADING adapter | Listed after run completion but not usable for eval. |
| `lv05ttq2v7kd7l628qdstxjz` | 20 | `o9ac2ohv104rug6wtfi4jtqx` | UPLOADING adapter | Deployment attempts failed while status remained `UPLOADING`. |

## Rollout Samples

| Run ID | Step | Command | Notes |
| --- | ---: | --- | --- |
| `ilb7rwevow9e1nzorv00rhxz` | 0 | `prime train rollouts ilb7rwevow9e1nzorv00rhxz --step 0 --num 5 --plain` | Smoke rollouts were available even though the first progress check initially reported no samples. |
| `lv05ttq2v7kd7l628qdstxjz` | 0, 10 | `prime train rollouts lv05ttq2v7kd7l628qdstxjz --step <step> --num 5 --plain` | Samples show format learning and some exact answers, but also JSON outside tags and arithmetic mistakes with partial reward. |

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

## Local Files

| Path | Kind | Notes |
| --- | --- | --- |
| `episodes/2026-06-03-meta-data-analysis-lite-001/env/meta_data_analysis_lite.py` | environment source | v0.1.1 deterministic table QA environment. |
| `episodes/2026-06-03-meta-data-analysis-lite-001/env/test_meta_data_analysis_lite.py` | tests | parser/reward/generation checks plus mixed-task Arrow metadata regression. |
| `episodes/2026-06-03-meta-data-analysis-lite-001/env/README.md` | env docs | local usage and reward summary. |
| `episodes/2026-06-03-meta-data-analysis-lite-001/env/pyproject.toml` | package metadata | Prime Hub package metadata, version `0.1.1`. |
| `episodes/2026-06-03-meta-data-analysis-lite-001/configs/llama1b_1step_smoke_v01_mixed.toml` | training config | v0.1.1 smoke config. |
| `episodes/2026-06-03-meta-data-analysis-lite-001/configs/llama1b_20step_v011_mixed.toml` | training config | v0.1.1 first non-trivial RL config. |

## External Links

| Label | URL | Notes |
| --- | --- | --- |
| Prime environment | https://app.primeintellect.ai/dashboard/environments/abugoot/meta-data-analysis-lite | `abugoot/meta-data-analysis-lite@0.1.1` is latest. |
| Smoke run | https://app.primeintellect.ai/dashboard/training/ilb7rwevow9e1nzorv00rhxz | 1-step Llama 1B hosted smoke. |
| 20-step run | https://app.primeintellect.ai/dashboard/training/lv05ttq2v7kd7l628qdstxjz | First non-trivial Llama 1B hosted RL run. |
