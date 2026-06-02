# Subagent Spawn Prompt

Use this as the initial message for a Codex thread assigned one RL research
episode.

```text
You are running one small RL research episode for the meta-learning corpus in
this repo. First read:

- README.md
- env_registry.md
- agents/rl_episode_agent_brief.md
- agents/rl_episode_runbook.md
- agents/track_assignment_template.md
- reports/phase0_cost_calibration.md

Then choose or implement one Verifiers environment track, claim/update a row in
env_registry.md, create an episode directory under episodes/<episode_id>/, and
keep episode.yaml plus notebook.md updated as you work.

Default budget posture:

- Start with Llama 1B unless the research question needs more capability.
- First hosted run should be a 1-step smoke.
- For Qwen, use a 1-step smoke with max_tokens=16384 and inspect rollout client
  path, truncation, zero-advantage filtering, reward variance, and cost before
  launching any longer run.
- Preserve failed and stalled runs as useful data.
- Use a `meta-` prefix for new env names intended for Prime Hub.
- Tools are generally fine; sandboxes and judge models are allowed only when
  central to the track and must be recorded as cost drivers.

Required final output:

- Episode directory path.
- Env and model(s) tested.
- Prime run/eval IDs and dashboard links.
- Total observed cost.
- Key lesson about the env/RL dynamics.
- Recommended next experiment.
- Updated env_registry.md row.
```
