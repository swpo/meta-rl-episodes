# Episodes

Each research episode should create one directory here:

```text
episodes/<date>-<short-name>/
```

Recommended contents:

```text
episode.yaml
notebook.md
artifacts.md
configs/
env/ or env_ref.md
outputs/
```

`episode.yaml` is the structured record. `notebook.md` is the human-readable
lab notebook. `artifacts.md` can be a compact list of dashboards, eval IDs,
checkpoint IDs, rollout links, and any local output files.

Large raw artifacts do not need to be copied locally if Prime already stores
them. Store the IDs and enough summary to recover the evidence.
