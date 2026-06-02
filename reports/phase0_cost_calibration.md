# Phase 0 Cost Calibration

Goal: measure the practical cost and wall-clock behavior of tiny hosted RL runs
before asking subagents to launch independent research tracks.

This phase is intentionally about infrastructure economics, not environment
science. We hold the environment and run shape fixed, then vary only the model.

## Environment Choice

Use `primeintellect/alphabet-sort@latest`.

Reason: public Verifiers environment, no external LLM judge monitor, simple
deterministic reward, and short multi-turn conversations that still exercise
context growth more realistically than a one-shot toy completion.

Avoid `prime/backdoor-ifeval-all` for pure cost calibration because its source
includes an always-on LLM judge monitor. That env is useful later for reward
hacking dynamics, but it can contaminate a clean platform-cost estimate.

## Planned Runs

Current launch constraint: run these serially. These initial probes focused on
platform cost and model/client behavior rather than environment science.

| Run | Config | Model | Steps | Batch | RPE | Max Tokens | Run ID | Status |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| llama1b | `configs/phase0/alphabet_sort_llama1b_50step.toml` | `meta-llama/Llama-3.2-1B-Instruct` | 50 | 128 | 8 | 256 | `nlt9ngv0iwdxg4uy2c01g2c9` | completed |
| qwen08b | `configs/phase0/alphabet_sort_qwen08b_50step.toml` | `Qwen/Qwen3.5-0.8B` | 50 | 128 | 8 | 256 | `tbvax0qzdzki1jj8y17alfoi` | failed at step 0 |
| qwen08b-4096-smoke | `configs/phase0/alphabet_sort_qwen08b_1step_4096.toml` | `Qwen/Qwen3.5-0.8B` | 1 | 128 | 8 | 4096 | `iounbs46ic8rsraa13uaryvi` | completed, reward 0 |
| qwen08b-16384-smoke | `configs/phase0/alphabet_sort_qwen08b_1step_16384.toml` | `Qwen/Qwen3.5-0.8B` | 1 | 128 | 8 | 16384 | `zyqsk5ooaxgs5xz6rq9jkx92` | completed |
| qwen2b | `configs/phase0/alphabet_sort_qwen2b_50step.toml` | `Qwen/Qwen3.5-2B` | 50 | 128 | 8 | 256 | `dlhv80061cjijtkhif6t8xnc` | failed at step 0 |
| qwen2b-4096-smoke | `configs/phase0/alphabet_sort_qwen2b_1step_4096.toml` | `Qwen/Qwen3.5-2B` | 1 | 128 | 8 | 4096 | `q66ojbgotyo0whecdvws2nxz` | failed at step 0 |
| qwen2b-16384-smoke | `configs/phase0/alphabet_sort_qwen2b_1step_16384.toml` | `Qwen/Qwen3.5-2B` | 1 | 128 | 8 | 16384 | `b3kwqzaz7ssfnyk0j7dwgm3w` | failed at step 0 |
| qwen4b-16384-smoke | `configs/phase0/alphabet_sort_qwen4b_1step_16384.toml` | `Qwen/Qwen3.5-4B` | 1 | 128 | 8 | 16384 | `gal6c45tijbqukm36hvnyu7b` | stopped, stalled |
| qwen9b-16384-smoke | `configs/phase0/alphabet_sort_qwen9b_1step_16384.toml` | `Qwen/Qwen3.5-9B` | 1 | 128 | 8 | 16384 | `lxz6blxwehmu05derroag8io` | completed |
| qwen35b-a3b | `configs/phase0/alphabet_sort_qwen35b_a3b_50step.toml` | `Qwen/Qwen3.5-35B-A3B` | 50 | 128 | 8 | 256 | `qy0tbppmiyj09p7neno44ptz` | failed at step 0 |
| qwen35b-a3b-4096-smoke | `configs/phase0/alphabet_sort_qwen35b_a3b_1step_4096.toml` | `Qwen/Qwen3.5-35B-A3B` | 1 | 128 | 8 | 4096 | `sjj16q81sb2rgpx8zh2g7vgr` | completed |

## Launch Commands

