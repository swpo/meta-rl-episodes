# Episode Notebook: 2026-06-02-meta-memory-state-001

## Question

Can a small deterministic Verifiers environment test multi-turn state tracking
with richer state updates than alphabet-sort, while staying cheap and robust to
malformed model outputs?

## Environment

- Env: `abugoot/meta-memory-state`
- Version/source: Prime Hub `0.6.0`, local scaffold source retained
- Local path or Hub URL: `episodes/2026-06-02-meta-memory-state-001/env`
  and `https://app.primeintellect.ai/dashboard/environments/abugoot/meta-memory-state`
- Key args for successful smoke: `seed=1337420`, `num_examples=128`,
  `min_turns=1`, `max_turns=2`, `account_count=2`
- Reward signal: per-turn shaped reward over account balances, total,
  hallucinated accounts, output format, and anti-stuffing penalties
- Parser assumptions: preferred output is one `<ledger>...</ledger>` JSON block;
  integer-like strings are accepted; malformed output returns 0 or shaped credit
- Tooling: none

## Hypotheses

1. Llama 1B should produce useful partial reward variance because format,
   arithmetic, and memory can fail independently.
2. Averaging per-turn shaped scores should reduce all-zero reward batches.
3. A deterministic parser and no judge/sandbox dependencies should keep cost
   comparable to or only slightly above alphabet-sort.

## Smoke Tests

### Local Unit Smoke

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B -m unittest discover -s episodes/2026-06-02-meta-memory-state-001/env -p 'test_*.py'
```

Result:

- Reward: exact full completion scores `1.0`; close wrong balances receive
  partial credit
- Truncation: not applicable
- Errors: none; malformed `None` and plain text return `0.0`
- Notes: 16 tests pass after adding hosted-signature, Verifiers
  message-object, anti-stuffing, diagnostic, and v0.6 schema-penalty
  regressions

### Syntax Smoke

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B -c "import sys; sys.path.insert(0, 'episodes/2026-06-02-meta-memory-state-001/env'); import meta_memory_state"
```

Result:

- Status: passed on Python 3.13.5
- Notes: Verifiers import is intentionally lazy inside `load_environment`

### Hosted RL Smoke

Run ID: `rdair5n0ca531bxqqvetrok8`

Dashboard: `https://app.primeintellect.ai/dashboard/training/rdair5n0ca531bxqqvetrok8`

Config: `episodes/2026-06-02-meta-memory-state-001/configs/llama1b_1step_smoke.toml`

Prepared command:

```bash
prime train episodes/2026-06-02-meta-memory-state-001/configs/llama1b_1step_smoke.toml --yes --plain
```

Expected cost:

- Rough estimate: `$0.002-$0.01`, using Phase 0 Llama 1B alphabet-sort cost as
  the proxy and allowing some headroom for longer multi-turn prompts
- Hard expectation: should remain below `$0.05` for one step unless hosted
  integration or tokenization behaves unexpectedly

Hub env:

- `abugoot/meta-memory-state@0.1.1`
- Content hash:
  `e28776ba0b031a4faafec40d226f4e18345a5759fc4d9b8f6b0faae1f7667f4f`
- Wheel SHA256:
  `dcdca4b74747213c3f092a8613fd7c1222e82abfbc5821e5bb25165cd0313782`
- Prime integration action: `SUCCESS`
- Failed version preserved: `0.1.0` failed integration because `README.md`
  was missing.

## Runs

| Run | Model | Steps | Max Tokens | Status | Cost | Reward Read | Notes |
| --- | --- | ---: | ---: | --- | ---: | --- | --- |
| local-unit-tests | none | 0 | 0 | passed | `$0.00` | exact and partial reward behavior verified | Pure helper tests only |
| llama1b-smoke | `meta-llama/Llama-3.2-1B-Instruct` | 1 | 512 | completed | `$0.03` | reward mean/min/max all `0.0` | Run `rdair5n0ca531bxqqvetrok8`; Hub env 0.1.1 installed and ran |
| llama1b-smoke-v02 | `meta-llama/Llama-3.2-1B-Instruct` | 1 | 512 | completed | `$0.0080` | reward mean/min/max all `0.0` | Run `mngozs87cvyj745q8zaqph9k`; easier prompt/parser still zero |
| llama1b-smoke-v03 | `meta-llama/Llama-3.2-1B-Instruct` | 1 | 512 | completed | `$0.0085` | reward mean/min/max all `0.0` | Run `qh9lqxz5v3s82sjfs03cso8h`; answer-signature fix still zero |
| llama1b-smoke-v04 | `meta-llama/Llama-3.2-1B-Instruct` | 1 | 512 | completed | `$0.0085` | reward mean `0.343`, min/max `0.213 / 0.618` | Run `msisq47uw7tcnvuxn5aejrbg`; non-trivial reward signal achieved |
| llama1b-50step-v04 | `meta-llama/Llama-3.2-1B-Instruct` | 50 | 512 | completed | `$0.61` | final reward mean `0.779`, min/max `0.580 / 0.926` | Run `wpw270lopu0vrzyfx9otn6w1`; reward improved but answer stuffing/truncation emerged |
| llama1b-50step-v05 | `meta-llama/Llama-3.2-1B-Instruct` | 50 | 512 | failed before training | `$0.00` | no steps | Run `ovhe41qu43r1i3gwo98lw0mq`; renderer auto-validation blocked model, and admin-only run_config was unavailable |
| qwen08b-50step-v05 | `Qwen/Qwen3.5-0.8B` | 50 | 16384 | completed | `$0.07` | final reward `0.936`, best step `0.993` | Run `t06x036p2njx21ts5fi5p4vm`; anti-stuffing metrics stayed clean, truncation `0.0` |
| qwen08b-30step-v06 | `Qwen/Qwen3.5-0.8B` | 30 | 16384 | completed | `$0.04` | final reward `0.916`, best step `0.989` | Run `fdzqzv4ridlnhond78eghitd`; stricter schema reward preserved clean formatting and short outputs |
| qwen08b-30step-v06-resume-from25 | `Qwen/Qwen3.5-0.8B` | 25 -> 30 | 16384 | completed | `$0.0067` | final logged reward `0.959` | Run `jspr0dm70xv1nzv2jkz8u8ug`; resumed from step-25 checkpoint to regenerate a final adapter |
| qwen08b-30step-v06-resume-retry2-from25 | `Qwen/Qwen3.5-0.8B` | 25 -> 26 | 16384 | stopped | `$0.0027` | restarted step rewards `0.969`, `0.954` | Run `pnm7mpulnx3j8y1oyjz2sxwx`; fresh resume and native restart both stalled waiting for trainer checkpoint 26 |
| qwen08b-30step-v06-diff-3acct-2to3 | `Qwen/Qwen3.5-0.8B` | 30 | 16384 | completed | `$0.06` | final reward `0.951`, step 20 `0.875` | Run `uvzzmvybz365g0qqgwbo2san`; first difficulty ablation with 3 accounts and 2-3 turns |
| qwen08b-30step-v06-diff-3acct-3to4-attempt1 | `Qwen/Qwen3.5-0.8B` | 0 -> 1 | 16384 | stopped | `$0.0052` | step rewards `0.560`, `0.532` | Run `xvpykb8rxhq1kzg5wtnm9ty6`; stopped after waiting at trainer checkpoint broadcast 1 for about 5.5 minutes |
| qwen08b-30step-v06-diff-3acct-3to4-retry | `Qwen/Qwen3.5-0.8B` | 30 | 16384 | completed | `$0.08` | final reward `0.879`, step 20 `0.857` | Run `xn4ncn6hfi6pexy78mtt5cen`; retry completed and showed a harder turn-depth regime |
| qwen08b-30step-v06-diff-4acct-3to4 | `Qwen/Qwen3.5-0.8B` | 30 | 16384 | completed | `$0.09` | final reward `0.865`, step 20 `0.889` | Run `epzwm0i1cbluvcx27ya4caan`; width increase did not cause sharp collapse, but solve-all stayed `0.0` |
| qwen08b-30step-v06-diff-4acct-4to5-attempt1 | `Qwen/Qwen3.5-0.8B` | 0 -> 1 | 16384 | stopped | `$0.0070` | step rewards `0.570`, `0.608` | Run `jvwvglhzbp2h8abmhtkgf6ri`; batch 128 stalled waiting for trainer checkpoint 1 |
| qwen08b-30step-v06-diff-4acct-4to5-retry | `Qwen/Qwen3.5-0.8B` | 0 -> 1 | 16384 | stopped | `$0.0069` | step rewards `0.599`, `0.587` | Run `ylzr995pao3587n4xgjnrj1r`; second batch-128 attempt repeated checkpoint-1 stall |
| qwen08b-30step-v06-diff-4acct-4to5-b64 | `Qwen/Qwen3.5-0.8B` | 30 | 16384 | completed | `$0.05` | final reward `0.895`, step 20 `0.855` | Run `zhc48qkatvucpcaqvsekd9sm`; batch 64 cleared checkpoint waits and still reached high shaped reward |
| qwen08b-30step-v06-diff-4acct-5to6-b64 | `Qwen/Qwen3.5-0.8B` | 0 | 16384 | stopped | `$0.00` | no completed step | Run `rzu3o8g5dro2qol7qbfbti1y`; superseded by successful batch-32 retry |
| qwen08b-30step-v06-diff-4acct-5to6-b32 | `Qwen/Qwen3.5-0.8B` | 30 | 16384 | completed | `$0.03` | final reward `0.848`, step 20 `0.777` | Run `o4qsl2ttfmlnf07bba1uo4qg`; 5-6 turn difficulty rung completed cheaply, formatting mostly clean, solve-all stayed `0.0` |
| qwen08b-30step-v06-diff-4acct-6to7-b32 | `Qwen/Qwen3.5-0.8B` | 30 | 16384 | completed | `$0.16` | final reward `0.713`, step 20 `0.801` | Run `t4kf6tmab09foppeih32pvx6`; first clear small-model difficulty trace, with mid-run length/repetition spike and recovery to clean formatting |
| qwen2b-30step-v06-diff-4acct-6to7-b32 | `Qwen/Qwen3.5-2B` | 30 | 16384 | completed | `$0.08` | final reward `0.957`, step 20 `0.912` | Run `wc5nvpymcd093n8x9c7yedgt`; matched model-scaling run, no length pathology, solve-all still `0.0` |

