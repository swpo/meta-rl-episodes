# Track: Science Mini-Reasoning

## Objective

Build a small `meta-` science reasoning environment with deterministic or
rubric-lite rewards, inspired by bioreasoning but much cheaper.

## Environment Shape

Examples:

- Match a mechanism to a phenotype from a tiny curated fact table.
- Predict qualitative direction from a provided pathway snippet.
- Extract and combine two facts from a compact context.

## Reward Ideas

- Exact label match.
- Partial credit for valid evidence fields.
- Format compliance.
- Optional held-out perturbation/context split.

## Cost Notes

Avoid LLM judges for the first version. If a judge is necessary, label the env
`judge` in `env_registry.md` and run separate cost calibration. Deterministic
fact tables are preferred.

## Initial Smoke Plan

- Llama 1B for mechanics.
- Qwen 9B or 35B only if the science reasoning is beyond Llama 1B.
- Use `max_tokens=16384` for Qwen smokes.

## Collision Avoidance

Do not duplicate `bioreasoning_phenotype`; use a tiny, controlled science task
with explicit deterministic labels.
