# Track: Code Debugging

## Objective

Build a `meta-` environment where the model fixes or reasons about tiny code
snippets and reward comes from deterministic tests.

## Environment Shape

Examples:

- One-file bug fix with 1-3 unit tests.
- Predict test outcome from code.
- Write a small function under constraints.

## Reward Ideas

- Unit test pass rate.
- Static format checks.
- Penalty for changing forbidden files or interfaces.

## Cost Notes

This likely needs sandbox execution. Keep tests tiny and timeouts strict.
Record sandbox use as a cost driver. Avoid broad package installs.

## Initial Smoke Plan

- Local dry run of tests.
- Hosted 1-step Llama 1B smoke.
- Try Qwen 9B only if Llama cannot produce syntactically valid code or if the
  env is intentionally beyond Llama's capability.

## Collision Avoidance

Keep tasks smaller than full coding-agent benchmarks; this track is about RL
dynamics from tests, not building a large code benchmark.