## Eval Matrix

### v0.4 Same-Reward Evals

These evals use the same v0.4 reward/objective. The extra columns are
auxiliary metrics computed from saved `results.jsonl` files with
`eval_analysis.py`.

| Eval | Model | Seed | Reward Mean | Truncation | Output Tokens | Parseable Turns | Multi-Candidate Turns | Mean Candidates | Code Fences | Notes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| base-train | base Llama 1B | `1337420` | `0.084` | `0.000` | `55.1` | `0.184` | `0.000` | `0.18` | `0.000` | Low reward, little valid JSON, no stuffing |
| base-heldout | base Llama 1B | `424242` | `0.025` | `0.000` | `63.3` | `0.064` | `0.000` | `0.06` | `0.000` | Lower held-out reward, still no stuffing |
| trained-train | adapter `lz4ro...` | `1337420` | `0.790` | `1.000` | `784.0` | `1.000` | `1.000` | `13.14` | `1.000` | Reward transfers to eval, but every output truncates |
| trained-heldout | adapter `lz4ro...` | `424242` | `0.782` | `1.000` | `752.0` | `1.000` | `1.000` | `13.23` | `1.000` | Same-reward improvement generalizes; stuffing mechanism generalizes too |

Read: held-out reward is not the problem here. The optimized behavior transfers
well to unseen examples under the same reward. The issue is that the reward
allows a high-scoring policy that emits many parseable candidates inside long
code-fenced outputs. The auxiliary metrics make that mechanism visible without
changing the eval objective.

### v0.5 Base Evals Before RL

Version `0.5.0` changes the reward to score the selected ledger candidate rather
than the best hidden candidate, then applies penalties for multiple candidates,
repeated tags, code fences, and very long outputs. It also adds Verifiers metrics
for parseability, exact one-ledger adherence, multi-candidate rate, code fences,
candidate count, and output length.

| Eval | Model | Seed | Reward Mean | Truncation | Output Tokens | Parseable Turns | Exact One Ledger | Multi-Candidate Turns | Mean Candidates | Notes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| base-train-v05 | base Llama 1B | `1337420` | `0.0148` | `0.000` | `56.1` | `0.041` | `0.041` | `0.000` | `0.04` | Sparse but nonzero signal; no stuffing/truncation |
| base-heldout-v05 | base Llama 1B | `424242` | `0.0173` | `0.000` | `78.1` | `0.043` | `0.043` | `0.000` | `0.04` | Similar sparse signal on held-out seed |

Read: v0.5 is much stricter than v0.4 for the base model, because most XML-like
outputs are no longer parseable JSON ledgers. This is acceptable for the next
probe because the signal is not all zero and the diagnostic metrics are clean:
no truncation, no code fences, and no multi-candidate behavior before RL.

### v0.6 Eval Attempts

After the v0.6 Qwen RL run completed, evals were retried to wrap up the version.

| Eval | Model | Seed | Reward Mean | Truncation | Output Tokens | Parseable Turns | Exact One Ledger | Multi-Candidate Turns | Mean Candidates | Notes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| base-heldout-v06-llama1b | base Llama 1B | `424242` | `0.0190` | `0.000` | `63.7` | `0.043` | `0.043` | `0.000` | `0.04` | Completed; confirms v0.6 eval harness works for non-Qwen |
| base-heldout-v06-qwen08b-tiny | base Qwen 0.8B | `424242` | - | - | - | - | - | - | - | Hung for about 60s before creating an output directory; killed locally |
| trained-heldout-v06-qwen08b | adapter `uuntogr...` | `424242` | - | - | - | - | - | - | - | Blocked because adapter deployment failed with "Adapter failed to load" |
| trained-heldout-v06-qwen08b-retry-tiny | adapter `lsbgjt...` | `424242` | `0.9740` | `0.000` | `38.7` | `1.000` | `1.000` | `0.000` | `1.00` | Completed 3-example eval after redeploy; full 32-example eval not run yet |

Read: v0.6 itself is evaluable: the Llama held-out eval completed and its
metrics are consistent with v0.5's sparse base behavior. Earlier base Qwen 0.8B
eval attempts hung locally through `prime eval run`, but a deployed
resume-regenerated adapter ran through a tiny trained held-out eval cleanly.
Later run-scoped Qwen evals on the harder 6-7 turn setting also completed, so
the hang appears intermittent or setup-specific rather than a permanent Qwen
eval blocker.

