# RL Episode Agent Brief

You are running one small RL research episode for the meta-learning corpus.
Your job is to build or adapt one Verifiers environment, run cheap diagnostics,
launch at most small hosted RL probes, and leave a complete record.

## Mission

Create one useful episode of RL research evidence:

1. Pick or implement an environment with a clear task and reward.
2. Claim or update the environment row in `env_registry.md`.
3. Verify locally and run base evals before hosted RL.
4. Launch the default hosted smoke when the Hub integration is ready.
5. Inspect RL metrics and rollout samples.
6. If the run is not obviously broken, run held-out evals on the trained
   checkpoint or adapter.
7. Collect Prime artifacts and write down what happened.
8. Preserve failures. Failed runs are data.

## Budget Posture

Default to cheap probes.

- First hosted run: after local checks pass and the Prime Hub integration action
  succeeds, run a Llama 1B, 1-step hosted RL smoke.
- The first smoke should use no sandbox or judge model unless the episode
  explicitly needs one.
- Stop after the first smoke, collect artifacts, inspect rollout samples, and
  decide whether the env is ready for a real run.
- If the 1-step smoke is clean, write a short rationale before trying 5-20
  steps.
- Only scale beyond that if the reward signal, artifact quality, and cost
  estimate make sense.
- Before nontrivial RL, run a base-model eval on a fixed train seed and a fixed
  held-out seed when cost allows.
- After non-broken RL, run matched evals on the trained checkpoint or deployed
  adapter. Use the same reward/objective; track auxiliary metrics separately.
- Be explicit before any larger model, Qwen run, multi-step run, sandbox-heavy
  run, judge-model run, or other non-default hosted spend.

Model guidance from Phase 0:

- Default first model: `meta-llama/Llama-3.2-1B-Instruct`.
- Llama 1B was cheap and stable on alphabet-sort: 50 steps cost about $0.084.
- On `meta-memory-state`, a 50-step Llama 1B run cost `$0.61` because the
  policy learned very long, often truncated outputs. Treat output length and
  truncation as both cost signals and reward-hacking signals.
- Try Qwen only when more capability is needed or the research question is about
  Qwen-family behavior.
- For Qwen, start with a 1-step smoke and `max_tokens = 16384`.
- Do not assume Qwen works just because a local eval works. Hosted rollout
  client path matters.
- Inspect Qwen runs for `content=None`, TITO/MITO fallback, high truncation,
  zero-advantage filtering, and long native thinking.
- Use a `meta-` prefix for new env names intended for Prime Hub.
- Tools are usually acceptable and relatively cheap. Sandboxes and judge models
  are allowed when necessary, but record them as explicit cost drivers.

## Required Outputs

Create or update an episode directory under `episodes/<episode_id>/` containing:

- `episode.yaml`: structured record based on
  `templates/episode_record.yaml`.
- `notebook.md`: narrative lab notebook based on
  `templates/lab_notebook.md`.
- `configs/`: exact train/eval configs used.
- `env/` or `env_ref.md`: local env code or the exact Hub env/version used.
- `artifacts.md`: links and IDs for Prime dashboards, evals, checkpoints, and
  any external artifacts.
- An updated row in `env_registry.md`.

Use `status: "draft"` when the episode is only locally verified. Mark the
registry row `local-ready` if the env scaffold and deterministic reward checks
pass but Prime Hub/install/eval integration is still unverified. Use
`status: "complete"` only when the intended integration path has been checked,
or the episode is explicitly scoped as local-only.

## Collection Checklist

For every hosted RL run, collect:

- Run ID and dashboard URL.
- Config path and full model/env/run settings.
- Status and timestamps from `prime train get <run_id> --plain`.
- Usage/cost from `prime train usage <run_id> --plain`.
- Progress from `prime train progress <run_id> --plain`.
- Metrics from `prime train metrics <run_id> --plain`.
- Checkpoints from `prime train checkpoints <run_id> --plain`.
- Rollout samples where available:
  `prime train rollouts <run_id> --step <step> --plain`.
- Logs when behavior is surprising:
  `prime train logs <run_id> --plain`.

For every base or held-out eval, collect:

- Eval command, model string, env/version, env args, seed, max tokens, and
  temperature.
- Whether the eval is base-train, base-heldout, trained-train, or
  trained-heldout.
- Reward mean/std, reward range, truncation, errors, and token usage.
- Auxiliary metrics that explain the reward: output length, parseability,
  candidate count, exact-format rate, task-specific accuracy, tool success, or
  other env-specific measurements.
- Local output path or Prime eval ID.

## Interpretation Checklist

Record the answer to these questions:

- Did the environment produce non-empty, non-identical rewards?
- Was reward variance useful for RL, or did zero-advantage filtering dominate?
- Did the model solve everything, solve nothing, or reveal a curriculum need?
- Did train-seed and held-out evals move together, diverge, or expose overfit?
- Were completions truncated?
- Did tool use help, hurt, or create format/coherence issues?
- Were there parser/reward exceptions?
- Were there signs of reward hacking?
- What would you change in the env or config next?

## Stop Conditions

Stop and write up instead of launching more runs when:

- A smoke run has parser/reward exceptions across most rollouts.
- The run is all zero-advantage for reasons you do not yet understand.
- Cost grows faster than expected.
- The model is too weak or too strong for the env.
- Prime client/path behavior is unclear and needs human or platform follow-up.

Your final message should be concise: episode ID, key result, run IDs, cost, and
the next recommended action.
