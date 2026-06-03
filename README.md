# Meta RL Research Episodes

This repo is a clean-slate research scaffold for collecting many small RL
environment-building and training episodes on Prime Intellect / Verifiers.

The aim is not only to produce good environments. The larger goal is to build a
corpus of environment definitions, configs, run artifacts, metrics, failures,
and lab notes that can later support a meta-learning task: learning to reason
about RL experiment dynamics from the setup and traces.

## Current Guidance

Phase 0 calibrated cost and model/client behavior on
`primeintellect/alphabet-sort`.

Weak default recommendation:

- Start hosted RL probes with `meta-llama/Llama-3.2-1B-Instruct`.
- Use small runs first: 1-step smoke, then 5-20 steps, then only scale if the
  run produces useful reward variance and clean artifacts.
- For nontrivial episodes, keep a fixed eval matrix: base model on the training
  seed, base model on a held-out seed, then trained checkpoint/adapter on the
  same seeds when the RL run is not obviously broken.
- Use the same reward/objective for eval; track auxiliary metrics separately to
  explain reward movement and expose overfit, truncation, reward hacking, or
  tool/coherence failures.
- A 20-50 step Llama 1B follow-up can still be cheap enough to be worthwhile
  when the smoke is healthy; the first completed episode cost `$0.61` for 50
  steps, and revealed reward hacking via verbose answer stuffing.
- Watch output length and truncation as cost and quality signals, not just
  reward mean.
- Try larger Qwen models only when the environment appears to need more
  capability.
- For Qwen, use a one-step smoke with a high token ceiling, usually
  `max_tokens = 16384`, and inspect truncation, rollout client path, reward
  variance, and zero-advantage filtering before launching a real run.
- Beware Qwen token/client behavior. We observed `content=None` failures,
  TITO/MITO fallback, long native thinking, and model-dependent client paths.

See [reports/phase0_cost_calibration.md](reports/phase0_cost_calibration.md)
for the evidence behind this recommendation.

## Scaffold

- [agents/rl_episode_agent_brief.md](agents/rl_episode_agent_brief.md): prompt
  brief for Codex or another researcher running one episode.
- [agents/rl_episode_runbook.md](agents/rl_episode_runbook.md): operational
  workflow for designing an env, running smokes, launching hosted RL, and
  collecting artifacts.
- [agents/verifiers_env_patterns.md](agents/verifiers_env_patterns.md): portable
  Verifiers implementation patterns distilled for this repo.
- [env_registry.md](env_registry.md): coordination registry for claimed and
  completed environments.
- [agents/tracks/](agents/tracks): initial research directions and env ideas.
- [schemas/episode_record.schema.json](schemas/episode_record.schema.json):
  structured schema for episode records.
- [templates/episode_record.yaml](templates/episode_record.yaml): fill-in
  record for each episode.
- [templates/lab_notebook.md](templates/lab_notebook.md): human-readable notes
  template.
- [templates/artifacts.md](templates/artifacts.md): artifact/link tracking
  template.
- [templates/env_ref.md](templates/env_ref.md): environment reference template.
- [templates/prime_train_config.toml](templates/prime_train_config.toml):
  minimal hosted training config template.
- [episodes/README.md](episodes/README.md): where completed episode records
  should live.

## Episode Shape

Each research episode should leave enough context that another agent can answer:

- What was the environment and what behavior was it meant to elicit?
- What was the reward signal, and where might it be brittle or hackable?
- Which smoke tests passed or failed?
- Which hosted runs were launched, with exact configs and run IDs?
- What were the base and held-out eval results before and after RL?
- What did Prime report for status, usage, metrics, progress, checkpoints, and
  rollouts?
- What changed after observing the run?
- What would be the next useful experiment?

The raw run artifacts can stay on Prime when large. The local record should
store IDs, URLs, configs, summary metrics, and concise interpretation.

## Coordination

Before starting a new environment, claim a row in
[env_registry.md](env_registry.md). Use a `meta-` prefix for new env names so
Prime Hub entries are easy to identify as part of this project.

Track briefs in [agents/tracks/](agents/tracks) are meant to spread agents
across different RL dynamics when we are ready for more throughput. For now,
they are an idea backlog: tool coherence, multi-turn state, sparse vs shaped
reward, reward-hacking formats, data analysis, code debugging, model thresholds,
and science mini-reasoning.

Tools are acceptable and often cheap. Sandboxes and judge models are also
allowed when central to the track, but label them as explicit cost drivers in
the registry and episode record.
