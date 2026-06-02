# RL Episode Runbook

This runbook is for Codex or another coding agent running one RL research
episode in this repo.

## 1. Set Up The Episode

Choose a short, stable episode ID:

```text
episodes/<date>-<short-env-name>-<question>/
```

Example:

```text
episodes/2026-06-02-alphabet-sort-qwen-cost/
```

Create:

```text
episode.yaml
notebook.md
artifacts.md
configs/
env/ or env_ref.md
```

Use `templates/episode_record.yaml` and `templates/lab_notebook.md`.

Before implementing, claim or update a row in `env_registry.md`.

New envs intended for Prime Hub should use a `meta-` prefix:

```text
meta-<short-env-name>
```

## 2. Define The Research Question

Good questions are narrow:

- Can a small model learn this reward in 20 steps?
- Does tool use improve reward without breaking answer coherence?
- Does a harder curriculum produce reward variance where the base env does not?
- Does a model family fail because of capability, token budget, or client path?

Bad questions are too broad:

- Does RL work?
- Is this model good?
- Can we train reasoning?

## 3. Build Or Select The Environment

For a new Verifiers env, record:

- Package/module name.
- `load_environment` entrypoint.
- Dataset source and split.
- Env args.
- Prompt format.
- Reward functions and weights.
- Parser assumptions.
- Any tool definitions.
- Known reward-hacking risks.
- Cost labels from `env_registry.md`, especially `sandbox` or `judge`.

For a Hub env, record:

- Full ID, version, and dashboard URL.
- Exact env args.
- Why this env is suitable for the episode.

Reward functions should handle missing or malformed outputs defensively. Return
0 or a shaped failure score for bad completions; do not raise on routine model
mistakes such as `content=None`, missing tags, invalid JSON, or no tool call.

Tools are often cheap enough to use when they are central to the experiment.
Sandboxes and judge models are allowed, but they are cost/runtime dependencies
and should be labeled in the registry and episode record.

## 4. Smoke Test Before Hosted RL

Run a tiny eval first when possible:

```bash
prime eval run <env_id_or_config> \
  -m <model> \
  -n 3 -r 1 -c 1 \
  -a '<env_args_json>' \
  --max-tokens <tokens> \
  --abbreviated-summary \
  --plain
```

Look for:

- Non-empty completions.
- Parser/reward errors.
- Truncation.
- Reward range.
- Format compliance.
- Tool-call behavior if relevant.

## 5. Hosted RL Smoke

First hosted run should usually be 1 step:

```toml
model = "meta-llama/Llama-3.2-1B-Instruct"
max_steps = 1
batch_size = 128
rollouts_per_example = 8

[sampling]
max_tokens = 256

[[env]]
id = "<team-or-hub>/<env>"
name = "<episode_env_name>"

[env.args]
# env-specific args
```

Launch:

```bash
prime train configs/<episode>/<smoke>.toml --yes --plain
```

Collect:

```bash
prime train get <run_id> --plain
prime train usage <run_id> --plain
prime train progress <run_id> --plain
prime train metrics <run_id> --plain
prime train logs <run_id> --plain
```

## 6. Model And Token Defaults

Use these as weak starting points, not laws.

### Llama

Start with:

```toml
model = "meta-llama/Llama-3.2-1B-Instruct"

[sampling]
max_tokens = 256
```

Phase 0 result: Llama 1B completed 50 alphabet-sort steps for about $0.084 and
produced clean metrics/checkpoints.

### Qwen

For Qwen, start with a 1-step smoke and a high token ceiling:

```toml
model = "Qwen/Qwen3.5-9B"

[sampling]
max_tokens = 16384
```

Then inspect:

- `is_truncated/*`
- `filters/*/zero_advantage`
- `effective_batch_size/*`
- `reward/*/mean`, min, max
- `decode_len/*/mean`
- logs for `Using token client (TITO)`, `direct renderer`, or `TITO fell back to MITO`
- reward/parser errors involving `content=None`

Observed Phase 0 Qwen behavior:

- Qwen 0.8B at 16K worked and used direct renderer, but this may be platform
  behavior rather than a general model fact.
- Qwen 2B failed at 256, 4096, and 16K on the hosted TITO path.
- Qwen 4B at 16K stalled on TITO/MITO fallback and was stopped.
- Qwen 9B at 16K produced clean completions but solved alphabet-sort too
  uniformly for useful RL signal.
- Qwen 35B-A3B worked at 4096 on alphabet-sort but was verbose and costly.

Recommendation for agents:

- Use Llama 1B for infra and cost probes.
- Use Qwen 9B or Qwen 35B only after a 1-step smoke demonstrates clean reward
  variance and acceptable cost.
- Treat all Qwen results as model/client/env interactions, not pure capability
  measurements.

## 7. Decide Whether To Scale

Scale only if the smoke has:

- No systemic parser/reward exceptions.
- Some reward variance.
- Manageable zero-advantage filtering.
- No or acceptable truncation.
- Cost per step that fits the intended budget.
- Rollouts that look semantically related to the intended behavior.

Suggested scale-up ladder:

```text
1 step -> 5 steps -> 20 steps -> 50+ steps
```

At each stage, update `episode.yaml` and `notebook.md`.

## 8. Record The Episode

Use the schema fields in `templates/episode_record.yaml`.

Do not only report success. Record:

- Failed launches.
- Stalled jobs.
- Unexpected model/client paths.
- Weird billing.
- Reward crashes.
- All-zero or all-one reward distributions.
- Any human interventions such as stopping a run.

This project needs the messy traces.