### v0.6 6-7 Turn Run-Scoped Evals

These evals are scoped under their source RL run directories so later dataset
assembly can join `linked_rl_run_id`, adapter, env args, and metrics directly:

- `evals/run_t4kf6tmab09foppeih32pvx6/...` for the Qwen 0.8B 4-account /
  6-7-turn run.
- `evals/run_wc5nvpymcd093n8x9c7yedgt/...` for the matched Qwen 2B run.

All four evals use env `abugoot/meta-memory-state@0.6.0`, held-out seed
`424242`, `num_examples=32`, `min_turns=6`, `max_turns=7`, `account_count=4`,
`n=8`, `rollouts_per_example=1`, `temperature=0.7`, `max_tokens=16384`, and
`--skip-upload`.

| Eval | RL Run | Model | Adapter | Reward | Exact Ledger | Exact Turn | Balance Exact | Total Exact | Account Exact | Output Tokens | Result Store |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| base-heldout-6to7-qwen08b-n8 | `t4kf6tmab09foppeih32pvx6` | `Qwen/Qwen3.5-0.8B` | - | `0.651` | `0.36` | `0.00` | `0.02` | `0.04` | `0.465` | `267.9` | `evals/run_t4kf6tmab09foppeih32pvx6/base_heldout_seed424242_4acct_6to7_n8/summary.json` |
| trained-heldout-6to7-qwen08b-n8 | `t4kf6tmab09foppeih32pvx6` | `Qwen/Qwen3.5-0.8B` | `dsg66w80rcjhu3kkv0zpdzve` | `0.862` | `1.00` | `0.06` | `0.32` | `0.12` | `0.765` | `282.6` | `evals/run_t4kf6tmab09foppeih32pvx6/trained_heldout_seed424242_4acct_6to7_n8/summary.json` |
| base-heldout-6to7-qwen2b-n8 | `wc5nvpymcd093n8x9c7yedgt` | `Qwen/Qwen3.5-2B` | - | `0.728` | `0.86` | `0.10` | `0.24` | `0.16` | `0.575` | `268.3` | `evals/run_wc5nvpymcd093n8x9c7yedgt/base_heldout_seed424242_4acct_6to7_n8/summary.json` |
| trained-heldout-6to7-qwen2b-n8 | `wc5nvpymcd093n8x9c7yedgt` | `Qwen/Qwen3.5-2B` | `ym5npd2cye3h2zfey3746say` | `0.955` | `1.00` | `0.42` | `0.70` | `0.46` | `0.910` | `266.0` | `evals/run_wc5nvpymcd093n8x9c7yedgt/trained_heldout_seed424242_4acct_6to7_n8/summary.json` |

Read: the run-scoped evals strengthen the scaling story. Qwen 0.8B improves
from base reward `0.651` to trained `0.862` and fixes ledger formatting, but
exact turn correctness remains very low. Qwen 2B improves from base `0.728` to
trained `0.955`, with exact-turn rate rising from `0.10` to `0.42` and
all-balances-exact turn rate from `0.24` to `0.70`. `solve_all_examples_rate`
is still `0.0` for every cell, so full multi-turn exactness remains unsolved.

## Hosted RL Smoke Results

Run `rdair5n0ca531bxqqvetrok8` completed on June 2, 2026.

Usage:

- Training: `93.99K` tokens, `$0.0056`
- Inference input: `416.08K` tokens, `$0.0083`
- Inference output: `185.40K` tokens, about `$0.01`
- Total: `695.47K` tokens, `$0.03`

Core metrics:

- Reward mean/min/max: `0.0 / 0.0 / 0.0`
- Rewards distribution: all 128 samples in bin `0.000`
- Advantages distribution: all 128 samples in bin `0.000`
- `solve_none`: `1.0`
- `solve_all`: `0.0`
- `effective_batch_size`: `0.0`
- `filters/zero_advantage`: `0.9375`
- `filters/gibberish`: `0.0625`
- `is_truncated`: `0.125`
- Mean sequence length: `661.9`
- Mean prefill length: `252.2`
- Mean decode length: `467.6`
- Mean turns: `3.0`
- Empty rollouts: `0.0`
- Errored rollouts: `0.0`

Artifact quirks:

- 64 rollout samples were logged at step 0.
- `prime train checkpoints` reported no checkpoints, although the logs said a
  final checkpoint was written.

Rollout inspection:

Samples show that Llama 1B often copied the placeholder `account` key from the
required shape instead of using the actual account names. It also tended to emit
many `<ledger>` blocks, wrap outputs in code fences, and place possibly useful
JSON-like balances outside the required tag. This means the first env version
is too format-fragile and/or too hard for Llama 1B to produce useful reward
variance.

## Follow-Up Iterations

### v0.2.0: easier prompt/parser

Changes:

- Replaced the prompt's placeholder `"account": 0` schema with concrete account
  keys.
- Added best-candidate JSON parsing, so JSON-like ledgers outside the preferred
  tag can receive partial credit with a format penalty.
- Added an easier config with two accounts and one to two turns.

Run `mngozs87cvyj745q8zaqph9k` completed for `$0.0080`, but reward stayed all
zero: mean/min/max `0.0`, `solve_none=1.0`, `effective_batch_size=0.0`,
`zero_advantage=0.9766`, truncation `0.0391`. Rollout samples showed outputs
that should sometimes have received shaped partial credit locally, so the next
suspect was the hosted reward interface.

### v0.3.0: answer-signature scoring

Change:

- Updated the reward path to score `completion, answer`, matching the Verifiers
  hosted reward function convention, instead of only the local state-shaped
  helper path.

Run `qh9lqxz5v3s82sjfs03cso8h` completed for `$0.0085`, but reward again stayed
all zero: `zero_advantage=0.9844`, `effective_batch_size=0.0`, truncation
`0.0208`. Manually replaying a stored rollout through the local scorer produced
nonzero reward, which pointed to another mismatch: hosted scoring sees
Verifiers `AssistantMessage` objects, while stored rollouts are serialized to
dicts.

### v0.4.0: message-object-compatible scoring

Change:

- Made `score_completion` accept both dict-shaped messages and Verifiers
  message objects via `getattr(message, "role")` / `getattr(message, "content")`.

Run `msisq47uw7tcnvuxn5aejrbg` completed for `$0.0085` and produced the first
usable reward signal:

- Reward mean/min/max: `0.3426 / 0.2125 / 0.6175`
- Reward distribution: nonzero spread, with bins from `0.000-0.048` through
  `0.912-0.960`
- Advantage distribution: nonzero spread from about `-0.510` to `0.520`
- `effective_batch_size`: `1.0`
- `zero_advantage`: `0.0`
- `gibberish`: `0.0391`
- `is_truncated`: `0.0223`
- Mean sequence length: `291.2`
- Mean prefill/decode length: `140.9 / 150.4`

The run used `--skip-action-check` because the v0.4 Prime integration action
was still marked `RUNNING` after several minutes. The action later completed
`SUCCESS`, so this was a timing workaround rather than a failed integration.
`prime train rollouts` returned no samples for this run even though logs said
64 samples were logged; distributions and metrics were available.

### v0.4.0 50-step follow-up

Run `wpw270lopu0vrzyfx9otn6w1` completed 50 hosted RL steps for `$0.61`.

