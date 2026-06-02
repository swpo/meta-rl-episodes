# Track: Tool Coherence

## Objective

Build a `meta-` Verifiers environment where tool use can improve correctness but
also risks degrading answer coherence, formatting, or final synthesis.

## Motivation

Agents often know how to call tools, but RL may reward tool-mediated correctness
while accidentally encouraging verbose, fragmented, or incoherent answers. This
track should expose the tradeoff.

## Environment Shape

Examples:

- A lookup/calculation tool provides useful facts, but the final answer must be
  concise and formatted.
- Some tasks are easier without the tool, so unnecessary tool calls are a mild
  penalty.
- The tool can return distractors or extra fields that must be ignored.

## Reward Ideas

- Correct final answer.
- Format compliance.
- Penalty for irrelevant tool calls.
- Penalty for missing final answer after tool use.
- Optional coherence proxy: final answer length, required fields present, no
  raw tool dump.

## Cost Notes

Tool calls are usually cheap compared with judge models or sandboxes. Prefer
deterministic local tools and deterministic scoring. Avoid LLM-as-judge unless
the research question specifically needs it.

## Initial Smoke Plan

- Llama 1B, 1 step, `max_tokens=512` or enough for tool call plus final answer.
- If tool use fails because the model is too weak, smoke Qwen 9B with
  `max_tokens=16384`.

## Collision Avoidance

Differentiate from data-analysis tracks by keeping tools lightweight and
non-sandboxed.
