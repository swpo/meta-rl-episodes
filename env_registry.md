# Meta Environment Registry

Use this registry to avoid accidental duplicate work across subagents.

Every environment intended for Prime Hub should use a `meta-` prefix in its env
ID/name, for example:

```text
meta-tool-coherence
meta-sparse-shaping
meta-data-analysis-lite
```

If the Hub namespace also includes the owner/team, use:

```text
<team>/meta-<short-name>
```

## Claim Protocol

Before starting an episode:

1. Pick a track from `agents/tracks/` or propose a new one.
2. Add a row with status `claimed`.
3. Include owner/thread, intended env name, task family, and expected expensive
   dependencies.
4. Check for similar rows and intentionally differentiate the env.

After completing an episode:

1. Update status to `completed`, `blocked`, or `abandoned`.
2. Add Prime env/version, run IDs, costs, and the key result.
3. Link the episode directory and report/notebook.

## Cost Labels

Use these labels in the registry:

- `cheap`: deterministic reward, no sandbox, no judge model.
- `tool-cheap`: tool calls are expected but do not require paid model judges or
  expensive sandbox infrastructure.
- `sandbox`: requires code execution, data analysis, browser, or other sandboxed
  runtime. Useful but must be cost-monitored.
- `judge`: uses an LLM-as-judge, monitor, or evaluator model. Useful but
  usually less suitable for first cost calibration.
- `mixed`: multiple cost drivers.

## Registry

| Env Name | Status | Owner/Thread | Track | Task Family | Reward Type | Tools / Expensive Dependencies | Similar Envs To Avoid | Prime Env / Version | Episode | Run IDs | Cost | Key Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- |
| `meta-tool-coherence` | unclaimed | - | tool-coherence | tool use / answer synthesis | deterministic + format | tool-cheap | - | - | - | - | - | Tool calls should help on some cases and hurt coherence on others. |
| `meta-memory-state` | unclaimed | - | multi-turn-state | multi-turn memory | deterministic / shaped | cheap | alphabet-sort | - | - | - | - | Tests state tracking across turns without needing a sandbox. |
| `meta-sparse-shaping` | unclaimed | - | sparse-vs-shaped | curriculum / reward design | sparse and shaped variants | cheap | - | - | - | - | - | Paired env/config to compare sparse vs shaped reward dynamics. |
| `meta-reward-hack-format` | unclaimed | - | reward-hacking-format | adversarial formatting | deterministic with hack traps | cheap | backdoor/ifeval-style tasks | - | - | - | - | Tests parser/reward loopholes without an LLM judge. |
| `meta-data-analysis-lite` | unclaimed | - | data-analysis-sandbox | tabular data analysis | deterministic computed answers | sandbox | - | - | - | - | - | Sandbox needed; keep dataset small and record runtime/cost. |
| `meta-code-debug-mini` | unclaimed | - | code-debugging | coding/debugging | unit tests / deterministic | sandbox | - | - | - | - | - | Small code repair tasks with cheap tests; sandbox cost must be tracked. |
| `meta-model-threshold` | unclaimed | - | model-threshold | capability threshold | deterministic | cheap | - | - | - | - | - | Designed so Llama 1B struggles and Qwen 9B/35B may be needed. |
| `meta-science-mini` | unclaimed | - | science-reasoning | scientific reasoning | deterministic / rubric-lite | cheap or judge optional | bioreasoning_phenotype | - | - | - | - | Tiny science task without external judge by default. |