```bash
prime train configs/phase0/alphabet_sort_llama1b_50step.toml --plain
prime train configs/phase0/alphabet_sort_qwen08b_50step.toml --plain
prime train configs/phase0/alphabet_sort_qwen08b_1step_4096.toml --yes --plain
prime train configs/phase0/alphabet_sort_qwen08b_1step_16384.toml --yes --plain
prime train configs/phase0/alphabet_sort_qwen2b_50step.toml --plain
prime train configs/phase0/alphabet_sort_qwen2b_1step_4096.toml --yes --plain
prime train configs/phase0/alphabet_sort_qwen2b_1step_16384.toml --yes --plain
prime train configs/phase0/alphabet_sort_qwen4b_1step_16384.toml --yes --plain
prime train configs/phase0/alphabet_sort_qwen9b_1step_16384.toml --yes --plain
prime train configs/phase0/alphabet_sort_qwen35b_a3b_50step.toml --plain
prime train configs/phase0/alphabet_sort_qwen35b_a3b_1step_4096.toml --yes --plain
```

## Collection Checklist

After each run, collect:

| Field | Source |
| --- | --- |
| `run_id` | `prime train list --plain` |
| status/timestamps | `prime train get <run_id> --plain` |
| final usage/cost | `prime train usage <run_id> --plain` |
| latest step/sample steps | `prime train progress <run_id> --plain` |
| checkpoint cadence | `prime train checkpoints <run_id> --plain` |
| train metrics summary | `prime train metrics <run_id> --plain` |
| representative rollouts | `prime train rollouts <run_id> --step <step> --plain` |
| wall time | derived from timestamps |
| cost per step | usage cost / completed steps |
| cost per rollout | usage cost / completed training rollouts |
| avg input/output tokens | usage and/or metrics output |
| notes | queue delays, failures, output length drift, weird model behavior |

## Derived Starter Rules

Interim rules from the first calibration runs:

| Model | Cost | Wall Time | Cost / Step | Cost / Rollout | Avg Output Tokens | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `meta-llama/Llama-3.2-1B-Instruct` | $0.0836 | 13 min started-to-completed | $0.00167 | $0.000013 | 35.8 inference output tokens/rollout | 50 steps, 6400 rollouts, no errors, final step reward 0.676, no final-step truncation |
| `Qwen/Qwen3.5-0.8B` | $0.0020 | 6 min to failure | n/a | n/a | n/a | Failed before completing step 0; reward saw `None` content and zero-advantage filtering discarded all rollouts |
| `Qwen/Qwen3.5-0.8B`, 4096-token cap | $0.0031 | 1 min total / 3.1s step | $0.0031 | $0.000024 billed per nominal rollout | 23.4 decode tokens/sample | Completed but no useful signal: reward 0, solve_none 1.0, 99.2% zero-advantage filtering |
| `Qwen/Qwen3.5-0.8B`, 16384-token cap | $0.0006 | 1 min total / 11.6s step | $0.0006 | $0.000005 billed per nominal rollout | 22.6 decode tokens/sample | Completed with useful signal: reward 0.434, 6.25% zero-advantage filtering; used direct renderer path |
| `Qwen/Qwen3.5-2B` | $0.0045 | 2 min to failure | n/a | n/a | n/a | Same hosted-training failure as Qwen 0.8B; tiny eval probe works normally outside hosted training |
| `Qwen/Qwen3.5-2B`, 4096-token cap | $0.0049 | 1 min to failure | n/a | n/a | n/a | Still failed: all three attempts 128/128 zero-advantage and `weighted_reward` saw `None` content |
| `Qwen/Qwen3.5-2B`, 16384-token cap | $0.0044 | 1 min to failure | n/a | n/a | n/a | Still failed on TITO: all three attempts 128/128 zero-advantage and `weighted_reward` saw `None` content |
| `Qwen/Qwen3.5-4B`, 16384-token cap | $0.09 | 9 min until manual stop | n/a | n/a | n/a | Stalled on TITO/MITO fallback with 123 active env tasks; stopped to unblock serial queue |
| `Qwen/Qwen3.5-9B`, 16384-token cap | $0.56 | 3 min total / 76.7s step | $0.56 | $0.0044 billed per nominal rollout | 1919.2 decode tokens/sample | Completed, reward 1.0, no truncation; too easy for RL signal on this env (99.2% zero-advantage filtering) |
| `Qwen/Qwen3.5-35B-A3B`, 256-token cap | $0.11 | 1 min to failure | n/a | n/a | n/a | Same `content=None` failure, but with much higher output usage from native thinking |
| `Qwen/Qwen3.5-35B-A3B`, 4096-token cap | $0.61 | 3 min total / 79.8s step | $0.61 | $0.0048 billed per nominal rollout | 1677.3 decode tokens/sample | 1-step hosted smoke completed; reward 0.943, but 62.5% zero-advantage filtering and 5.5% truncation |

