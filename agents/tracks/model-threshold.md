# Track: Model Capability Threshold

## Objective

Build a `meta-` environment whose difficulty is calibrated so very small models
struggle, while mid-size or larger models can get a usable but non-saturated
reward distribution.

## Environment Shape

Examples:

- Compositional symbolic reasoning.
- Multi-constraint planning.
- Slightly long-horizon exact-answer tasks.
- Tasks with easy/medium/hard knobs.

## Reward Ideas

- Partial credit by constraint.
- Difficulty-stratified metrics.
- Held-out eval by difficulty level.

## Cost Notes

This can be deterministic and cheap, but may require Qwen 9B or 35B capability
probes. Use 1-step smokes before longer runs.

## Initial Smoke Plan

- Llama 1B, 1 step, to verify env mechanics.
- Qwen 9B, 1 step, `max_tokens=16384`, to check capability and cost.
- Adjust difficulty until reward is neither all-zero nor all-one.

## Collision Avoidance

Do not just make a larger version of another track. The key artifact here is the
model-size/difficulty threshold.
