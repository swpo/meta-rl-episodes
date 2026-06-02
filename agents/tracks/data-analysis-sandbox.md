# Track: Data Analysis Sandbox

## Objective

Build a `meta-` environment where the model must analyze a small generated table
or dataset, likely using a sandbox/tool to compute the answer.

## Environment Shape

Examples:

- Tiny CSV with aggregation, filtering, or regression-lite questions.
- Generated tables with hidden deterministic answers.
- Tool/sandbox path available; no-tool path possible but harder.

## Reward Ideas

- Exact numeric answer with tolerance.
- Correct intermediate fields.
- Format compliance.
- Optional penalty for not using required tool when the track is specifically
  about tool use.

## Cost Notes

This track may require sandbox execution. Sandboxes are useful but are a real
cost/runtime dependency. Keep datasets tiny, limit tool turns, and explicitly
record sandbox time/cost. Avoid LLM judges unless separately justified.

## Initial Smoke Plan

- Local/eval smoke first.
- Llama 1B hosted 1-step smoke with strict sandbox/tool limits.
- If Llama cannot use the sandbox reliably, try Qwen 9B with `max_tokens=16384`.

## Collision Avoidance

Differentiate from tool-coherence by requiring actual data computation rather
than simple lookup.
