# Track Assignment Template

Use this when assigning a subagent to a specific research track.

```text
Track: <track name>
Episode ID: <date-short-name>
Proposed env name: meta-<short-name>

Read:
- README.md
- env_registry.md
- agents/rl_episode_agent_brief.md
- agents/rl_episode_runbook.md
- agents/tracks/<track>.md
- reports/phase0_cost_calibration.md

Goal:
<one paragraph describing the environment/research question>

Avoid duplicating:
- <similar envs or rows in env_registry.md>

Cost posture:
- Start with Llama 1B.
- First hosted run is a 1-step smoke.
- If using Qwen, use a 1-step 16K smoke and inspect client path, truncation,
  zero-advantage filtering, reward variance, and cost.
- Tools are allowed when they are central to the research question.
- Sandboxes and judge models are allowed only when justified; record them as
  explicit cost drivers.

Required artifacts:
- episodes/<episode_id>/episode.yaml
- episodes/<episode_id>/notebook.md
- episodes/<episode_id>/artifacts.md
- configs and env reference/code
- Updated row in env_registry.md
```