## Hosted Model Price Chart

Source: `prime train models --plain` on 2026-06-02. Prices are per 1M tokens.
All listed models report 64K context windows.

| Model | Input | Output | Train |
| --- | ---: | ---: | ---: |
| `Qwen/Qwen3.5-0.8B` | $0.02 | $0.06 | $0.06 |
| `Qwen/Qwen3.5-2B` | $0.05 | $0.15 | $0.15 |
| `Qwen/Qwen3.5-4B` | $0.10 | $0.30 | $0.30 |
| `Qwen/Qwen3.5-9B` | $0.20 | $0.60 | $0.60 |
| `Qwen/Qwen3.5-35B-A3B` | $0.25 | $0.75 | $1.00 |
| `Qwen/Qwen3.5-122B-A10B` | $0.50 | $1.50 | $2.00 |
| `Qwen/Qwen3.5-397B-A17B` | $1.00 | $3.00 | $4.00 |
| `Qwen/Qwen3.6-35B-A3B` | $0.25 | $0.75 | $1.00 |
| `meta-llama/Llama-3.2-1B-Instruct` | $0.02 | $0.06 | $0.06 |
| `meta-llama/Llama-3.2-3B-Instruct` | $0.05 | $0.15 | $0.15 |

Cost projection using the successful 35B 4096-token smoke token mix
(229.19K train, 36.65K input, 496.75K output for one 128-rollout step):

| Model | Projected 1-Step Cost | Projected 10 Steps | Caveat |
| --- | ---: | ---: | --- |
| `Qwen/Qwen3.5-0.8B` | $0.044 projected / $0.0006 observed at 16K | $0.44 projected | 16K smoke worked and produced reward distribution, apparently because it used direct renderer rather than TITO |
| `Qwen/Qwen3.5-2B` | $0.111 projected / $0.0044 observed to failure at 16K | $1.11 projected | 16K smoke still failed on TITO/content path |
| `Qwen/Qwen3.5-4B` | $0.222 projected / $0.09 observed before stop | $2.22 projected | 16K smoke stalled on TITO/MITO fallback; not recommended until retried or Prime clarifies client behavior |
| `Qwen/Qwen3.5-9B` | $0.443 projected / $0.56 observed at 16K | $4.43 projected / ~$5.6 observed if linear | 16K smoke completed and solved, but this env was too easy for RL signal |
| `Qwen/Qwen3.5-35B-A3B` | $0.611 | $6.11 | Observed at 1 step; 10-15 steps is a safer starter range than 50 |

## Llama 1B Result

Run: `nlt9ngv0iwdxg4uy2c01g2c9`

Dashboard: <https://app.primeintellect.ai/dashboard/training/nlt9ngv0iwdxg4uy2c01g2c9>

Status:

- Created: 2026-06-02 15:18
- Started: 2026-06-02 15:19
- Completed: 2026-06-02 15:32
- Latest step: 49
- Steps with samples/distributions: 0, 10, 20, 30, 40

Usage:

| Bucket | Tokens | Cost | Price / Mtok |
| --- | ---: | ---: | ---: |
| Training | 888,295 | $0.0531 | $0.06 |
| Inference input | 845,995 | $0.0169 | $0.02 |
| Inference output | 229,251 | $0.0138 | $0.06 |
| Total | 1,963,541 | $0.0836 | - |

Derived:

| Quantity | Value |
| --- | ---: |
| Training rollouts | 6,400 |
| Total cost / step | $0.00167 |
| Total cost / rollout | $0.000013 |
| Total tokens / step | 39,271 |
| Total tokens / rollout | 306.8 |
| Training tokens / rollout | 138.8 |
| Inference input tokens / rollout | 132.2 |
| Inference output tokens / rollout | 35.8 |

Selected metrics:

| Metric | Step 0 | Step 49 |
| --- | ---: | ---: |
| reward/all/mean | 0.251 | 0.676 |
| metrics/alphabet_sort_cost_probe/num_turns | 1.000 | 1.063 |
| decode_len/all/mean | 21.4 | 27.7 |
| prefill_len/all/mean | 78.7 | 85.9 |
| seq_len/all/mean | 100.1 | 113.6 |
| is_truncated/all/mean | 0.000 | 0.000 |
| empty_rollouts/all | 0.000 | 0.000 |
| errored_rollouts/all | 0.000 | 0.000 |
| solve_all/all | 0.000 | 0.500 |
| solve_none/all | 0.125 | 0.000 |

Checkpoints:

| Step | Checkpoint ID | Status | Size |
| ---: | --- | --- | ---: |
| 10 | `lc62svt9mkbod1jazusqb5in` | READY | 180,717,305 bytes |
| 20 | `ucrfum7h6j04u38yetgy2x6z` | READY | 180,717,305 bytes |
| 30 | `momj7ojojcpdydrv737qmsh1` | READY | 180,717,305 bytes |
| 40 | `uaptmxryr5ckvtbbdwqdjpgk` | READY | 180,717,305 bytes |
| 50 | `b5ms983px2dgr1udnehr5d6g` | UPLOADING | TBD |

Notes:

- Actual cost was far below the $10 target: roughly eight cents for this 50-step
  run.
- The short-output env makes `max_tokens=256` mostly irrelevant for this model;
  output averaged only 35.8 inference output tokens per rollout across the run.
- Cost appears easy to scale linearly for similar short-output single/multi-turn
  envs: a comparable 100-step Llama 1B run would be around $0.17 before any
  eval overhead.
- This is not a good proxy for tool-heavy or verbose reasoning envs; those need
  a separate token-growth probe.
- Step-40 rollout samples were available and showed clean XML-tagged sorting
  completions, often with reward 1.0.

## Qwen 0.8B Result

Run: `tbvax0qzdzki1jj8y17alfoi`

Dashboard: <https://app.primeintellect.ai/dashboard/training/tbvax0qzdzki1jj8y17alfoi>

Status:

- Created: 2026-06-02 16:03
- Started: 2026-06-02 16:03
- Completed: 2026-06-02 16:09
- Status: FAILED
- Latest step: none
- Checkpoints: none

Usage:

| Bucket | Tokens | Cost | Price / Mtok |
| --- | ---: | ---: | ---: |
| Training | 0 | $0.0000 | $0.06 |
| Inference input | 45,197 | $0.0009 | $0.02 |
| Inference output | 18,090 | $0.0011 | $0.06 |
| Total | 63,287 | $0.0020 | - |

Failure:

- Prime failure analysis reports `BackoffLimitExceeded`.
- Root cause: the `primeintellect/alphabet-sort@0.1.12` reward function raised
  `expected string or bytes-like object, got 'NoneType'` for every rollout.
- All 128 rollouts at step 0 had zero advantage, so the zero-advantage filter
  discarded the full batch on 3 consecutive attempts and crashed the run.
- Logs show Qwen used the token-in-token-out client:
  `Using token client (TITO) for rollouts - server-side templating`.
- No training tokens were billed; the failed probe cost only inference for the
  attempted batches.

Read:

`Qwen/Qwen3.5-0.8B` is not a drop-in cost-probe default for this env/config.
This may be a model/client serialization issue, an environment parser/reward
robustness issue for `None` assistant content, or an interaction between Qwen
TITO rollouts and the alphabet-sort environment. For subagent defaults, prefer
the Llama 1B baseline unless a Qwen-family comparison is specifically needed and
has passed a smoke run.

## Qwen 2B Result

Run: `dlhv80061cjijtkhif6t8xnc`

Dashboard: <https://app.primeintellect.ai/dashboard/training/dlhv80061cjijtkhif6t8xnc>

Status:

- Created: 2026-06-02 16:13
- Started: 2026-06-02 16:13
- Completed: 2026-06-02 16:15
- Status: FAILED
- Latest step: none
- Checkpoints: none

Usage:

| Bucket | Tokens | Cost | Price / Mtok |
| --- | ---: | ---: | ---: |
| Training | 0 | $0.0000 | $0.15 |
| Inference input | 44,581 | $0.0022 | $0.05 |
| Inference output | 15,397 | $0.0023 | $0.15 |
| Total | 59,978 | $0.0045 | - |