Usage:

- Training: `5.29M` tokens, `$0.32`
- Inference input: `2.84M` tokens, `$0.06`
- Inference output: `3.95M` tokens, `$0.24`
- Total: `12.08M` tokens, `$0.61`

Reward improved throughout the run:

| Step | Reward Mean | Reward Min/Max | Truncation | Decode Len Mean | Notes |
| ---: | ---: | --- | ---: | ---: | --- |
| 0 | `0.395` | `0.196 / 0.527` | `0.043` | `149.3` | Nonzero signal from the start |
| 10 | `0.572` | `0.445 / 0.792` | `0.196` | `430.3` | Verbosity begins to rise |
| 20 | `0.664` | `0.482 / 0.909` | `0.500` | `674.7` | Many candidate ledgers in samples |
| 30 | `0.719` | `0.558 / 0.892` | `0.917` | `829.2` | High reward with near-token-limit outputs |
| 40 | `0.773` | `0.566 / 0.943` | `0.961` | `762.5` | Samples still mostly answer stuffing |
| 49 | `0.779` | `0.580 / 0.926` | `0.969` | `653.4` | Final metrics; samples available only through step 40 |

The positive result is that the env is trainable: `effective_batch_size` stayed
`1.0`, `zero_advantage` stayed `0.0`, and reward roughly doubled from the first
sampled step to the final metrics.

The negative result is more important for the next iteration. Qualitative
samples at steps 20, 30, and 40 show the model emitting many possible ledgers,
often inside repeated code fences, instead of one clean `<ledger>` answer. Since
v0.4.0 scores the best parseable candidate, the model can improve reward by
answer stuffing. The output-token cost also rose with this behavior, so even a
cheap model can become less cheap when the reward encourages long completions.

Checkpoints were listed at steps 10, 20, 30, and 40:

- `t6r9odwqtqmmb6ttd0qbaqzh` at step 10
- `k0lrv5pt9qlqmozjuonaolud` at step 20
- `j6xr82lpq15wvr5mfkjof8p9` at step 30
- `h2s6hy7gg9o4v3my0q20tden` at step 40

Logs said a final step-50 checkpoint was written, but
`prime train checkpoints` did not list it.

### v0.5.0: anti-stuffing reward and diagnostics

Changes:

- Scoring now selects one ledger candidate instead of taking the maximum score
  over every parseable candidate in the response.
- Multiple parseable candidates, repeated `<ledger>` tags, code fences, and
  long outputs receive multiplicative penalties.
- The environment reports auxiliary Verifiers metrics for parseable turn rate,
  exact one-ledger rate, multi-candidate rate, code-fence rate, mean candidate
  count, and mean output characters.
- Local eval analysis now reports exact-one-candidate and exact-one-ledger
  rates separately from exact-one-tag rate.

Local checks passed:

- `PYTHONDONTWRITEBYTECODE=1 python -B -m unittest discover -s episodes/2026-06-02-meta-memory-state-001/env -p 'test_*.py'`
  ran 16 tests.
- `PYTHONDONTWRITEBYTECODE=1 python -B -m py_compile ...` passed for the env
  source and tests.

Hub env:

- `abugoot/meta-memory-state@0.5.0`
- Content hash: `749c8305`
- Wheel SHA256:
  `b27b8552d6b3f00639afdb4dcff12f2c9b4aedda0a3cc650858ea841f0bd91e0`
- Pushed at approximately `2026-06-02T22:00:49Z`

Base evals on the easy 2-account, 1-2 turn setting completed without runtime
errors. The stricter v0.5 reward drops base reward to about `0.015-0.017`
because only one assistant turn in each 32-example eval produces valid ledger
JSON, but the runs are not fully dead: both train and held-out seeds have one
nonzero example, clean zero truncation, and no multi-candidate behavior.

Hosted Llama 1B launch attempts were blocked by platform/model-path issues:

- Run `ovhe41qu43r1i3gwo98lw0mq` failed before training because hosted renderer
  auto-validation did not map `meta-llama/Llama-3.2-1B-Instruct`; the logs
  suggested an explicit default renderer, but local config rejected a top-level
  `orchestrator` override and Prime rejected `run_config` overrides with HTTP
  403 for this account.
- Switching to `sprints/Llama-3.2-1B-Instruct` failed with an HTTP 400
  free-tier environment requirement check.

The completed v0.5 RL probe therefore used Qwen 0.8B:

- Config:
  `episodes/2026-06-02-meta-memory-state-001/configs/qwen08b_50step_v05.toml`
- Run: `t06x036p2njx21ts5fi5p4vm`
- Dashboard:
  `https://app.primeintellect.ai/dashboard/training/t06x036p2njx21ts5fi5p4vm`
- Model: `Qwen/Qwen3.5-0.8B`
- Steps: 50, batch size `128`, rollouts per example `8`, max tokens `16384`
- Status: completed at `2026-06-02T22:41Z`
- Cost: `1.16M` training tokens, `$0.07`; no inference tokens were charged in
  the run usage table.

Training metrics:

| Step | Reward Mean | Exact One Ledger | Parseable | Multi-Candidate | Code Fence | Truncation | Zero Advantage | Decode Len Mean |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | `0.451` | `0.229` | `0.958` | `0.008` | `0.104` | `0.000` | `0.000` | `36.8` |
| 3 | `0.615` | `0.763` | `1.000` | `0.000` | `0.017` | `0.000` | `0.125` | `39.6` |
| 10 | `0.855` | `0.992` | `0.992` | `0.000` | `0.000` | `0.000` | `0.188` | `49.7` |
| 20 | `0.923` | `0.998` | `1.000` | `0.000` | `0.000` | `0.000` | `0.563` | `52.3` |
| 30 | `0.940` | `1.000` | `1.000` | `0.000` | `0.000` | `0.000` | `0.500` | `42.5` |
| 40 | `0.945` | `0.979` | `1.000` | `0.000` | `0.000` | `0.000` | `0.688` | `43.3` |
| 49 | `0.936` | `0.992` | `1.000` | `0.000` | `0.000` | `0.000` | `0.750` | `43.5` |

Read: v0.5 fixed the candidate-stuffing failure. Output length stayed short,
truncation stayed zero, multi-candidate behavior disappeared, and reward rose
rapidly. The rising zero-advantage filter suggests this easy 2-account setting
is mostly saturated by roughly 20-30 steps, so 50 steps is useful for a curve
but past the efficient learning window.

Qualitative samples show the remaining weakness. At step 10 and step 30 the
model still made subtle two-turn arithmetic/total mistakes while receiving high
partial reward. A step 20 sample also put an extra `"total"` key inside the
`balances` object and still received `0.7625`, revealing that the extra-key
penalty was too small.

Post-run eval/deployment attempts:

- Base Qwen evals through `prime eval run` were attempted at 16K, 512, and a
  tiny 3-example/256-token diagnostic. All hung before creating output
  directories and were killed locally.
- A READY Qwen adapter record was created for the completed run:
  `tipm3xgcydkin391rs5flxm7`, model string
  `Qwen/Qwen3.5-0.8B:tipm3xgcydkin391rs5flxm7`.
- `prime deployments create tipm3xgcydkin391rs5flxm7 --yes --plain` remained
  in `DEPLOYING` for several minutes. One-shot inference returned 404 model not
  found, and `prime deployments delete` refused cleanup while status was
  `DEPLOYING`. A later deployment list showed `DEPLOY_FAILED` with error
  "Deployment timed out after 30 minutes".

