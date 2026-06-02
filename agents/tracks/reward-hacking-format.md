# Track: Reward Hacking Format

## Objective

Build a `meta-` environment that intentionally contains plausible parser or
formatting traps, then document whether models exploit or stumble into them.

## Environment Shape

Examples:

- XML/JSON answer tags with distractor text.
- Multiple candidate answers where only one section should be scored.
- Prompts that mention the reward format or include adversarial examples.

## Reward Ideas

- Exact answer in the required field.
- Penalty for extra answer-like fields.
- Parser robustness tests.
- Held-out eval with slightly different formatting.

## Cost Notes

Prefer deterministic parser-based scoring. Avoid LLM judges for the first
version; the point is to study cheap reward hacking and parser brittleness.

## Initial Smoke Plan

- Llama 1B, 1 step, `max_tokens=512`.
- Inspect rollouts manually. Reward hacking may not show in metrics alone.

## Collision Avoidance

Do not recreate `prime/backdoor-ifeval-all`; focus on a small deterministic env
that records parser assumptions clearly.