Failure:

- Same pattern as Qwen 0.8B.
- Prime failure analysis reports `BackoffLimitExceeded`.
- Root cause: `weighted_reward` in `primeintellect/alphabet-sort@0.1.12`
  repeatedly raised `expected string or bytes-like object, got 'NoneType'`.
- All 128 rollouts at step 0 had zero advantage and were filtered on all 3
  attempts.
- Logs again show the Qwen training path using the token-in-token-out client:
  `Using token client (TITO) for rollouts - server-side templating`.

Verification eval:

To check whether Qwen 2B fails on the environment in general, we ran a tiny
normal eval with the same Hub env/version/args:

```bash
prime eval run primeintellect/alphabet-sort@0.1.12 \
  -m Qwen/Qwen3.5-2B \
  -n 3 -r 1 -c 1 \
  -a '{"min_turns":1,"max_turns":2,"min_names_per_turn":1,"max_names_per_turn":4,"similarity_power":4,"power_per_turn":true,"seed":1337420}' \
  --max-tokens 256 \
  --abbreviated-summary \
  --plain
```

Eval ID: `qtkismw4yazzg1yn6e8euthq`

Result:

| Metric | Value |
| --- | ---: |
| avg reward | 0.242 |
| rewards | 0.49, 0.175, 0.06 |
| avg num turns | 1.667 |
| avg input tokens | 160 |
| avg output tokens | 40 |
| truncation | 0 |

Read:

Qwen 2B can produce non-empty, scored completions for `alphabet-sort` under
normal `prime eval run`. The hosted-training failure is therefore not evidence
that the env is globally broken or that the model cannot answer the task. The
most likely culprit is the Qwen hosted-training TITO/server-side templating path
returning assistant messages with `content=None`, combined with an environment
reward that does not defensively handle `None` content. For our own envs, reward
functions should treat missing/None assistant content as score 0 rather than
raising.

## Smaller Qwen 4096-Token Smokes

Question: did the smaller hosted Qwen failures happen only because
`max_tokens=256` was too low, as with Qwen 35B?

### Qwen 0.8B at 4096

Run: `iounbs46ic8rsraa13uaryvi`

Config: `configs/phase0/alphabet_sort_qwen08b_1step_4096.toml`

Dashboard: <https://app.primeintellect.ai/dashboard/training/iounbs46ic8rsraa13uaryvi>

Status:

- Created: 2026-06-02 16:54
- Started: 2026-06-02 16:54
- Completed: 2026-06-02 16:55
- Status: COMPLETED
- Latest step: 0

Usage:

| Bucket | Tokens | Cost | Price / Mtok |
| --- | ---: | ---: | ---: |
| Training | 10,480 | $0.0006 | $0.06 |
| Inference input | 57,470 | $0.0011 | $0.02 |
| Inference output | 21,970 | $0.0013 | $0.06 |
| Total | 89,920 | $0.0031 | - |

Selected metrics:

| Metric | Value |
| --- | ---: |
| reward/all/mean | 0.000 |
| decode_len/all/mean | 23.4 |
| seq_len/all/mean | 81.9 |
| is_truncated/all/mean | 0.000 |
| solve_none/all | 1.000 |
| filters/all/zero_advantage | 0.992 |
| effective_batch_size/all | 0.000 |
| time/step | 3.1s |

Read:

The 4096-token cap prevented a hard crash, but it did not create a useful
training signal. The run only completed because the third attempt had 1 rollout
that escaped the enforced filters; reward was still 0 across the accepted batch.
Qwen 0.8B is therefore cheap but not a good default model for this env.

### Qwen 2B at 4096

Run: `q66ojbgotyo0whecdvws2nxz`

Config: `configs/phase0/alphabet_sort_qwen2b_1step_4096.toml`

Dashboard: <https://app.primeintellect.ai/dashboard/training/q66ojbgotyo0whecdvws2nxz>

Status:

- Created: 2026-06-02 16:56
- Started: 2026-06-02 16:56
- Completed: 2026-06-02 16:57
- Status: FAILED
- Latest step: none

Usage:

| Bucket | Tokens | Cost | Price / Mtok |
| --- | ---: | ---: | ---: |
| Training | 0 | $0.0000 | $0.15 |
| Inference input | 48,220 | $0.0024 | $0.05 |
| Inference output | 16,590 | $0.0025 | $0.15 |
| Total | 64,810 | $0.0049 | - |