### v0.6.0: stricter schema penalty

The env source was bumped to `0.6.0` after inspecting v0.5 rollout samples.
Changes:

- Extra top-level keys and extra keys inside `balances` now contribute to a
  meaningful schema score instead of a tiny extra-account penalty.
- The balance-score weight was reduced from `0.60` to `0.50`; schema score now
  carries `0.15`.
- Unit tests increased from 14 to 16, adding regressions for an extra `"total"`
  key inside `balances` and an extra top-level key.

Hub env:

- `abugoot/meta-memory-state@0.6.0`
- Version ID: `jigzx1ag2fh2mqaibtjld9zd`
- Content hash:
  `790e961cdfdb2817941e56f22c10477c859dcc40b8ce52072b2422953d8e8653`
- Wheel SHA256:
  `7f801e266c7d6660648af91d6646134bbb661eaf1e75612db49720a2e4b60a70`
- Prime integration action: `SUCCESS`
- Pushed at approximately `2026-06-03T00:34:47Z`

The completed v0.6 RL probe used Qwen 0.8B:

- Config:
  `episodes/2026-06-02-meta-memory-state-001/configs/qwen08b_30step_v06.toml`
- Run: `fdzqzv4ridlnhond78eghitd`
- Dashboard:
  `https://app.primeintellect.ai/dashboard/training/fdzqzv4ridlnhond78eghitd`
- Model: `Qwen/Qwen3.5-0.8B`
- Steps: 30, batch size `128`, rollouts per example `8`, max tokens `16384`
- Status: completed at `2026-06-03T00:45Z`
- Cost: `728.46K` training tokens, `$0.04`; no inference tokens were charged in
  the run usage table.

Training metrics:

| Step | Reward Mean | Exact One Ledger | Parseable | Multi-Candidate | Code Fence | Truncation | Zero Advantage | Decode Len Mean |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | `0.543` | `0.238` | `0.988` | `0.000` | `0.164` | `0.000` | `0.000` | `40.9` |
| 3 | `0.735` | `0.772` | - | - | `0.009` | - | - | - |
| 10 | `0.771` | `0.941` | `0.984` | `0.020` | `0.000` | `0.000` | `0.000` | `46.7` |
| 15 | `0.857` | `0.991` | - | - | - | `0.000` | `0.188` | `44.6` |
| 20 | `0.905` | `0.996` | `1.000` | `0.000` | `0.000` | `0.000` | `0.500` | `43.0` |
| 25 | `0.989` | `1.000` | `1.000` | - | - | `0.000` | `0.813` | `46.6` |
| 29 | `0.916` | `1.000` | `1.000` | - | - | `0.000` | `0.750` | `39.5` |

Read: v0.6 preserved the v0.5 anti-stuffing improvement. By step 20, sampled
outputs were cleanly formatted, exactly one-ledger adherence was near 1.0, and
truncation stayed zero. The best step was 25 with reward `0.989`, and the final
step was still high at `0.916`.

The remaining problem is arithmetic fidelity under shaped partial credit. Step
20 samples were usually one clean ledger block, but some still carried wrong
balances or totals while scoring `0.6-0.9`. That makes v0.7 less about output
format and more about whether the reward should separate exact state tracking
from merely close arithmetic.

Post-run eval/deployment attempts:

- Tiny base Qwen eval command:
  `prime eval run abugoot/meta-memory-state@0.6.0 -m Qwen/Qwen3.5-0.8B -n 3 ... --max-tokens 16384`
  hung for about 60 seconds without creating an output directory and was killed.
- Base Llama held-out eval completed on v0.6 with 32 examples, reward `0.0190`,
  truncation `0.0`, parseable turn rate `0.0426`, exact-one-ledger turn rate
  `0.0426`, multi-candidate rate `0.0`, and code-fence rate `0.0`.
- The v0.6 Qwen adapter record `uuntogrnb6um3esp2c5nkk3d` was READY and
  deployable, but `prime deployments create uuntogrnb6um3esp2c5nkk3d --yes --plain`
  immediately left it in `DEPLOY_FAILED` with error "Adapter failed to load.
  Please contact support if this persists."
- A final-adapter retry used config
  `episodes/2026-06-02-meta-memory-state-001/configs/qwen08b_30step_v06_resume_from25_retry.toml`
  to resume from READY step-25 checkpoint `vs01hyx5vxxbn431rb3qj22v` and target
  the same step-30 endpoint.
- Retry run `jspr0dm70xv1nzv2jkz8u8ug` completed for `111.75K` training tokens
  and `$0.0067`. Logged rewards for resumed steps 25-29 were
  `0.9601`, `0.9272`, `0.9383`, `0.9608`, and `0.9587`; truncation stayed
  `0.0`, parseability stayed `1.0`, and final exact-one-ledger was `1.0`.
- The retry produced a fresh READY final adapter `lsbgjt98s0d1nyv5eofomojx`.
  Its first deployment attempt eventually timed out, but a later deployment
  retry on June 3, 2026 succeeded. One-shot inference against
  `Qwen/Qwen3.5-0.8B:lsbgjt98s0d1nyv5eofomojx` returned a normal greeting, so
  the adapter now loads for inference.
- A second final-adapter retry used
  `episodes/2026-06-02-meta-memory-state-001/configs/qwen08b_30step_v06_resume_retry2_from25.toml`
  to resume from the first retry's READY step-25 checkpoint
  `ykoqriy9kluvxwo2zksxwiyi`. Run `pnm7mpulnx3j8y1oyjz2sxwx` generated steps
  25 and 26, then stalled waiting for trainer checkpoint 26. Prime's native
  `train restart` repeated the same stall, so the run was stopped at `$0.0027`.

### Difficulty Ablation: 3 Accounts / 2-3 Turns

Goal: keep the successful Qwen 0.8B v0.6 training setup fixed and vary only env
difficulty, because the easy 2-account / 1-2 turn setting is close to solved.

- Config:
  `episodes/2026-06-02-meta-memory-state-001/configs/qwen08b_30step_v06_diff_3acct_2to3.toml`
- Env args: `seed=1337420`, `num_examples=128`, `min_turns=2`,
  `max_turns=3`, `account_count=3`.
- Run `uvzzmvybz365g0qqgwbo2san` completed on June 3, 2026 for `1.07M`
  training tokens and `$0.06`.
- Reward trajectory at comparison points:
  - Step 0: reward `0.5726`, parseable `0.9507`, exact-one-ledger `0.2208`,
    code-fence `0.1625`, sequence length `267.4`.
  - Step 10: reward `0.8169`, parseable `1.0`, exact-one-ledger `0.9297`,
    code-fence `0.0`, sequence length `273.0`.
  - Step 20: reward `0.8749`, parseable `1.0`, exact-one-ledger `0.9818`,
    code-fence `0.0`, sequence length `268.4`.
  - Step 29: reward `0.9509`, parseable `1.0`, exact-one-ledger `1.0`,
    zero-advantage `0.0625`, sequence length `263.5`.
- Qualitative samples show the useful residual failure mode: formatting is
  clean, but arithmetic/state updates are still wrong on some 3-turn examples.
  For example, at step 20 a sample kept `utilities` at `30` after a credit where
  ground truth was `20`, then propagated the wrong total while still receiving
  reward `0.889`.
