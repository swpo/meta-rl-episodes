# Episode Notebook: <episode_id>

## Question

What are we trying to learn?

## Environment

- Env:
- Version/source:
- Local path or Hub URL:
- Key args:
- Reward signal:
- Parser assumptions:
- Tooling:

## Hypotheses

1. 
2. 
3. 

## Smoke Tests

### Eval Smoke

Command:

```bash

```

Result:

- Reward:
- Truncation:
- Errors:
- Notes:

## Eval Matrix

Use the same reward/objective for base and trained evals. Record auxiliary
metrics separately when they explain what the reward is doing.

| Eval | Model | Seed/Split | Examples | Reward | Truncation | Aux Metrics | Notes |
| --- | --- | --- | ---: | --- | ---: | --- | --- |

### Hosted RL Smoke

Run ID:

Dashboard:

Config:

Result:

- Status:
- Cost:
- Reward:
- Zero-advantage filtering:
- Truncation:
- Notes:

## Runs

| Run | Model | Steps | Max Tokens | Status | Cost | Reward Read | Notes |
| --- | --- | ---: | ---: | --- | ---: | --- | --- |

## Observations

What happened that was expected?

What happened that was surprising?

What did the model actually do in rollouts?

## Failure Modes

- Parser/reward errors:
- Truncation:
- Empty or malformed outputs:
- Zero-advantage filtering:
- Tool-use issues:
- Cost/runtime surprises:
- Platform/client issues:

## Interpretation

What do we think this episode teaches about RL dynamics, environment design, or
model behavior?

## Next Steps

1. 
2. 
3. 