Failure:

- Same failure as the original 256-token run: `weighted_reward` received
  `None` content and raised `TypeError`.
- All three step-0 attempts had 128/128 zero-advantage rollouts, so the
  orchestrator crashed with `BackoffLimitExceeded`.
- Output use stayed short despite the larger ceiling, so Qwen 2B is not simply
  a "needs more thinking tokens" case on this env/training path.

Read:

Raising the token ceiling is not enough to make Qwen 2B usable in hosted RL on
`alphabet-sort`. Since Qwen 2B worked in local `prime eval run` at 256, the
remaining culprit is likely the hosted TITO/content path plus this env's
non-defensive reward parser, not raw model incapability.

## Qwen 16K Ladder

Question: should agent guidance simply say "use `max_tokens=16384` for Qwen"?

Short answer: use 16K for Qwen smoke tests, but do not assume it fixes every
Qwen model or gives a trainable RL signal. It fixes some failure modes and
exposes different ones.

| Model | Run ID | Status | Cost | Reward | Decode Mean | Filtering | Client Path / Read |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `Qwen/Qwen3.5-0.8B` | `zyqsk5ooaxgs5xz6rq9jkx92` | completed | $0.0006 | 0.434 | 22.6 | 6.25% zero-advantage | Switched to direct renderer; usable signal and very cheap |
| `Qwen/Qwen3.5-2B` | `b3kwqzaz7ssfnyk0j7dwgm3w` | failed | $0.0044 | n/a | n/a | 128/128 zero-advantage on 3 attempts | Stayed on TITO; 16K did not fix `content=None` |
| `Qwen/Qwen3.5-4B` | `gal6c45tijbqukm36hvnyu7b` | stopped | $0.09 | n/a | n/a | n/a | Stayed on TITO, spent 307K output tokens, then stalled with 123 active env tasks; manually stopped |
| `Qwen/Qwen3.5-9B` | `lxz6blxwehmu05derroag8io` | completed | $0.56 | 1.000 | 1919.2 | 99.2% zero-advantage | Stayed on TITO; solved task, no truncation, but task too easy for useful RL signal |
| `Qwen/Qwen3.5-35B-A3B` | `sjj16q81sb2rgpx8zh2g7vgr` | completed | $0.61 | 0.943 | 1677.3 | 62.5% zero-advantage | Worked at 4096 already; 16K not tested because 4096 was sufficient |

### Qwen 0.8B at 16K

Run: `zyqsk5ooaxgs5xz6rq9jkx92`

Config: `configs/phase0/alphabet_sort_qwen08b_1step_16384.toml`

Dashboard: <https://app.primeintellect.ai/dashboard/training/zyqsk5ooaxgs5xz6rq9jkx92>

Status:

- Created: 2026-06-02 17:02
- Started: 2026-06-02 17:03
- Completed: 2026-06-02 17:04
- Status: COMPLETED
- Latest step: 0

Usage:

| Bucket | Tokens | Cost | Price / Mtok |
| --- | ---: | ---: | ---: |
| Training | 10,250 | $0.0006 | $0.06 |
| Inference input | 0 | $0.0000 | $0.02 |
| Inference output | 0 | $0.0000 | $0.06 |
| Total | 10,250 | $0.0006 | - |

Selected metrics:

| Metric | Value |
| --- | ---: |
| reward/all/mean | 0.434 |
| decode_len/all/mean | 22.6 |
| seq_len/all/mean | 80.1 |
| is_truncated/all/mean | 0.000 |
| solve_none/all | 0.0625 |
| filters/all/zero_advantage | 0.0625 |
| effective_batch_size/all | 0.9375 |
| time/step | 11.6s |

Logs:

- `Initialized Qwen35Renderer for Qwen/Qwen3.5-0.8B`
- `Using direct renderer rollout client`

Read:

This is the first small-Qwen run that produced a real reward distribution on
hosted RL. It did not need the full 16K budget; the important difference appears
to be the rollout client path, not output length.

### Qwen 2B at 16K

Run: `b3kwqzaz7ssfnyk0j7dwgm3w`

Config: `configs/phase0/alphabet_sort_qwen2b_1step_16384.toml`