- Interpretation: this rung is harder and more informative than the easy
  setting. It does not immediately saturate, sequence length/cost roughly rise,
  and reward is noisy through the middle of training. But by step 29 the small
  model still reaches high reward with clean formatting, so the next difficulty
  rung should increase accounts/turns again before batch-size or model-scaling
  ablations.

### Difficulty Ablation: 3 Accounts / 3-4 Turns

Goal: isolate turn depth by keeping `account_count=3` fixed and increasing from
2-3 turns to 3-4 turns.

- Config:
  `episodes/2026-06-02-meta-memory-state-001/configs/qwen08b_30step_v06_diff_3acct_3to4.toml`
- Env args: `seed=1337420`, `num_examples=128`, `min_turns=3`,
  `max_turns=4`, `account_count=3`.
- First attempt `xvpykb8rxhq1kzg5wtnm9ty6` was stopped after reaching step 1
  and waiting about 5.5 minutes for trainer checkpoint broadcast 1. It cost
  `$0.0052` for `87.45K` training tokens. Step 0 reward was `0.5601`, exact
  one-ledger `0.2979`, parseable `0.9729`, sequence length `337.5`; step 1
  reward was `0.5315`.
- Retry `xn4ncn6hfi6pexy78mtt5cen` completed on June 3, 2026 for `1.41M`
  training tokens and `$0.08`.
- Retry reward trajectory at comparison points:
  - Step 0: reward `0.5657`, parseable `0.9798`, exact-one-ledger `0.1654`,
    code-fence `0.1374`, multi-candidate `0.0020`, sequence length `329.3`.
  - Step 3: reward `0.7553`, exact-one-ledger `0.8132`, multi-candidate
    `0.0137`, truncation `0.0078`, sequence length `649.0`; this was the main
    transient verbosity spike.
  - Step 10: reward `0.8037`, parseable `0.9862`, exact-one-ledger `0.9185`,
    multi-candidate `0.0528`, sequence length `338.3`.
  - Step 20: reward `0.8574`, parseable `1.0`, exact-one-ledger `0.9877`,
    multi-candidate `0.0`, sequence length `324.9`.
  - Step 29: reward `0.8789`, parseable `1.0`, exact-one-ledger `0.9979`,
    multi-candidate `0.0`, sequence length `333.6`, solve-all `0.0`.
- Qualitative step-20 samples are format-clean but still make state/arithmetic
  mistakes. One sample scored `0.859` while carrying `books=-25` after a debit
  where ground truth was `books=-15`, then ending with total `-25` instead of
  `-10`. Another scored `0.753` while badly mishandling a transfer from `rent`
  to `travel`.
- Interpretation: 3-4 turns is a better difficulty rung than 2-3 turns. The
  final reward is lower (`0.879` vs `0.951`), solve-all remains `0.0`, and
  early training briefly reintroduces longer/multi-candidate outputs before
  settling back to clean formatting. This is now a plausible setting for
  model-size or compute/batch ablations.

### Difficulty Ablation: 4 Accounts / 3-4 Turns

Goal: push width one rung higher while keeping the same 3-4 turn depth, Qwen
0.8B model, 30-step budget, batch size, rollout count, and 16K token ceiling.

- Config:
  `episodes/2026-06-02-meta-memory-state-001/configs/qwen08b_30step_v06_diff_4acct_3to4.toml`
- Env args: `seed=1337420`, `num_examples=128`, `min_turns=3`,
  `max_turns=4`, `account_count=4`.
- Run `epzwm0i1cbluvcx27ya4caan` completed on June 3, 2026 for `1.45M`
  training tokens and `$0.09`.
- Reward trajectory at comparison points:
  - Step 0: reward `0.5638`, parseable `0.9715`, exact-one-ledger `0.1917`,
    code-fence `0.1826`, multi-candidate `0.0083`, sequence length `389.6`.
  - Step 5: reward `0.7749`, parseable `0.9906`, exact-one-ledger `0.6469`,
    code-fence `0.0083`, multi-candidate `0.0`, sequence length `358.4`.
  - Step 10: reward `0.8304`, parseable `1.0`, exact-one-ledger `0.9954`,
    code-fence `0.0`, multi-candidate `0.0026`, sequence length `365.1`.
  - Step 20: reward `0.8891`, parseable `1.0`, exact-one-ledger `1.0`,
    code-fence `0.0`, multi-candidate `0.0`, sequence length `364.4`.
  - Step 29: reward `0.8647`, parseable `1.0`, exact-one-ledger `0.9980`,
    code-fence `0.0`, multi-candidate `0.0`, sequence length `381.9`,
    solve-all `0.0`.
- Qualitative step-20 samples are useful because they show high shaped reward
  without exact ledger solving. One 4-turn sample scored `0.939` while totals
  were wrong throughout and the final food balance was wrong. Another scored
  `0.951` with correct balances but wrong totals after the second and third
  updates.
- Interpretation: account width alone did not produce the sharp degradation we
  were looking for. Compared with the 3-account / 3-4-turn retry, final reward
  is only slightly lower (`0.865` vs `0.879`) and final formatting is just as
  clean. The interesting failure is still exact arithmetic/state fidelity under
  shaped partial credit, so the next degradation search should probably increase
  turn depth again, for example 4 accounts with 4-5 turns, or add an exact-state
  auxiliary metric before sweeping model size or batch/rollout count.

### Difficulty Ablation: 4 Accounts / 4-5 Turns

Goal: increase turn depth again after 4 accounts / 3-4 turns still reached
high shaped reward.

The first two attempts kept `batch_size=128`:

- Config:
  `episodes/2026-06-02-meta-memory-state-001/configs/qwen08b_30step_v06_diff_4acct_4to5.toml`
- Env args: `seed=1337420`, `num_examples=128`, `min_turns=4`,
  `max_turns=5`, `account_count=4`.
- Attempt `jvwvglhzbp2h8abmhtkgf6ri` was stopped at step 1 after waiting at
  trainer checkpoint broadcast 1. It cost `$0.0070` for `116.64K` training
  tokens. Step rewards were `0.5703` and `0.6076`.
- Retry `ylzr995pao3587n4xgjnrj1r` repeated the same checkpoint-1 stall and was
  stopped at `$0.0069` for `116.03K` training tokens. Step rewards were
  `0.5985` and `0.5867`.

The successful run used the same env difficulty but reduced the hosted training
batch to `64`:

- Config:
  `episodes/2026-06-02-meta-memory-state-001/configs/qwen08b_30step_v06_diff_4acct_4to5_b64.toml`
- Run `zhc48qkatvucpcaqvsekd9sm` completed on June 3, 2026 for `868.45K`
  training tokens and `$0.05`.
- Reward trajectory:
  - Step 0: reward `0.5661`, parseable `0.9930`, exact-one-ledger `0.2477`,
    code-fence `0.1695`, sequence length `449.0`.
  - Step 5: reward `0.6782`, parseable `0.9672`, exact-one-ledger `0.9141`,
    code-fence `0.0`, sequence length `473.4`.
  - Step 10: reward `0.8144`, parseable `0.9922`, exact-one-ledger `0.9922`,
    code-fence `0.0`, sequence length `440.3`.
  - Step 20: reward `0.8554`, parseable `1.0`, exact-one-ledger `0.9969`,
    code-fence `0.0`, sequence length `433.8`, solve-all `0.0`.
  - Step 29: reward `0.8945`, parseable `1.0`, exact-one-ledger `1.0`,
    code-fence `0.0`, sequence length `425.2`, solve-all `0.0`.
