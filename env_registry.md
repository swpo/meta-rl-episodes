# Meta Environment Registry

Use this registry to avoid accidental duplicate work across episodes.

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
3. Include owner/episode, intended env name, task family, and expected expensive
   dependencies.
4. Check for similar rows and intentionally differentiate the env.

After completing an episode:

1. Update status to `local-ready`, `hub-ready`, `completed`, `blocked`, or `abandoned`.
2. Add Prime env/version, run IDs, costs, and the key result.
3. Link the episode directory and report/notebook.

Use `local-ready` when an env scaffold and deterministic local checks pass but
Prime Hub/install/eval/training integration has not yet been verified.

Use `hub-ready` when the env has been pushed to Prime Hub and has a prepared
hosted run config, but the first hosted eval/RL run has not completed yet.

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

| Env Name | Status | Owner/Episode | Track | Task Family | Reward Type | Tools / Expensive Dependencies | Similar Envs To Avoid | Prime Env / Version | Episode | Run IDs | Cost | Key Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- |
| `meta-tool-coherence` | unclaimed | - | tool-coherence | tool use / answer synthesis | deterministic + format | tool-cheap | - | - | - | - | - | Tool calls should help on some cases and hurt coherence on others. |
| `meta-memory-state` | completed | episode `2026-06-02-meta-memory-state-001` | multi-turn-state | multi-turn ledger memory | deterministic / shaped + anti-stuffing | cheap | alphabet-sort | `abugoot/meta-memory-state@0.6.0`, hash `790e961c...` | [episodes/2026-06-02-meta-memory-state-001](episodes/2026-06-02-meta-memory-state-001) | `rdair5n0ca531bxqqvetrok8`, `mngozs87cvyj745q8zaqph9k`, `qh9lqxz5v3s82sjfs03cso8h`, `msisq47uw7tcnvuxn5aejrbg`, `wpw270lopu0vrzyfx9otn6w1`, `ovhe41qu43r1i3gwo98lw0mq`, `t06x036p2njx21ts5fi5p4vm`, `fdzqzv4ridlnhond78eghitd`, `jspr0dm70xv1nzv2jkz8u8ug`, `pnm7mpulnx3j8y1oyjz2sxwx`, `uvzzmvybz365g0qqgwbo2san`, `xvpykb8rxhq1kzg5wtnm9ty6`, `xn4ncn6hfi6pexy78mtt5cen`, `epzwm0i1cbluvcx27ya4caan`, `jvwvglhzbp2h8abmhtkgf6ri`, `ylzr995pao3587n4xgjnrj1r`, `zhc48qkatvucpcaqvsekd9sm`, `rzu3o8g5dro2qol7qbfbti1y`, `o4qsl2ttfmlnf07bba1uo4qg`, `t4kf6tmab09foppeih32pvx6`, `wc5nvpymcd093n8x9c7yedgt` | `$1.3435` | v0.4 Llama 1B improved reward but exploited best-candidate scoring via candidate stuffing/truncation. v0.5/v0.6 Qwen runs fixed formatting/stuffing and established cheap probes. Difficulty ladder: 3-account / 2-3-turn reward `0.573 -> 0.951`; 3-account / 3-4-turn retry `0.566 -> 0.879`; 4-account / 3-4-turn `0.564 -> 0.865`; 4-account / 4-5-turn batch-64 `0.566 -> 0.895`; 4-account / 5-6-turn batch-32 `0.568 -> 0.848`; 4-account / 6-7-turn batch-32 Qwen 0.8B `0.569 -> 0.713` with mid-run length/repetition spike; matched Qwen 2B `0.713 -> 0.957` without that pathology. Run-scoped held-out evals on 4-account / 6-7 turns show base/trained reward `0.651 -> 0.862` for Qwen 0.8B and `0.728 -> 0.955` for Qwen 2B; trained 2B exact-turn rate `0.42`, solve-all examples `0.0`. |
| `meta-sparse-shaping` | unclaimed | - | sparse-vs-shaped | curriculum / reward design | sparse and shaped variants | cheap | - | - | - | - | - | Paired env/config to compare sparse vs shaped reward dynamics. |
| `meta-reward-hack-format` | unclaimed | - | reward-hacking-format | adversarial formatting | deterministic with hack traps | cheap | backdoor/ifeval-style tasks | - | - | - | - | Tests parser/reward loopholes without an LLM judge. |
| `meta-data-analysis-lite` | completed-tool-extension | episode `2026-06-03-meta-data-analysis-lite-001` | data-analysis-sandbox | tabular data analysis | deterministic computed answers | cheap + tool-cheap; no sandbox/judge | `meta-memory-state` | `abugoot/meta-data-analysis-lite@0.2.1`, hash `fd2e9aec...` | [episodes/2026-06-03-meta-data-analysis-lite-001](episodes/2026-06-03-meta-data-analysis-lite-001) | `ilb7rwevow9e1nzorv00rhxz`, `lv05ttq2v7kd7l628qdstxjz`, `gvq9mq8ppx0a4g3rwsx77215`, `cw41toqvv97d0ba5q8e199wx`, `x36l212xgveqr6qgnsske6jk`, `ic5nrtiex0w2zuuf421ox451` | `$0.2578` | v0.1.1 no-tool Llama 1B learned format and partial arithmetic: base train/held-out reward `0.0225 / 0.0113` -> trained `0.654 / 0.465`, but exact answers stayed low. v0.2.1 adds deterministic `analyze_table`; base Qwen 2B with tools looped calls (`2.375` calls avg, reward `0.3125`) while no-tool Qwen was parseable but arithmetically weak (`exact_answer 0.0625`). A capped 10-step Qwen 2B tool run (`ic5n...`, `$0.06`) learned one-call tool use; trained train/held-out reward `0.978 / 1.000`, exact answer `1.0 / 1.0`. A 20-step tool run failed after zero-advantage filtering removed all rollouts, so the recommended default is `configs/qwen2b_10step_v021_tools_b32r2.toml`. |
| `meta-code-debug-mini` | unclaimed | - | code-debugging | coding/debugging | unit tests / deterministic | sandbox | - | - | - | - | - | Small code repair tasks with cheap tests; sandbox cost must be tracked. |
| `meta-model-threshold` | unclaimed | - | model-threshold | capability threshold | deterministic | cheap | - | - | - | - | - | Designed so Llama 1B struggles and Qwen 9B/35B may be needed. |
| `meta-science-mini` | unclaimed | - | science-reasoning | scientific reasoning | deterministic / rubric-lite | cheap or judge optional | bioreasoning_phenotype | - | - | - | - | Tiny science task without external judge by default. |