Dashboard: <https://app.primeintellect.ai/dashboard/training/b3kwqzaz7ssfnyk0j7dwgm3w>

Status:

- Created: 2026-06-02 17:05
- Started: 2026-06-02 17:05
- Completed: 2026-06-02 17:06
- Status: FAILED
- Latest step: none

Usage:

| Bucket | Tokens | Cost | Price / Mtok |
| --- | ---: | ---: | ---: |
| Training | 0 | $0.0000 | $0.15 |
| Inference input | 43,610 | $0.0022 | $0.05 |
| Inference output | 14,750 | $0.0022 | $0.15 |
| Total | 58,360 | $0.0044 | - |

Read:

Qwen 2B stayed on the TITO/server-side-templating path and failed exactly like
the 4096-token run. All three attempts had 128/128 zero-advantage rollouts and
`weighted_reward` repeatedly received `None` content. For this env, 16K alone
does not make Qwen 2B a usable hosted RL target.

### Qwen 4B at 16K

Run: `gal6c45tijbqukm36hvnyu7b`

Config: `configs/phase0/alphabet_sort_qwen4b_1step_16384.toml`

Dashboard: <https://app.primeintellect.ai/dashboard/training/gal6c45tijbqukm36hvnyu7b>

Status:

- Created: 2026-06-02 17:08
- Started: 2026-06-02 17:08
- Stopped: 2026-06-02 17:17
- Status: STOPPED
- Latest step: none

Usage before stop:

| Bucket | Tokens | Cost | Price / Mtok |
| --- | ---: | ---: | ---: |
| Training | 0 | $0.0000 | $0.30 |
| Inference input | 10,390 | $0.0010 | $0.10 |
| Inference output | 307,200 | $0.0922 | $0.30 |
| Total | 317,590 | $0.0932 | - |

Read:

Qwen 4B stayed on TITO and repeatedly fell back to MITO on turn 2. After
spending 307K output tokens, the run sat for minutes with 123 active env tasks,
no step metrics, and no further usage movement, so it was manually stopped to
unblock the serial queue. Treat this as an infrastructure/model-client stall,
not a completed cost estimate.

### Qwen 9B at 16K

Run: `lxz6blxwehmu05derroag8io`

Config: `configs/phase0/alphabet_sort_qwen9b_1step_16384.toml`

Dashboard: <https://app.primeintellect.ai/dashboard/training/lxz6blxwehmu05derroag8io>

Status:

- Created: 2026-06-02 17:17
- Started: 2026-06-02 17:17
- Completed: 2026-06-02 17:20
- Status: COMPLETED
- Latest step: 0

Usage:

| Bucket | Tokens | Cost | Price / Mtok |
| --- | ---: | ---: | ---: |
| Training | 261,510 | $0.1569 | $0.60 |
| Inference input | 36,420 | $0.0073 | $0.20 |
| Inference output | 656,580 | $0.3939 | $0.60 |
| Total | 954,510 | $0.5581 | - |

Selected metrics:

| Metric | Value |
| --- | ---: |
| reward/all/mean | 1.000 |
| decode_len/all/mean | 1919.2 |
| seq_len/all/mean | 1636.0 |
| is_truncated/all/mean | 0.000 |
| solve_all/all | 1.000 |
| filters/all/zero_advantage | 0.992 |
| effective_batch_size/all | 0.000 |
| time/step | 76.7s |

Read:

Qwen 9B works as a capability smoke at 16K: it produced content, scored cleanly,
and did not truncate. But it solved the env so uniformly that this specific
alphabet-sort configuration has almost no RL training signal for Qwen 9B. For
agent guidance, Qwen 9B is a reasonable first Qwen capability probe if the env
is harder than this toy sorting setup; otherwise it may be too strong.

## Qwen 35B-A3B Diagnosis

Initial failed run: `qy0tbppmiyj09p7neno44ptz`

Dashboard: <https://app.primeintellect.ai/dashboard/training/qy0tbppmiyj09p7neno44ptz>

Status:

- Created: 2026-06-02 16:35
- Started: 2026-06-02 16:35
- Completed: 2026-06-02 16:36
- Status: FAILED
- Latest step: none
- Checkpoints: none

Usage:

| Bucket | Tokens | Cost | Price / Mtok |
| --- | ---: | ---: | ---: |
| Training | 0 | $0.0000 | $1.00 |
| Inference input | 38,848 | $0.0097 | $0.25 |
| Inference output | 130,904 | $0.0982 | $0.75 |
| Total | 169,752 | $0.1079 | - |

Failure:

- Same structural failure as the smaller hosted Qwen runs: `weighted_reward`
  received `None` assistant content and raised `TypeError`.
- Prime failure analysis reports `BackoffLimitExceeded`: all 128 rollouts had
  zero advantage for all 3 step-0 attempts.
- Logs confirm this run used the Qwen token-in-token-out training path:
  `Using token client (TITO) for rollouts - server-side templating`.
- The output-token bill is diagnostic. The run spent 130,904 output tokens on
  failed step-0 attempts despite a 256-token cap, consistent with Qwen spending
  the budget in native `reasoning_content` across 1-2 assistant turns and never
  reaching final `content`.

Eval probes:

| Probe | Eval ID | Max Tokens | Result |
| --- | --- | ---: | --- |
| default thinking | `sen167ojgvsr0pp30waz4p50` | 256 | Failed/zero reward; avg output 256, truncation 1.0, `content=None` caused follow-up API errors |
| attempted no-thinking flag | `v76s21klz4l9stqexuc4z5lr` | 256 | Invalid for this provider/client path: `AsyncCompletions.create()` rejected `enable_thinking` as an unexpected kwarg |
| default thinking | `tycuwaku9aypczw3wmnl111y` | 4096 | Worked: reward 1.0 on 3/3 examples, no truncation, avg output 1375.3 tokens |

Hosted RL smoke run with larger cap: `sjj16q81sb2rgpx8zh2g7vgr`

Config: `configs/phase0/alphabet_sort_qwen35b_a3b_1step_4096.toml`

Dashboard: <https://app.primeintellect.ai/dashboard/training/sjj16q81sb2rgpx8zh2g7vgr>

Status:

- Created: 2026-06-02 16:46
- Started: 2026-06-02 16:46
- Completed: 2026-06-02 16:49
- Status: COMPLETED
- Latest step: 0
- Checkpoints: none

Usage:

| Bucket | Tokens | Cost | Price / Mtok |
| --- | ---: | ---: | ---: |
| Training | 229,190 | $0.2292 | $1.00 |
| Inference input | 36,650 | $0.0092 | $0.25 |
| Inference output | 496,750 | $0.3726 | $0.75 |
| Total | 762,600 | $0.6110 | - |

Selected step-0 metrics:

| Metric | Value |
| --- | ---: |
| reward/all/mean | 0.943 |
| seq_len/all/mean | 1542.5 |
| decode_len/all/mean | 1677.3 |
| prefill_len/all/mean | 113.3 |
| is_truncated/all/mean | 0.0547 |
| num_turns/all/mean | 1.3125 |
| solve_all/all | 0.625 |
| filters/all/zero_advantage | 0.625 |
| effective_batch_size/all | 0.375 |
| time/step | 79.8s |

Read:

The failed 35B run was a token-budget/thinking-channel issue, not evidence that
the model or env was incapable. Capital-Q Qwen 35B with native thinking needs a
much larger generation cap even for a short-format task. However, the larger cap
changes the economics dramatically: this 1-step smoke cost $0.61 and included
one fully discarded all-zero attempt before a usable batch. A 50-step run at this
shape could plausibly land in the tens of dollars, so a larger-model starter run
should be closer to 10-15 steps unless the env first reduces verbosity or
supports a provider-compatible no-thinking setting.

## Open Questions

- Why did Qwen 0.8B at 16K use the direct renderer path while Qwen 2B/4B/9B
  used TITO? Is there a supported config knob to choose the rollout client?
- Is the small/mid-Qwen `content=None` behavior specific to `alphabet-sort` with
  TITO/server-side templating and a non-defensive reward, or does it appear on
  other environments too?
- Would a difficulty-adjusted alphabet-sort variant give Qwen 9B non-uniform
  rewards, or is it simply too strong for this env family?
- Are checkpoint/adaptor artifacts produced on a cadence that is useful for
  very short runs?
- Is a 50-step run enough to estimate cost linearly for 5/20/100-step variants?
- Should the subagent default be Llama 1B for cheap probes, with Qwen 9B or 35B
  reserved for capability probes after a one-step 16K smoke test?
