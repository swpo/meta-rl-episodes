# Track: Sparse Vs Shaped Reward

## Objective

Build paired `meta-` env variants that expose the difference between sparse
terminal reward and shaped intermediate/partial reward.

## Environment Shape

Examples:

- A puzzle or transformation task with exact final answer.
- Variant A gives only final correctness.
- Variant B gives partial credit for valid intermediate structure.

## Reward Ideas

- Sparse binary reward.
- Shaped partial reward for subgoals.
- Format compliance held constant across variants.

## Cost Notes

Keep deterministic. This is a cheap track unless the task requires a sandbox.

## Initial Smoke Plan

- Llama 1B, 1-step smoke for both sparse and shaped variants.
- If sparse reward has all-zero signal, run 5-20 steps only on shaped variant or
  add a curriculum.

## Collision Avoidance

Record both variants under one episode so other agents do not duplicate the same
comparison.