- Qualitative samples still separate shaped reward from exact state tracking.
  At step 20, one sample scored `0.950` while all balances were correct but
  every total was low; another scored `0.925` while totals were wrong and
  `cash` drifted from `15` to `20` after a later turn.
- Interpretation: the batch-128 stalls are probably trainer/batch handling, not
  task difficulty. Batch 64 completes and the model still reaches high shaped
  reward, so 4 accounts / 4-5 turns is not a Qwen 0.8B collapse point under the
  current reward.

### Difficulty Probe: 4 Accounts / 5-6 Turns

Goal: push turn depth again while keeping the run cheap and interpretable. A
batch-64 attempt did not complete a logged rollout batch, so the useful
difficulty read comes from the lighter batch-32 retry rather than from the
stopped attempt.

- Superseded config:
  `episodes/2026-06-02-meta-memory-state-001/configs/qwen08b_30step_v06_diff_4acct_5to6_b64.toml`
- Run `rzu3o8g5dro2qol7qbfbti1y` reached orchestrator step 0 but logged no
  completed step and no usage. This is recorded as an operational attempt, not
  as evidence of model/task failure.

The completed run reduced hosted training batch size to `32` and kept
`rollouts_per_example=8`:

- Config:
  `episodes/2026-06-02-meta-memory-state-001/configs/qwen08b_30step_v06_diff_4acct_5to6_b32.toml`
- Env args: `seed=1337420`, `num_examples=128`, `min_turns=5`,
  `max_turns=6`, `account_count=4`.
- Run `o4qsl2ttfmlnf07bba1uo4qg` completed on June 3, 2026 for `539.65K`
  training tokens and `$0.03`.
- Reward trajectory:
  - Step 0: reward `0.5675`, parseable `0.9688`, exact-one-ledger `0.1875`,
    code-fence `0.1094`, sequence length `534.6`.
  - Step 5: reward `0.6581`, parseable `1.0`, exact-one-ledger `0.9625`,
    code-fence `0.0`, sequence length `519.2`.
  - Step 10: reward `0.7638`, parseable `1.0`, exact-one-ledger `1.0`,
    code-fence `0.0`, sequence length `485.5`.
  - Step 20: reward `0.7772`, parseable `1.0`, exact-one-ledger `1.0`,
    code-fence `0.0`, sequence length `533.0`, solve-all `0.0`.
  - Step 29: reward `0.8483`, parseable `0.9688`, exact-one-ledger `0.9688`,
    code-fence `0.0`, sequence length `541.8`, solve-all `0.0`.
- Qualitative samples: step 20 outputs are clean one-ledger answers, but still
  make state errors on large negative transfers and totals. Two sampled
  rollouts for the same six-turn problem scored `0.854` and `0.897`; both
  missed the large `rent` decrease after transfer-heavy turns, and totals
  drifted even when several balances were correct.
- Interpretation: 4 accounts / 5-6 turns is a clean harder trace rather than a
  collapse. The model learns the output contract and improves shaped reward,
  but exact multi-turn state accounting remains unsolved.

### Difficulty/Scaling Probe: 4 Accounts / 6-7 Turns

Goal: push the same small model until the shaped reward trace shows a real
capability bottleneck, then run the natural next-size Qwen model on the same
config. Both runs used `batch_size=32`, `rollouts_per_example=8`,
`max_tokens=16384`, env version `0.6.0`, seed `1337420`, `num_examples=128`,
`account_count=4`, and `min_turns=6`, `max_turns=7`.

Small-model run:

- Config:
  `episodes/2026-06-02-meta-memory-state-001/configs/qwen08b_30step_v06_diff_4acct_6to7_b32.toml`
- Run `t4kf6tmab09foppeih32pvx6` completed on June 3, 2026 for `2.70M`
  training tokens and `$0.16`.
- Reward trajectory:
  - Step 0: reward `0.5686`, parseable `0.9635`, exact-one-ledger `0.2708`,
    code-fence `0.2760`, sequence length `592.9`.
  - Step 9: reward `0.5145`, exact-one-ledger `0.6324`,
    multi-candidate `0.3092`, repetition filter `0.2500`, truncation `0.2188`,
    prompt-too-long `0.1563`, sequence length `14693.8`.
  - Step 10: reward `0.6754`, exact-one-ledger `0.8314`,
    multi-candidate `0.1048`, repetition filter `0.1563`, truncation `0.1563`,
    sequence length `10497.0`.
  - Step 20: reward `0.8013`, parseable `0.9948`, exact-one-ledger `0.9948`,
    code-fence `0.0`, truncation `0.0`, sequence length `601.2`,
    solve-all `0.0`.
  - Step 29: reward `0.7129`, parseable `0.9911`, exact-one-ledger `0.9911`,
    code-fence `0.0`, truncation `0.0`, sequence length `609.5`,
    solve-all `0.0`.
- Qualitative samples: step 20 samples were clean one-ledger outputs with high
  rewards (`0.918` and `0.908`), but they still made transfer-state and total
  errors. For example, a transfer that should make `books` negative was kept
  positive in a high-reward answer.
- Interpretation: this is the first genuinely useful small-model limit trace
  for the environment. Qwen 0.8B learns the output contract and recovers from a
  bad length/repetition phase, but the harder 6-7 turn depth destabilizes the
  policy mid-run and final shaped reward is lower/noisier.

Matched model-scaling run:

- Config:
  `episodes/2026-06-02-meta-memory-state-001/configs/qwen2b_30step_v06_diff_4acct_6to7_b32.toml`
- Run `wc5nvpymcd093n8x9c7yedgt` completed on June 3, 2026 for `562.68K`
  training tokens and `$0.08`.
- Reward trajectory:
  - Step 0: reward `0.7131`, exact-one-ledger `0.9167`, parseable `0.9688`,
    code-fence `0.2500`, sequence length `601.3`, solve-all `0.0`.
  - Step 10: reward `0.9208`, exact-one-ledger `1.0`, parseable `1.0`,
    code-fence `0.0`, truncation `0.0`, sequence length `575.9`,
    solve-all `0.0`.
  - Step 20: reward `0.9120`, exact-one-ledger `1.0`, parseable `1.0`,
    truncation `0.0`, sequence length `555.5`, solve-all `0.0`.
  - Step 29: reward `0.9568`, exact-one-ledger `1.0`, parseable `1.0`,
    truncation `0.0`, sequence length `578.7`, solve-all `0.0`.
- Qualitative samples: step 20 samples scored `0.992` and `0.996`. They were
  clean and mostly exact, with isolated total errors around turn 5 while final
  balances/totals were otherwise close.
- Interpretation: the next-size model removes the 0.8B length/repetition
  pathology and improves final shaped reward substantially. It also costs less
  overall on this config despite the higher per-token model price, because it
  does not spend a mid-run phase generating near-context-limit outputs.

## Observations

The environment differs from alphabet-sort by requiring arithmetic state
updates, including transfers that modify two accounts at once. Final answers
depend on all prior turns, and the reward can distinguish correct totals from
correct per-account state.

The local `verifiers` package is not installed in the checked runtime, so local
rollout integration was not verified. The scaffold follows the public
alphabet-sort pattern: synthetic `Dataset`, `vf.MultiTurnEnv`, `env_response`,
`@vf.stop`, and `vf.Rubric`. The env was pushed successfully to Prime Hub
through `abugoot/meta-memory-state@0.6.0`, and hosted training integration was
verified by completed Llama and Qwen runs.

Sample generated case:

```json
{
  "num_turns": 2,
  "accounts": ["books", "cash", "food", "rent"],
  "updates": [
    {"kind": "transfer", "from": "books", "to": "cash", "amount": 30},
    {"kind": "transfer", "from": "cash", "to": "rent", "amount": 5}
  ],
  "final": {
    "balances": {"books": -45, "cash": 10, "food": 25, "rent": -10},
    "total": -20
  }
}
```

## Failure Modes

- Parser/reward errors: none in local tests
- Truncation: `12.5%` in hosted smoke; outputs were much longer than expected
- Empty or malformed outputs: scored defensively, no exception in tests
- Zero-advantage filtering: `93.75%`, dominated the smoke run
- Tool-use issues: none, no tools
- Cost/runtime surprises: one-step smoke cost `$0.03`, still cheap but higher
  than the rough `$0.002-$0.01` estimate because decode length was high
- Platform/client issues: TITO rollout path worked; no env errors observed
- Qwen eval/deployment issues: earlier `prime eval run` attempts hung for Qwen
  0.8B on this env, but later run-scoped Qwen 0.8B and 2B evals on the 6-7 turn
  setting completed normally. The v0.5 adapter deployment timed out, and the
  original v0.6 adapter deployment failed to load. A resumed v0.6 retry
  regenerated a fresh final adapter, and a later deployment retry loaded
  successfully for one-shot inference. A second resume/restart attempt stalled
  at trainer checkpoint broadcast 26 and was stopped. The first 3-account /
  3-4-turn ablation attempt also stalled at trainer checkpoint broadcast 1 and
  was stopped, but a fresh
  retry of the same config completed. At 4 accounts / 4-5 turns, two batch-128
  attempts stalled at trainer checkpoint broadcast 1, while the same env args
  completed with batch 64. At 4 accounts / 5-6 turns, a batch-64 attempt logged
  no completed batch, but a batch-32 retry completed; the stopped batch-64
  attempt is therefore not treated as a model/task signal.

## Interpretation

This episode now has a successful first target: the env installs and runs on
Prime, v0.4 produces a non-trivial RL signal cheaply, and a 50-step run shows
real optimization dynamics. The important implementation lesson is that local
reward tests need to mimic hosted Verifiers objects, not only serialized rollout
dicts.

The eval matrix sharpens the research lesson. This is not simply overfitting to
the training seed: same-reward held-out eval reward rises from `0.025` for the
base model to `0.782` for the trained adapter. But the auxiliary metrics move
with it: truncation goes to `1.0`, every assistant turn contains multiple
candidates, and code fences appear in every assistant turn. The learned behavior
generalizes, but it generalizes as a reward exploit made available by the
best-candidate parser.

The v0.5 iteration converts that failure into an explicit experiment. The Qwen
0.8B run answered the main question positively: RL increased exact one-ledger
outputs and reward without pushing output length, candidate count, or truncation
back toward the v0.4 failure mode.

The v0.6 iteration pushed on the remaining schema loophole and confirmed that a
30-step Qwen run is enough to recover high reward on the easy setting for only
`$0.04`. Format behavior is now mostly controlled. The next scientific question
is arithmetic/state correctness: the shaped reward is useful for learning
dynamics, but it can still report high partial reward for ledgers that are
cleanly formatted and close while wrong.

The difficulty ablations make that next question concrete. Three accounts with
2-3 turns still reaches high shaped reward (`0.951`) by step 29. Three accounts
with 3-4 turns is meaningfully harder: the completed retry ends at `0.879`, has
final solve-all `0.0`, and briefly shows a length/multi-candidate spike before
returning to clean outputs. Four accounts with the same 3-4 turn depth costs a
little more and ends slightly lower (`0.865`), but it is not a sharp degradation
point. Four accounts with 4-5 turns at batch 64 still recovers to `0.895`, with
clean formatting and final `solve_all=0.0`, so the shaped reward remains easy
to optimize even when exact accounting is not solved. Four accounts with 5-6
turns at batch 32 also completes cheaply, rising from `0.568` to `0.848`. This
is a better degradation trace: format control is mostly solved, reward improves
substantially, but exact state tracking still never reaches `solve_all`. Four
accounts with 6-7 turns is the first clear small-model stress test: Qwen 0.8B
hits a mid-run length/repetition/multi-candidate spike and ends at only
`0.713`, while the matched Qwen 2B run stays short, clean, and reaches `0.957`.
That makes this rung a good target for future model-size and training-parameter
scaling work.

The run-scoped held-out evals make the result more useful for the meta dataset.
On held-out 4-account / 6-7-turn examples, base Qwen 0.8B scored `0.651` and
the trained 0.8B adapter scored `0.862`; base Qwen 2B scored `0.728` and the
trained 2B adapter scored `0.955`. Formatting improved to exact-one-ledger
`1.0` for both trained adapters. Exactness still lags: trained 0.8B exact-turn
rate is `0.06`, trained 2B exact-turn rate is `0.42`, and all four eval cells
have `solve_all_examples_rate=0.0`.

## Next Steps

1. Use the run-scoped 4-account / 6-7-turn eval grid as the default comparison
   point for future model-size or reward variants.
2. Ask Prime about the Qwen adapter deployment history and resume instability:
   v0.5 timed out, original v0.6 failed to load, the resume-regenerated adapter
   deployed only on retry, and run `pnm7mpulnx3j8y1oyjz2sxwx` stalled twice at
   trainer checkpoint broadcast 26.
3. Consider a v0.7 reward variant that records exact-correct state tracking as
   an auxiliary metric and optionally tightens arithmetic/total penalties.
4. Treat 3 accounts / 3-4 turns, 4 accounts / 3-4 turns, 4 accounts / 4-5
   turns, and 4 accounts / 5-6 turns as useful difficulty traces, with the
   5-6 turn batch-32 run currently the cleanest harder rung.
5. Use 4 accounts / 6-7 turns at batch size 32 as the current scaling target:
   Qwen 0.8B shows the bottleneck, and Qwen 2B gives the first clean scaling
   contrast.
6. Use 20-30 steps as the default cheap Qwen 0.8B probe for this easy setting;
   longer runs are useful only when checking saturation or drift.
7. Next useful follow-up: either run Qwen 4B on the 4-account / 6-7-turn config
   or add stricter exact-state auxiliary metrics/evals before doing more
   learning-rate/batch-size ablations.

## Episode Close-Out

Status: completed on June 3, 2026.

This episode achieved its initial goal: build a deterministic Verifiers env,
push it to Prime Hub, run non-trivial hosted RL, iterate through reward bugs and
reward-hacking failures, and finish with a useful difficulty/model-scaling
dataset. The best current comparison point is 4 accounts / 6-7 turns at batch
32, with run-scoped base/trained held-out evals for Qwen 0.8B and Qwen 2B.

The main research result is not that the task is solved. It is that the episode
now separates three things cleanly: format learning, shaped reward optimization,
and exact state tracking. RL fixes format and improves reward; scaling to Qwen
2B improves exact state metrics; full exact multi-turn solving remains open.
