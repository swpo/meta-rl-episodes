# Artifacts: 2026-06-02-meta-memory-state-001

## Prime Hosted Runs

| Run ID | Dashboard | Config | Status | Notes |
| --- | --- | --- | --- | --- |
| `rdair5n0ca531bxqqvetrok8` | https://app.primeintellect.ai/dashboard/training/rdair5n0ca531bxqqvetrok8 | `configs/llama1b_1step_smoke.toml` | completed | 1-step Llama 1B smoke; reward all zero; cost `$0.03`. |
| `mngozs87cvyj745q8zaqph9k` | https://app.primeintellect.ai/dashboard/training/mngozs87cvyj745q8zaqph9k | `configs/llama1b_1step_smoke_v02.toml` | completed | v0.2 prompt/parser smoke; reward all zero; cost `$0.0080`. |
| `qh9lqxz5v3s82sjfs03cso8h` | https://app.primeintellect.ai/dashboard/training/qh9lqxz5v3s82sjfs03cso8h | `configs/llama1b_1step_smoke_v03.toml` | completed | v0.3 answer-signature smoke; reward all zero; cost `$0.0085`. |
| `msisq47uw7tcnvuxn5aejrbg` | https://app.primeintellect.ai/dashboard/training/msisq47uw7tcnvuxn5aejrbg | `configs/llama1b_1step_smoke_v04.toml` | completed | v0.4 message-object-compatible smoke; mean reward `0.343`; cost `$0.0085`. |
| `wpw270lopu0vrzyfx9otn6w1` | https://app.primeintellect.ai/dashboard/training/wpw270lopu0vrzyfx9otn6w1 | `configs/llama1b_50step_v04.toml` | completed | v0.4 50-step follow-up; final mean reward `0.779`; truncation `0.969`; cost `$0.61`. |
| `ovhe41qu43r1i3gwo98lw0mq` | https://app.primeintellect.ai/dashboard/training/ovhe41qu43r1i3gwo98lw0mq | `configs/llama1b_50step_v05.toml` | failed before training | v0.5 Llama attempt failed renderer auto-validation; no steps, samples, or charged usage. |
| `t06x036p2njx21ts5fi5p4vm` | https://app.primeintellect.ai/dashboard/training/t06x036p2njx21ts5fi5p4vm | `configs/qwen08b_50step_v05.toml` | completed | v0.5 Qwen 0.8B 50-step probe; final mean reward `0.936`, best step `0.993`, truncation `0.0`, cost `$0.07`. |
| `fdzqzv4ridlnhond78eghitd` | https://app.primeintellect.ai/dashboard/training/fdzqzv4ridlnhond78eghitd | `configs/qwen08b_30step_v06.toml` | completed | v0.6 Qwen 0.8B 30-step schema-penalty probe; final mean reward `0.916`, best step `0.989`, truncation `0.0`, cost `$0.04`. |
| `jspr0dm70xv1nzv2jkz8u8ug` | https://app.primeintellect.ai/dashboard/training/jspr0dm70xv1nzv2jkz8u8ug | `configs/qwen08b_30step_v06_resume_from25_retry.toml` | completed | v0.6 Qwen resume retry from step-25 checkpoint; final logged reward `0.959`, truncation `0.0`, cost `$0.0067`; fresh final adapter later deployed successfully on retry. |
| `pnm7mpulnx3j8y1oyjz2sxwx` | https://app.primeintellect.ai/dashboard/training/pnm7mpulnx3j8y1oyjz2sxwx | `configs/qwen08b_30step_v06_resume_retry2_from25.toml` | stopped | Second v0.6 Qwen resume retry from the first retry's step-25 checkpoint; fresh launch and native restart both stalled waiting for trainer checkpoint 26; cost `$0.0027`. |
| `uvzzmvybz365g0qqgwbo2san` | https://app.primeintellect.ai/dashboard/training/uvzzmvybz365g0qqgwbo2san | `configs/qwen08b_30step_v06_diff_3acct_2to3.toml` | completed | Difficulty ablation: same Qwen 0.8B 30-step setup, harder 3-account / 2-3 turn env args; final reward `0.951`, step-20 reward `0.875`, truncation `0.0`, cost `$0.06`. |
| `xvpykb8rxhq1kzg5wtnm9ty6` | https://app.primeintellect.ai/dashboard/training/xvpykb8rxhq1kzg5wtnm9ty6 | `configs/qwen08b_30step_v06_diff_3acct_3to4.toml` | stopped | First 3-account / 3-4 turn attempt; step 0 reward `0.560`, step 1 reward `0.532`, then stopped after waiting at trainer checkpoint broadcast 1; cost `$0.0052`. |
| `xn4ncn6hfi6pexy78mtt5cen` | https://app.primeintellect.ai/dashboard/training/xn4ncn6hfi6pexy78mtt5cen | `configs/qwen08b_30step_v06_diff_3acct_3to4.toml` | completed | Retry of 3-account / 3-4 turn ablation; final reward `0.879`, step-20 reward `0.857`, final solve-all `0.0`, cost `$0.08`. |
| `epzwm0i1cbluvcx27ya4caan` | https://app.primeintellect.ai/dashboard/training/epzwm0i1cbluvcx27ya4caan | `configs/qwen08b_30step_v06_diff_4acct_3to4.toml` | completed | 4-account / 3-4 turn ablation; final reward `0.865`, step-20 reward `0.889`, final solve-all `0.0`, cost `$0.09`. |
| `jvwvglhzbp2h8abmhtkgf6ri` | https://app.primeintellect.ai/dashboard/training/jvwvglhzbp2h8abmhtkgf6ri | `configs/qwen08b_30step_v06_diff_4acct_4to5.toml` | stopped | First 4-account / 4-5 turn batch-128 attempt; stopped after checkpoint-broadcast-1 stall; step rewards `0.570`, `0.608`; cost `$0.0070`. |
| `ylzr995pao3587n4xgjnrj1r` | https://app.primeintellect.ai/dashboard/training/ylzr995pao3587n4xgjnrj1r | `configs/qwen08b_30step_v06_diff_4acct_4to5.toml` | stopped | Retry of 4-account / 4-5 turn batch-128 attempt; repeated checkpoint-broadcast-1 stall; step rewards `0.599`, `0.587`; cost `$0.0069`. |
| `zhc48qkatvucpcaqvsekd9sm` | https://app.primeintellect.ai/dashboard/training/zhc48qkatvucpcaqvsekd9sm | `configs/qwen08b_30step_v06_diff_4acct_4to5_b64.toml` | completed | Batch-64 4-account / 4-5 turn run; final reward `0.895`, step-20 reward `0.855`, final solve-all `0.0`, cost `$0.05`. |
| `rzu3o8g5dro2qol7qbfbti1y` | https://app.primeintellect.ai/dashboard/training/rzu3o8g5dro2qol7qbfbti1y | `configs/qwen08b_30step_v06_diff_4acct_5to6_b64.toml` | stopped | Batch-64 4-account / 5-6 turn attempt; no completed steps or usage; superseded by successful batch-32 retry. |
| `o4qsl2ttfmlnf07bba1uo4qg` | https://app.primeintellect.ai/dashboard/training/o4qsl2ttfmlnf07bba1uo4qg | `configs/qwen08b_30step_v06_diff_4acct_5to6_b32.toml` | completed | Batch-32 4-account / 5-6 turn run; final reward `0.848`, step-20 reward `0.777`, final solve-all `0.0`, cost `$0.03`. |
| `t4kf6tmab09foppeih32pvx6` | https://app.primeintellect.ai/dashboard/training/t4kf6tmab09foppeih32pvx6 | `configs/qwen08b_30step_v06_diff_4acct_6to7_b32.toml` | completed | Batch-32 4-account / 6-7 turn Qwen 0.8B run; final reward `0.713`, step-20 reward `0.801`, mid-run length/repetition spike, final solve-all `0.0`, cost `$0.16`. |
| `wc5nvpymcd093n8x9c7yedgt` | https://app.primeintellect.ai/dashboard/training/wc5nvpymcd093n8x9c7yedgt | `configs/qwen2b_30step_v06_diff_4acct_6to7_b32.toml` | completed | Matched Qwen 2B scaling run for 4-account / 6-7 turns; final reward `0.957`, step-20 reward `0.912`, no length/repetition spike, final solve-all `0.0`, cost `$0.08`. |

## Prime Evals

| Eval ID | Dashboard | Command/Config | Status | Notes |
| --- | --- | --- | --- | --- |
| - | - | - | not run | Local Verifiers package unavailable in the checked runtime. |

## Local Evals

| Eval | Output Path | Model | Env Args | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| base-train | `evals/base_train_seed_v04/evals/meta-memory-state--meta-llama--Llama-3.2-1B-Instruct/6fe2570b/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct` | seed `1337420`, 32 examples | completed | Reward `0.084`; truncation `0.0`; parseable turns `0.184`; multi-candidate turns `0.0`. CLI upload step failed after local save, so no Prime eval ID. |
| base-heldout | `evals/base_heldout_seed_v04/evals/meta-memory-state--meta-llama--Llama-3.2-1B-Instruct/0b1bf684/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct` | seed `424242`, 32 examples | completed | Reward `0.025`; truncation `0.0`; parseable turns `0.064`; multi-candidate turns `0.0`. |
| trained-train | `evals/trained_train_seed_v04/evals/meta-memory-state--meta-llama--Llama-3.2-1B-Instruct:lz4roaz2jmokl189l0bj7mqq/a16445a5/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct:lz4roaz2jmokl189l0bj7mqq` | seed `1337420`, 32 examples | completed | Reward `0.790`; truncation `1.0`; multi-candidate turns `1.0`; mean candidates/turn `13.14`. |
| trained-heldout | `evals/trained_heldout_seed_v04/evals/meta-memory-state--meta-llama--Llama-3.2-1B-Instruct:lz4roaz2jmokl189l0bj7mqq/d1f473fa/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct:lz4roaz2jmokl189l0bj7mqq` | seed `424242`, 32 examples | completed | Reward `0.782`; truncation `1.0`; multi-candidate turns `1.0`; mean candidates/turn `13.23`. |
| base-train-v05 | `evals/base_train_seed_v05/evals/meta-memory-state--meta-llama--Llama-3.2-1B-Instruct/d0522798/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct` | seed `1337420`, 32 examples | completed | Reward `0.0148`; truncation `0.0`; parseable turns `0.041`; exact-one-ledger turns `0.041`; multi-candidate turns `0.0`. |
| base-heldout-v05 | `evals/base_heldout_seed_v05/evals/meta-memory-state--meta-llama--Llama-3.2-1B-Instruct/fa2fdf29/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct` | seed `424242`, 32 examples | completed | Reward `0.0173`; truncation `0.0`; parseable turns `0.043`; exact-one-ledger turns `0.043`; multi-candidate turns `0.0`. |
| base-train-v05-qwen08b | - | `Qwen/Qwen3.5-0.8B` | seed `1337420`, 32 examples | blocked | `prime eval run` attempts with 16K and 512 token caps hung before creating output directories; killed locally. |
| base-train-v05-qwen08b-tiny | - | `Qwen/Qwen3.5-0.8B` | seed `1337420`, 3 examples | blocked | Tiny 3-example, 256-token diagnostic also hung; no saved local results. |
| base-heldout-v06-llama1b | `evals/base_heldout_seed_v06_llama1b/evals/meta-memory-state--meta-llama--Llama-3.2-1B-Instruct/d011e013/results.jsonl` | `meta-llama/Llama-3.2-1B-Instruct` | seed `424242`, 32 examples | completed | Reward `0.0190`; truncation `0.0`; parseable turns `0.043`; exact-one-ledger turns `0.043`; multi-candidate turns `0.0`; code-fence turns `0.0`. |
| base-heldout-v06-qwen08b-tiny | - | `Qwen/Qwen3.5-0.8B` | seed `424242`, 3 examples | blocked | Tiny 3-example, 16K-token v0.6 eval hung for about 60s before creating an output directory; killed locally. |
| trained-heldout-v06-qwen08b-resume-tiny | `evals/trained_heldout_seed_v06_qwen08b_resume_tiny/evals/meta-memory-state--Qwen--Qwen3.5-0.8B:lsbgjt98s0d1nyv5eofomojx/8d89104b/results.jsonl` | `Qwen/Qwen3.5-0.8B:lsbgjt98s0d1nyv5eofomojx` | seed `424242`, 3 examples | completed | Reward `0.9740`; truncation `0.0`; parseable turns `1.0`; exact-one-ledger turns `1.0`; multi-candidate turns `0.0`; code-fence turns `0.0`. |
| base-heldout-v06-6to7-qwen08b-n8 | `evals/run_t4kf6tmab09foppeih32pvx6/base_heldout_seed424242_4acct_6to7_n8/evals/meta-memory-state--Qwen--Qwen3.5-0.8B/ff9dd043/results.jsonl` | `Qwen/Qwen3.5-0.8B` | seed `424242`, 4 accounts, 6-7 turns, linked RL run `t4kf6tmab09foppeih32pvx6` | completed | Reward `0.651`; exact-one-ledger turns `0.36`; exact-turn `0.00`; account-exact `0.465`; summary in scoped eval folder. |
| trained-heldout-v06-6to7-qwen08b-n8 | `evals/run_t4kf6tmab09foppeih32pvx6/trained_heldout_seed424242_4acct_6to7_n8/evals/meta-memory-state--Qwen--Qwen3.5-0.8B:dsg66w80rcjhu3kkv0zpdzve/e000b512/results.jsonl` | `Qwen/Qwen3.5-0.8B:dsg66w80rcjhu3kkv0zpdzve` | seed `424242`, 4 accounts, 6-7 turns, linked RL run `t4kf6tmab09foppeih32pvx6` | completed | Reward `0.862`; exact-one-ledger turns `1.0`; exact-turn `0.06`; account-exact `0.765`; solve-all examples `0.0`. |
| base-heldout-v06-6to7-qwen2b-n8 | `evals/run_wc5nvpymcd093n8x9c7yedgt/base_heldout_seed424242_4acct_6to7_n8/evals/meta-memory-state--Qwen--Qwen3.5-2B/41a7d6b3/results.jsonl` | `Qwen/Qwen3.5-2B` | seed `424242`, 4 accounts, 6-7 turns, linked RL run `wc5nvpymcd093n8x9c7yedgt` | completed | Reward `0.728`; exact-one-ledger turns `0.86`; exact-turn `0.10`; account-exact `0.575`; summary in scoped eval folder. |
| trained-heldout-v06-6to7-qwen2b-n8 | `evals/run_wc5nvpymcd093n8x9c7yedgt/trained_heldout_seed424242_4acct_6to7_n8/evals/meta-memory-state--Qwen--Qwen3.5-2B:ym5npd2cye3h2zfey3746say/70050276/results.jsonl` | `Qwen/Qwen3.5-2B:ym5npd2cye3h2zfey3746say` | seed `424242`, 4 accounts, 6-7 turns, linked RL run `wc5nvpymcd093n8x9c7yedgt` | completed | Reward `0.955`; exact-one-ledger turns `1.0`; exact-turn `0.42`; account-exact `0.910`; solve-all examples `0.0`. |

## Checkpoints

| Run ID | Step | Checkpoint ID | Status | Notes |
| --- | ---: | --- | --- | --- |
| `rdair5n0ca531bxqqvetrok8` | final | - | not listed | Logs said final checkpoint was written, but `prime train checkpoints` returned none. |
| `mngozs87cvyj745q8zaqph9k` | final | - | not listed | Logs said final checkpoint was written, but `prime train checkpoints` returned none. |
| `qh9lqxz5v3s82sjfs03cso8h` | final | - | not listed | Logs said final checkpoint was written, but `prime train checkpoints` returned none. |
| `msisq47uw7tcnvuxn5aejrbg` | final | - | not listed | Logs said final checkpoint was written, but `prime train checkpoints` returned none. |
| `wpw270lopu0vrzyfx9otn6w1` | 10 | `t6r9odwqtqmmb6ttd0qbaqzh` | ready | Listed by `prime train checkpoints`; size `172.3 MB`. |
| `wpw270lopu0vrzyfx9otn6w1` | 20 | `k0lrv5pt9qlqmozjuonaolud` | ready | Listed by `prime train checkpoints`; size `172.3 MB`. |
| `wpw270lopu0vrzyfx9otn6w1` | 30 | `j6xr82lpq15wvr5mfkjof8p9` | ready | Listed by `prime train checkpoints`; size `172.3 MB`. |
| `wpw270lopu0vrzyfx9otn6w1` | 40 | `h2s6hy7gg9o4v3my0q20tden` | ready | Listed by `prime train checkpoints`; size `172.3 MB`. |
| `wpw270lopu0vrzyfx9otn6w1` | 50 | - | not listed | Logs said final checkpoint was written, but only steps 10/20/30/40 were listed. |
| `t06x036p2njx21ts5fi5p4vm` | 25 | `xeepq0hs9j2n10vax391h27x` | ready | Listed by `prime train checkpoints`; size `97.8 MB`. |
| `t06x036p2njx21ts5fi5p4vm` | 30 | `zwien63xjtwzkzy48b243995` | ready | Listed by `prime train checkpoints`; size `97.8 MB`. |
| `t06x036p2njx21ts5fi5p4vm` | 35 | `qexxugmcjk7gi9ome0h1c2le` | ready | Listed by `prime train checkpoints`; size `97.8 MB`. |
| `t06x036p2njx21ts5fi5p4vm` | 40 | `ot6uwlx195sspoka9rzspxu2` | ready | Listed by `prime train checkpoints`; size `97.8 MB`. |
| `t06x036p2njx21ts5fi5p4vm` | 45 | `nyxpe3xu3i4zzt2cp90ludvl` | ready | Listed by `prime train checkpoints`; size `97.8 MB`; logs said final checkpoint was written but only steps 25-45 were listed. |
| `fdzqzv4ridlnhond78eghitd` | 5 | `dgtbytfkys3ewmww5ldx447w` | ready | Listed by `prime train checkpoints`; size `97.8 MB`. |
| `fdzqzv4ridlnhond78eghitd` | 10 | `vooc7y4i367egdavwj3dhlwl` | ready | Listed by `prime train checkpoints`; size `97.8 MB`. |
| `fdzqzv4ridlnhond78eghitd` | 15 | `tjcx5scgt7sl8jvl80mk4bp2` | ready | Listed by `prime train checkpoints`; size `97.8 MB`. |
| `fdzqzv4ridlnhond78eghitd` | 20 | `oay64borfhmd6a9p5vttlt1e` | ready | Listed by `prime train checkpoints`; size `97.8 MB`. |
| `fdzqzv4ridlnhond78eghitd` | 25 | `vs01hyx5vxxbn431rb3qj22v` | ready | Listed by `prime train checkpoints`; size `97.8 MB`. |
| `fdzqzv4ridlnhond78eghitd` | 30 | `oc078rsfvphlq2r08njn9o9e` | uploading | Listed as `UPLOADING` when checked shortly after completion; logs said final checkpoint writing completed. |
| `jspr0dm70xv1nzv2jkz8u8ug` | 25 | `ykoqriy9kluvxwo2zksxwiyi` | ready | Resume retry checkpoint; size `97.8 MB`. |
| `jspr0dm70xv1nzv2jkz8u8ug` | 30 | `x47ww0spp9qdbxgjzl8a8a0j` | uploading | Listed as `UPLOADING` when checked shortly after completion; final step-null adapter record was READY. |
| `pnm7mpulnx3j8y1oyjz2sxwx` | 25 | `m1gaxcecx4y5pjt9x685kxhv` | ready | Second resume retry checkpoint; size `97.8 MB`. |
| `uvzzmvybz365g0qqgwbo2san` | 5 | `mafbcb6at9x5hamfk6pj7dx7` | ready | Difficulty ablation checkpoint; size `97.8 MB`. |
| `uvzzmvybz365g0qqgwbo2san` | 10 | `u4b5u03efpun0gmxcyz3mx97` | ready | Difficulty ablation checkpoint; size `97.8 MB`. |
| `uvzzmvybz365g0qqgwbo2san` | 15 | `k36fgxl8veok08e22d9hz4bs` | ready | Difficulty ablation checkpoint; size `97.8 MB`. |
| `uvzzmvybz365g0qqgwbo2san` | 20 | `oklaohgp4v0y5u4yzk7vhcr7` | ready | Difficulty ablation checkpoint; size `97.8 MB`. |
| `uvzzmvybz365g0qqgwbo2san` | 25 | `cdkv8zpjojecika5aobdf0tl` | ready | Difficulty ablation checkpoint; size `97.8 MB`. |
| `xvpykb8rxhq1kzg5wtnm9ty6` | final | - | not listed | Stopped at latest step 1; no checkpoints listed. |
| `xn4ncn6hfi6pexy78mtt5cen` | 5 | `rsqu3xv8niucvpaam0fyysuj` | ready | 3-4 turn retry checkpoint; size `97.8 MB`. |
| `xn4ncn6hfi6pexy78mtt5cen` | 10 | `a386ggoxjgrtrtgp3v4mns5j` | ready | 3-4 turn retry checkpoint; size `97.8 MB`. |
| `xn4ncn6hfi6pexy78mtt5cen` | 15 | `b0upu6ai5v40mqhoiy7h025g` | ready | 3-4 turn retry checkpoint; size `97.8 MB`. |
| `xn4ncn6hfi6pexy78mtt5cen` | 20 | `z0hum4gt6nvugzwrpa517j3l` | ready | 3-4 turn retry checkpoint; size `97.8 MB`. |
| `xn4ncn6hfi6pexy78mtt5cen` | 25 | `mx6bjnru2d3phcohfwc1h8q3` | ready | 3-4 turn retry checkpoint; size `97.8 MB`. |
| `epzwm0i1cbluvcx27ya4caan` | 5 | `f8rhxq0zgl45w1zl56c6lt0p` | ready | 4-account / 3-4 turn checkpoint. |
| `epzwm0i1cbluvcx27ya4caan` | 10 | `hn8ugbbo7p2nbs8bk33tvfvq` | ready | 4-account / 3-4 turn checkpoint. |
| `epzwm0i1cbluvcx27ya4caan` | 15 | `x82qk7zuiw554ffnv5ki9o0p` | ready | 4-account / 3-4 turn checkpoint. |
| `epzwm0i1cbluvcx27ya4caan` | 20 | `ffg4642wm0tz3kyjck2clcl6` | ready | 4-account / 3-4 turn checkpoint. |
| `epzwm0i1cbluvcx27ya4caan` | 25 | `nd9fa56207170mksy8y8n0si` | ready | 4-account / 3-4 turn checkpoint. |
| `epzwm0i1cbluvcx27ya4caan` | 30 | `w704mo9oi3c1xkhs1rcfvpkv` | uploading | Listed as `UPLOADING` when checked shortly after completion; final step-null adapter record was READY. |
| `zhc48qkatvucpcaqvsekd9sm` | 5 | `n76qene09qjhpj2m2aritbff` | ready | 4-account / 4-5 turn batch-64 checkpoint; size `97.8 MB`. |
| `zhc48qkatvucpcaqvsekd9sm` | 10 | `a5q0kzvdknx43chvwhyzy971` | ready | 4-account / 4-5 turn batch-64 checkpoint; size `97.8 MB`. |
| `zhc48qkatvucpcaqvsekd9sm` | 15 | `yrbjyxxzpx5k2l9a4ed3b1wb` | ready | 4-account / 4-5 turn batch-64 checkpoint; size `97.8 MB`. |
| `zhc48qkatvucpcaqvsekd9sm` | 20 | `ghdsz3nypx629ed0rs9sdlne` | ready | 4-account / 4-5 turn batch-64 checkpoint; size `97.8 MB`. |
| `zhc48qkatvucpcaqvsekd9sm` | 25 | `wwht3hl184jyfm8ljgn0u2i6` | ready | 4-account / 4-5 turn batch-64 checkpoint; size `97.8 MB`. |
| `zhc48qkatvucpcaqvsekd9sm` | 30 | `bsaggzj09bu6tt8ln775988e` | uploading | Listed as `UPLOADING` when checked shortly after completion. |
| `o4qsl2ttfmlnf07bba1uo4qg` | 5 | `jgqcni75a42hq2wl0n32uipl` | ready | 4-account / 5-6 turn batch-32 checkpoint; size `97.8 MB`. |
| `o4qsl2ttfmlnf07bba1uo4qg` | 10 | `vng9skx9w55vv7g170x5txqv` | ready | 4-account / 5-6 turn batch-32 checkpoint; size `97.8 MB`. |
| `o4qsl2ttfmlnf07bba1uo4qg` | 15 | `kmxnunmvkdsarvym78h1rmvq` | ready | 4-account / 5-6 turn batch-32 checkpoint; size `97.8 MB`. |
| `o4qsl2ttfmlnf07bba1uo4qg` | 20 | `il9g9z808ex1porlnt8vid4k` | ready | 4-account / 5-6 turn batch-32 checkpoint; size `97.8 MB`. |
| `o4qsl2ttfmlnf07bba1uo4qg` | 25 | `o5clccll0p03wnbn88fk0cor` | ready | 4-account / 5-6 turn batch-32 checkpoint; size `97.8 MB`. |
| `o4qsl2ttfmlnf07bba1uo4qg` | 30 | `ps46j02lp2tkffpsshjy50l0` | uploading | Listed as `UPLOADING` when checked shortly after completion. |
| `t4kf6tmab09foppeih32pvx6` | 5 | `hmgjs08outxgt3dsfe67petw` | ready | 4-account / 6-7 turn Qwen 0.8B checkpoint. |
| `t4kf6tmab09foppeih32pvx6` | 10 | `sh8j5is53v6y2tj6s89smsp7` | ready | 4-account / 6-7 turn Qwen 0.8B checkpoint. |
| `t4kf6tmab09foppeih32pvx6` | 15 | `l7qoz7ropjf0tl1wfezf5wrl` | ready | 4-account / 6-7 turn Qwen 0.8B checkpoint. |
| `t4kf6tmab09foppeih32pvx6` | 20 | `z1vqw7t825bsuc98chke1zpx` | ready | 4-account / 6-7 turn Qwen 0.8B checkpoint. |
| `t4kf6tmab09foppeih32pvx6` | 25 | `y9iapv4l73xz6qd00p144vqv` | ready | 4-account / 6-7 turn Qwen 0.8B checkpoint. |
| `t4kf6tmab09foppeih32pvx6` | 30 | `q7yeyda5oyu0z6lf8nss7jrn` | uploading | Listed as `UPLOADING` when checked shortly after completion. |
| `wc5nvpymcd093n8x9c7yedgt` | 10 | `tdd4d5nwww3u3y4gh00fx6z5` | ready | 4-account / 6-7 turn Qwen 2B checkpoint. |
| `wc5nvpymcd093n8x9c7yedgt` | 15 | `ptt0pry8bk17mtk2yd1n5joy` | ready | 4-account / 6-7 turn Qwen 2B checkpoint. |
| `wc5nvpymcd093n8x9c7yedgt` | 20 | `s7hrmpsr5f2zpczw1mw29y3t` | ready | 4-account / 6-7 turn Qwen 2B checkpoint. |
| `wc5nvpymcd093n8x9c7yedgt` | 25 | `s0x751zonvs1mmwiiykzpkls` | ready | 4-account / 6-7 turn Qwen 2B checkpoint. |
| `wc5nvpymcd093n8x9c7yedgt` | 30 | `y40v7ydq727rjfbgkwg2cdix` | ready | 4-account / 6-7 turn Qwen 2B final checkpoint. |

## Adapter Deployments

| Adapter ID | Source Run | Model String | Status | Notes |
| --- | --- | --- | --- | --- |
| `lz4roaz2jmokl189l0bj7mqq` | `wpw270lopu0vrzyfx9otn6w1` | `meta-llama/Llama-3.2-1B-Instruct:lz4roaz2jmokl189l0bj7mqq` | unloaded after eval | Deployed for trained train/held-out evals, then unloaded; artifact remains READY/deployable. |
| `tipm3xgcydkin391rs5flxm7` | `t06x036p2njx21ts5fi5p4vm` | `Qwen/Qwen3.5-0.8B:tipm3xgcydkin391rs5flxm7` | deploy failed | READY adapter record exists. Deployment remained `DEPLOYING` for several minutes, inference returned 404 model not found, delete refused while deployment was in progress, and a later status check reported `DEPLOY_FAILED` with timeout error. |
| `uuntogrnb6um3esp2c5nkk3d` | `fdzqzv4ridlnhond78eghitd` | `Qwen/Qwen3.5-0.8B:uuntogrnb6um3esp2c5nkk3d` | deploy failed | READY v0.6 adapter record exists. `prime deployments create` returned with deployment status `DEPLOY_FAILED`; later JSON status reported error "Adapter failed to load. Please contact support if this persists." |
| `lsbgjt98s0d1nyv5eofomojx` | `jspr0dm70xv1nzv2jkz8u8ug` | `Qwen/Qwen3.5-0.8B:lsbgjt98s0d1nyv5eofomojx` | deployed | READY final adapter from the resume retry. Initial deployment timed out, but redeploy on June 3, 2026 succeeded; one-shot inference returned a normal greeting. |
| `q5bqdxys3dmb0it2zruvhxw0` | `uvzzmvybz365g0qqgwbo2san` | `Qwen/Qwen3.5-0.8B:q5bqdxys3dmb0it2zruvhxw0` | not deployed | READY final adapter from the 3-account / 2-3 turn difficulty ablation. |
| `oliy9hxwl96qjygs0ciwnrdc` | `uvzzmvybz365g0qqgwbo2san` | `Qwen/Qwen3.5-0.8B:oliy9hxwl96qjygs0ciwnrdc` | not deployed | READY step-29 adapter record from the difficulty ablation. |
| `aqpu5vg4x6wmsbfhxi1q9wp1` | `xn4ncn6hfi6pexy78mtt5cen` | `Qwen/Qwen3.5-0.8B:aqpu5vg4x6wmsbfhxi1q9wp1` | not deployed | READY final adapter from the 3-account / 3-4 turn difficulty ablation retry. |
| `ebi25offqrl587fnfp55bffx` | `epzwm0i1cbluvcx27ya4caan` | `Qwen/Qwen3.5-0.8B:ebi25offqrl587fnfp55bffx` | not deployed | READY final adapter from the 4-account / 3-4 turn difficulty ablation. |
| `dsg66w80rcjhu3kkv0zpdzve` | `t4kf6tmab09foppeih32pvx6` | `Qwen/Qwen3.5-0.8B:dsg66w80rcjhu3kkv0zpdzve` | deployed | READY final adapter from the 4-account / 6-7 turn Qwen 0.8B run; deployed successfully on June 3, 2026 and used for run-scoped held-out eval. |
| `ym5npd2cye3h2zfey3746say` | `wc5nvpymcd093n8x9c7yedgt` | `Qwen/Qwen3.5-2B:ym5npd2cye3h2zfey3746say` | deployed | READY final adapter from the matched 4-account / 6-7 turn Qwen 2B run; deployed successfully on June 3, 2026 and used for run-scoped held-out eval. |

## Rollout Samples

| Run ID | Step | Command | Notes |
| --- | ---: | --- | --- |
| `rdair5n0ca531bxqqvetrok8` | 0 | `prime train rollouts rdair5n0ca531bxqqvetrok8 --step 0 --plain` | 64 samples logged. Samples show placeholder `account` schema copying, multiple ledger blocks, code fences, and verbose malformed outputs. |
| `mngozs87cvyj745q8zaqph9k` | 0 | `prime train rollouts mngozs87cvyj745q8zaqph9k --step 0 --plain` | 64 samples logged. Samples showed outputs that should receive partial local reward, motivating hosted interface debugging. |
| `qh9lqxz5v3s82sjfs03cso8h` | 0 | `prime train rollouts qh9lqxz5v3s82sjfs03cso8h --step 0 --plain` | 64 samples logged. Local replay of a stored dict-shaped sample scored `0.72375`, but hosted reward stayed zero. |
| `msisq47uw7tcnvuxn5aejrbg` | 0 | `prime train rollouts msisq47uw7tcnvuxn5aejrbg --step 0 --plain` | Command returned no samples even though logs said 64 samples were logged; metrics and distributions were available. |
| `wpw270lopu0vrzyfx9otn6w1` | 0, 10, 20, 30, 40 | `prime train rollouts wpw270lopu0vrzyfx9otn6w1 --step <step> --num 5 --plain` | 64 samples logged at each sampled step. Step 20/30/40 samples show many candidate ledgers, code fences, and truncation; high reward often reflects best-candidate answer stuffing rather than one clean answer. |
| `t06x036p2njx21ts5fi5p4vm` | 0, 10, 20, 30, 40 | `prime train rollouts t06x036p2njx21ts5fi5p4vm --step <step> --num 3 --plain` | Step 0 had format errors/code fences; by step 40 sampled outputs were clean and often exact. Step 20 exposed a reward gap: an extra `"total"` key inside `balances` still received high partial reward. |
| `fdzqzv4ridlnhond78eghitd` | 0, 10, 20 | `prime train rollouts fdzqzv4ridlnhond78eghitd --step <step> --num 3 --plain` | Step 0 showed parseable JSON often outside ledger tags and some code fences. By step 20 sampled outputs were format-clean, but several arithmetic/state mistakes still received moderate to high partial reward. |
| `uvzzmvybz365g0qqgwbo2san` | 0, 20 | `prime train rollouts uvzzmvybz365g0qqgwbo2san --step <step> --num 2 --plain` | Step 0 already had parseable outputs but format and arithmetic were mixed. Step 20 sampled outputs were format-clean while still making state/arithmetic errors across 3-turn examples, receiving rewards around `0.75-0.89`. |
| `xvpykb8rxhq1kzg5wtnm9ty6` | 0 | `prime train rollouts xvpykb8rxhq1kzg5wtnm9ty6 --step 0 --num 2 --plain` | First 3-4 turn attempt sampled step 0 before the run stalled at checkpoint 1. Samples showed clean-ish JSON but missing tags in one case and arithmetic/state mistakes in both. |
| `xn4ncn6hfi6pexy78mtt5cen` | 0, 20 | `prime train rollouts xn4ncn6hfi6pexy78mtt5cen --step <step> --num 2 --plain` | Retry step 20 samples were format-clean but still wrong on state/arithmetic; rewards `0.859` and `0.753` despite incorrect balances/totals. |
| `epzwm0i1cbluvcx27ya4caan` | 20 | `prime train rollouts epzwm0i1cbluvcx27ya4caan --step 20 --num 2 --plain` | Step 20 samples were format-clean and high reward (`0.939`, `0.951`) but still had wrong totals, and one sample also had a wrong final balance. |
| `zhc48qkatvucpcaqvsekd9sm` | 0, 20 | `prime train rollouts zhc48qkatvucpcaqvsekd9sm --step <step> --num <n> --plain` | Step 0 sample used code fences and mishandled transfers. Step 20 samples were format-clean and high reward (`0.950`, `0.925`) while totals were wrong; one sample also had a wrong later `cash` balance. |
| `o4qsl2ttfmlnf07bba1uo4qg` | 0, 20 | `prime train rollouts o4qsl2ttfmlnf07bba1uo4qg --step <step> --num <n> --plain` | Step 0 sample was parseable but missed state updates and totals. Step 20 samples were clean one-ledger outputs with rewards `0.854` and `0.897`, but both still failed large negative transfer state and total tracking. |
| `t4kf6tmab09foppeih32pvx6` | 20 | `prime train rollouts t4kf6tmab09foppeih32pvx6 --step 20 --num <n> --plain` | Step 20 samples were clean one-ledger outputs with rewards `0.918` and `0.908`, but still wrong on transfer state and totals; the run also showed a mid-run length/repetition spike around steps 8-16. |
| `wc5nvpymcd093n8x9c7yedgt` | 20 | `prime train rollouts wc5nvpymcd093n8x9c7yedgt --step 20 --num <n> --plain` | Step 20 samples were clean and mostly exact with rewards `0.992` and `0.996`; remaining errors were isolated intermediate totals, not formatting or length problems. |

## Metrics And Distributions

| Run ID | Step | Metric | Value |
| --- | ---: | --- | ---: |
| `rdair5n0ca531bxqqvetrok8` | 0 | reward mean/min/max | `0.0 / 0.0 / 0.0` |
| `rdair5n0ca531bxqqvetrok8` | 0 | solve_none / solve_all | `1.0 / 0.0` |
| `rdair5n0ca531bxqqvetrok8` | 0 | zero_advantage filter | `0.9375` |
| `rdair5n0ca531bxqqvetrok8` | 0 | gibberish filter | `0.0625` |
| `rdair5n0ca531bxqqvetrok8` | 0 | effective_batch_size | `0.0` |
| `rdair5n0ca531bxqqvetrok8` | 0 | truncation rate | `0.125` |
| `rdair5n0ca531bxqqvetrok8` | 0 | mean seq / prefill / decode length | `661.9 / 252.2 / 467.6` |
| `rdair5n0ca531bxqqvetrok8` | 0 | reward distribution | all 128 samples at `0.000` |
| `rdair5n0ca531bxqqvetrok8` | 0 | advantage distribution | all 128 samples at `0.000` |
| `mngozs87cvyj745q8zaqph9k` | 0 | reward mean/min/max | `0.0 / 0.0 / 0.0` |
| `mngozs87cvyj745q8zaqph9k` | 0 | zero_advantage / effective_batch_size | `0.9766 / 0.0` |
| `mngozs87cvyj745q8zaqph9k` | 0 | truncation rate | `0.0391` |
| `qh9lqxz5v3s82sjfs03cso8h` | 0 | reward mean/min/max | `0.0 / 0.0 / 0.0` |
| `qh9lqxz5v3s82sjfs03cso8h` | 0 | zero_advantage / effective_batch_size | `0.9844 / 0.0` |
| `qh9lqxz5v3s82sjfs03cso8h` | 0 | truncation rate | `0.0208` |
| `msisq47uw7tcnvuxn5aejrbg` | 0 | reward mean/min/max | `0.3426 / 0.2125 / 0.6175` |
| `msisq47uw7tcnvuxn5aejrbg` | 0 | zero_advantage / effective_batch_size | `0.0 / 1.0` |
| `msisq47uw7tcnvuxn5aejrbg` | 0 | gibberish / truncation rate | `0.0391 / 0.0223` |
| `msisq47uw7tcnvuxn5aejrbg` | 0 | reward distribution | nonzero spread; bins from `0.000-0.048` through `0.912-0.960` |
| `msisq47uw7tcnvuxn5aejrbg` | 0 | advantage distribution | nonzero spread, roughly `-0.510` to `0.520` |
| `wpw270lopu0vrzyfx9otn6w1` | 0 | reward mean/min/max | `0.3945 / 0.1964 / 0.5269` |
| `wpw270lopu0vrzyfx9otn6w1` | 10 | reward mean/min/max | `0.5724 / 0.4450 / 0.7923` |
| `wpw270lopu0vrzyfx9otn6w1` | 20 | reward mean/min/max | `0.6642 / 0.4818 / 0.9088` |
| `wpw270lopu0vrzyfx9otn6w1` | 30 | reward mean/min/max | `0.7186 / 0.5579 / 0.8916` |
| `wpw270lopu0vrzyfx9otn6w1` | 40 | reward mean/min/max | `0.7735 / 0.5659 / 0.9431` |
| `wpw270lopu0vrzyfx9otn6w1` | 49 | reward mean/min/max | `0.7793 / 0.5801 / 0.9260` |
| `wpw270lopu0vrzyfx9otn6w1` | 0 -> 49 | truncation rate | `0.0433 -> 0.9688` |
| `wpw270lopu0vrzyfx9otn6w1` | 0 -> 49 | mean decode length | `149.3 -> 653.4`, peaking above `829` at step 30 |
| `wpw270lopu0vrzyfx9otn6w1` | 49 | zero_advantage / effective_batch_size | `0.0 / 1.0` |
| `wpw270lopu0vrzyfx9otn6w1` | 40 | reward distribution | 16 samples in `0.950-1.000`; no samples below `0.450` |
| `t06x036p2njx21ts5fi5p4vm` | 0 | reward mean | `0.4507` |
| `t06x036p2njx21ts5fi5p4vm` | 10 | reward / exact-one-ledger / truncation | `0.8546 / 0.9922 / 0.0` |
| `t06x036p2njx21ts5fi5p4vm` | 20 | reward / exact-one-ledger / truncation | `0.9230 / 0.9978 / 0.0` |
| `t06x036p2njx21ts5fi5p4vm` | 30 | reward / exact-one-ledger / truncation | `0.9401 / 1.0000 / 0.0` |
| `t06x036p2njx21ts5fi5p4vm` | 40 | reward / exact-one-ledger / truncation | `0.9453 / 0.9792 / 0.0` |
| `t06x036p2njx21ts5fi5p4vm` | 49 | reward / exact-one-ledger / truncation | `0.9361 / 0.9917 / 0.0` |
| `t06x036p2njx21ts5fi5p4vm` | 47 | best reward mean | `0.9929` |
| `t06x036p2njx21ts5fi5p4vm` | 0 -> 49 | multi-candidate / code-fence / truncation | `0.0083 -> 0.0`, `0.1042 -> 0.0`, `0.0 -> 0.0` |
| `t06x036p2njx21ts5fi5p4vm` | 0 -> 49 | mean decode length | `36.8 -> 43.5` |
| `t06x036p2njx21ts5fi5p4vm` | 0 -> 49 | zero_advantage filter | `0.0 -> 0.75` |
| `fdzqzv4ridlnhond78eghitd` | 0 | reward / exact-one-ledger / truncation | `0.5429 / 0.2383 / 0.0` |
| `fdzqzv4ridlnhond78eghitd` | 10 | reward / exact-one-ledger / truncation | `0.7711 / 0.9414 / 0.0` |
| `fdzqzv4ridlnhond78eghitd` | 20 | reward / exact-one-ledger / truncation | `0.9053 / 0.9961 / 0.0` |
| `fdzqzv4ridlnhond78eghitd` | 25 | best reward mean | `0.9891` |
| `fdzqzv4ridlnhond78eghitd` | 29 | reward / exact-one-ledger / truncation | `0.9157 / 1.0000 / 0.0` |
| `fdzqzv4ridlnhond78eghitd` | 0 -> 20 | multi-candidate / code-fence / truncation | `0.0 -> 0.0`, `0.1641 -> 0.0`, `0.0 -> 0.0` |
| `fdzqzv4ridlnhond78eghitd` | 0 -> 29 | mean decode length | `40.9 -> 39.5` |
| `fdzqzv4ridlnhond78eghitd` | 0 -> 29 | zero_advantage filter | `0.0 -> 0.75` |
| `jspr0dm70xv1nzv2jkz8u8ug` | 25 | reward / exact-one-ledger / truncation | `0.9601 / 1.0000 / 0.0` |
| `jspr0dm70xv1nzv2jkz8u8ug` | 26 | reward / exact-one-ledger / truncation | `0.9272 / 1.0000 / 0.0` |
| `jspr0dm70xv1nzv2jkz8u8ug` | 28 | reward / exact-one-ledger / truncation | `0.9608 / 0.9883 / 0.0` |
| `jspr0dm70xv1nzv2jkz8u8ug` | 29 | reward / exact-one-ledger / truncation | `0.9587 / 1.0000 / 0.0` |
| `jspr0dm70xv1nzv2jkz8u8ug` | 25 -> 29 | multi-candidate / code-fence / truncation | `0.0 -> 0.0`, `0.0 -> 0.0`, `0.0 -> 0.0` |
| `pnm7mpulnx3j8y1oyjz2sxwx` | 25 | reward / exact-one-ledger / truncation | `0.9689 / 1.0000 / 0.0` |
| `pnm7mpulnx3j8y1oyjz2sxwx` | 26 | reward / exact-one-ledger / truncation | `0.9544 / 1.0000 / 0.0` |
| `pnm7mpulnx3j8y1oyjz2sxwx` | 25 -> 26 | multi-candidate / code-fence / truncation | `0.0 -> 0.0`, `0.0 -> 0.0`, `0.0 -> 0.0` |
| `uvzzmvybz365g0qqgwbo2san` | 0 | reward / exact-one-ledger / truncation | `0.5726 / 0.2208 / 0.0` |
| `uvzzmvybz365g0qqgwbo2san` | 10 | reward / exact-one-ledger / truncation | `0.8169 / 0.9297 / 0.0` |
| `uvzzmvybz365g0qqgwbo2san` | 20 | reward / exact-one-ledger / truncation | `0.8749 / 0.9818 / 0.0` |
| `uvzzmvybz365g0qqgwbo2san` | 29 | reward / exact-one-ledger / truncation | `0.9509 / 1.0000 / 0.0` |
| `uvzzmvybz365g0qqgwbo2san` | 0 -> 29 | parseable / code-fence / zero-advantage | `0.9507 -> 1.0000`, `0.1625 -> 0.0`, `0.0 -> 0.0625` |
| `uvzzmvybz365g0qqgwbo2san` | 0 -> 29 | seq length / decode length | `267.4 -> 263.5`, `90.1 -> 86.6` |
| `xvpykb8rxhq1kzg5wtnm9ty6` | 0 | reward / exact-one-ledger / truncation | `0.5601 / 0.2979 / 0.0` |
| `xvpykb8rxhq1kzg5wtnm9ty6` | 1 | reward / exact-one-ledger / truncation | `0.5315 / 0.2719 / 0.0` |
| `xvpykb8rxhq1kzg5wtnm9ty6` | 0 -> 1 | seq length | `337.5 -> 342.2` |
| `xn4ncn6hfi6pexy78mtt5cen` | 0 | reward / exact-one-ledger / truncation | `0.5657 / 0.1654 / 0.0` |
| `xn4ncn6hfi6pexy78mtt5cen` | 3 | reward / seq length / truncation | `0.7553 / 649.0 / 0.0078` |
| `xn4ncn6hfi6pexy78mtt5cen` | 8 | reward / multi-candidate / seq length | `0.7578 / 0.2063 / 648.4` |
| `xn4ncn6hfi6pexy78mtt5cen` | 10 | reward / exact-one-ledger / multi-candidate | `0.8037 / 0.9185 / 0.0528` |
| `xn4ncn6hfi6pexy78mtt5cen` | 20 | reward / exact-one-ledger / multi-candidate | `0.8574 / 0.9877 / 0.0` |
| `xn4ncn6hfi6pexy78mtt5cen` | 29 | reward / exact-one-ledger / solve-all | `0.8789 / 0.9979 / 0.0` |
| `xn4ncn6hfi6pexy78mtt5cen` | 0 -> 29 | parseable / code-fence / multi-candidate | `0.9798 -> 1.0000`, `0.1374 -> 0.0`, `0.0020 -> 0.0` |
| `xn4ncn6hfi6pexy78mtt5cen` | 0 -> 29 | seq length / decode length | `329.3 -> 333.6`, `124.8 -> 124.2` |
| `epzwm0i1cbluvcx27ya4caan` | 0 | reward / exact-one-ledger / truncation | `0.5638 / 0.1917 / 0.0` |
| `epzwm0i1cbluvcx27ya4caan` | 5 | reward / exact-one-ledger / code-fence | `0.7749 / 0.6469 / 0.0083` |
| `epzwm0i1cbluvcx27ya4caan` | 10 | reward / exact-one-ledger / multi-candidate | `0.8304 / 0.9954 / 0.0026` |
| `epzwm0i1cbluvcx27ya4caan` | 20 | reward / exact-one-ledger / solve-all | `0.8891 / 1.0000 / 0.0` |
| `epzwm0i1cbluvcx27ya4caan` | 29 | reward / exact-one-ledger / solve-all | `0.8647 / 0.9980 / 0.0` |
| `epzwm0i1cbluvcx27ya4caan` | 0 -> 29 | parseable / code-fence / multi-candidate | `0.9715 -> 1.0000`, `0.1826 -> 0.0`, `0.0083 -> 0.0` |
| `epzwm0i1cbluvcx27ya4caan` | 0 -> 29 | seq length / decode length | `389.6 -> 381.9`, `163.4 -> 153.3` |
| `jvwvglhzbp2h8abmhtkgf6ri` | 0 -> 1 | reward / seq length | `0.5703 -> 0.6076`, `456.3 -> 455.2` |
| `ylzr995pao3587n4xgjnrj1r` | 0 -> 1 | reward / seq length | `0.5985 -> 0.5867`, `444.9 -> 462.7` |
| `zhc48qkatvucpcaqvsekd9sm` | 0 | reward / exact-one-ledger / code-fence | `0.5661 / 0.2477 / 0.1695` |
| `zhc48qkatvucpcaqvsekd9sm` | 5 | reward / exact-one-ledger / solve-all | `0.6782 / 0.9141 / 0.0` |
| `zhc48qkatvucpcaqvsekd9sm` | 10 | reward / exact-one-ledger / solve-all | `0.8144 / 0.9922 / 0.0` |
| `zhc48qkatvucpcaqvsekd9sm` | 20 | reward / exact-one-ledger / solve-all | `0.8554 / 0.9969 / 0.0` |
| `zhc48qkatvucpcaqvsekd9sm` | 29 | reward / exact-one-ledger / solve-all | `0.8945 / 1.0000 / 0.0` |
| `zhc48qkatvucpcaqvsekd9sm` | 0 -> 29 | parseable / code-fence / multi-candidate | `0.9930 -> 1.0000`, `0.1695 -> 0.0`, `0.0039 -> 0.0` |
| `zhc48qkatvucpcaqvsekd9sm` | 0 -> 29 | seq length / decode length | `449.0 -> 425.2`, `197.4 -> 179.0` |
| `rzu3o8g5dro2qol7qbfbti1y` | - | progress | no completed steps; stopped attempt superseded by batch-32 retry |
| `o4qsl2ttfmlnf07bba1uo4qg` | 0 | reward / exact-one-ledger / code-fence | `0.5675 / 0.1875 / 0.1094` |
| `o4qsl2ttfmlnf07bba1uo4qg` | 5 | reward / exact-one-ledger / solve-all | `0.6581 / 0.9625 / 0.0` |
| `o4qsl2ttfmlnf07bba1uo4qg` | 10 | reward / exact-one-ledger / solve-all | `0.7638 / 1.0000 / 0.0` |
| `o4qsl2ttfmlnf07bba1uo4qg` | 20 | reward / exact-one-ledger / solve-all | `0.7772 / 1.0000 / 0.0` |
| `o4qsl2ttfmlnf07bba1uo4qg` | 29 | reward / exact-one-ledger / solve-all | `0.8483 / 0.9688 / 0.0` |
| `o4qsl2ttfmlnf07bba1uo4qg` | 0 -> 29 | parseable / code-fence / multi-candidate | `0.9688 -> 0.9688`, `0.1094 -> 0.0`, `0.0 -> 0.0` |
| `o4qsl2ttfmlnf07bba1uo4qg` | 0 -> 29 | seq length / decode length | `534.6 -> 541.8`, `248.8 -> 248.8` |
| `t4kf6tmab09foppeih32pvx6` | 0 | reward / exact-one-ledger / code-fence | `0.5686 / 0.2708 / 0.2760` |
| `t4kf6tmab09foppeih32pvx6` | 9 | reward / multi-candidate / truncation | `0.5145 / 0.3092 / 0.2188` |
| `t4kf6tmab09foppeih32pvx6` | 9 | repetition / seq length / decode length | `0.2500 / 14693.8 / 14394.3` |
| `t4kf6tmab09foppeih32pvx6` | 20 | reward / exact-one-ledger / solve-all | `0.8013 / 0.9948 / 0.0` |
| `t4kf6tmab09foppeih32pvx6` | 29 | reward / exact-one-ledger / solve-all | `0.7129 / 0.9911 / 0.0` |
| `t4kf6tmab09foppeih32pvx6` | 0 -> 29 | seq length / decode length | `592.9 -> 609.5`, `281.4 -> 291.5`, with mid-run peak above `14.6K` seq tokens |
| `wc5nvpymcd093n8x9c7yedgt` | 0 | reward / exact-one-ledger / code-fence | `0.7131 / 0.9167 / 0.2500` |
| `wc5nvpymcd093n8x9c7yedgt` | 10 | reward / exact-one-ledger / truncation | `0.9208 / 1.0000 / 0.0` |
| `wc5nvpymcd093n8x9c7yedgt` | 20 | reward / exact-one-ledger / solve-all | `0.9120 / 1.0000 / 0.0` |
| `wc5nvpymcd093n8x9c7yedgt` | 29 | reward / exact-one-ledger / solve-all | `0.9568 / 1.0000 / 0.0` |
| `wc5nvpymcd093n8x9c7yedgt` | 0 -> 29 | parseable / multi-candidate / truncation | `0.9688 -> 1.0000`, `0.0 -> 0.0`, `0.0 -> 0.0` |
| `wc5nvpymcd093n8x9c7yedgt` | 0 -> 29 | seq length / decode length | `601.3 -> 578.7`, `292.3 -> 268.7` |

## Usage

| Run ID | Training Tokens | Input Tokens | Output Tokens | Total Tokens | Cost |
| --- | ---: | ---: | ---: | ---: | ---: |
| `rdair5n0ca531bxqqvetrok8` | `93.99K` | `416.08K` | `185.40K` | `695.47K` | `$0.03` |
| `mngozs87cvyj745q8zaqph9k` | `39.47K` | `91.42K` | `63.08K` | `193.97K` | `$0.0080` |
| `qh9lqxz5v3s82sjfs03cso8h` | `37.22K` | `92.50K` | `74.30K` | `204.02K` | `$0.0085` |
| `msisq47uw7tcnvuxn5aejrbg` | `37.05K` | `94.71K` | `73.03K` | `204.80K` | `$0.0085` |
| `wpw270lopu0vrzyfx9otn6w1` | `5.29M` | `2.84M` | `3.95M` | `12.08M` | `$0.61` |
| `ovhe41qu43r1i3gwo98lw0mq` | `0` | `0` | `0` | `0` | `$0.00` |
| `t06x036p2njx21ts5fi5p4vm` | `1.16M` | `0` | `0` | `1.16M` | `$0.07` |
| `fdzqzv4ridlnhond78eghitd` | `728.46K` | `0` | `0` | `728.46K` | `$0.04` |
| `jspr0dm70xv1nzv2jkz8u8ug` | `111.75K` | `0` | `0` | `111.75K` | `$0.0067` |
| `pnm7mpulnx3j8y1oyjz2sxwx` | `44.85K` | `0` | `0` | `44.85K` | `$0.0027` |
| `uvzzmvybz365g0qqgwbo2san` | `1.07M` | `0` | `0` | `1.07M` | `$0.06` |
| `xvpykb8rxhq1kzg5wtnm9ty6` | `87.45K` | `0` | `0` | `87.45K` | `$0.0052` |
| `xn4ncn6hfi6pexy78mtt5cen` | `1.41M` | `0` | `0` | `1.41M` | `$0.08` |
| `epzwm0i1cbluvcx27ya4caan` | `1.45M` | `0` | `0` | `1.45M` | `$0.09` |
| `jvwvglhzbp2h8abmhtkgf6ri` | `116.64K` | `0` | `0` | `116.64K` | `$0.0070` |
| `ylzr995pao3587n4xgjnrj1r` | `116.03K` | `0` | `0` | `116.03K` | `$0.0069` |
| `zhc48qkatvucpcaqvsekd9sm` | `868.45K` | `0` | `0` | `868.45K` | `$0.05` |
| `rzu3o8g5dro2qol7qbfbti1y` | `0` | `0` | `0` | `0` | `$0.00` |
| `o4qsl2ttfmlnf07bba1uo4qg` | `539.65K` | `0` | `0` | `539.65K` | `$0.03` |
| `t4kf6tmab09foppeih32pvx6` | `2.70M` | `0` | `0` | `2.70M` | `$0.16` |
| `wc5nvpymcd093n8x9c7yedgt` | `562.68K` | `0` | `0` | `562.68K` | `$0.08` |

## Local Files

| Path | Kind | Notes |
| --- | --- | --- |
| `env/meta_memory_state.py` | env source | Deterministic generator, parser, reward, and lazy Verifiers entrypoint. |
| `env/test_meta_memory_state.py` | tests | Sixteen local unit tests for deterministic generation, reward robustness, hosted answer signature, Verifiers message-object handling, anti-stuffing, diagnostics, and v0.6 schema penalties. |
| `env/pyproject.toml` | package metadata | Single-file Verifiers environment packaging scaffold; Prime Hub latest is v0.6.0. |
| `env/README.md` | package metadata | Required by Prime env integration; added after 0.1.0 failed CI. |
| `eval_analysis.py` | eval analysis helper | Summarizes local `results.jsonl` with reward, token, truncation, candidate count, tag, code-fence, parseability, and exact state/total metrics. |
| `configs/llama1b_1step_smoke.toml` | hosted train config | Llama 1B one-step smoke config used for run `rdair5n0ca531bxqqvetrok8`. |
| `configs/llama1b_1step_smoke_v02.toml` | hosted train config | Easier v0.2 Llama 1B one-step smoke config used for run `mngozs87cvyj745q8zaqph9k`. |
| `configs/llama1b_1step_smoke_v03.toml` | hosted train config | v0.3 answer-signature smoke config used for run `qh9lqxz5v3s82sjfs03cso8h`. |
| `configs/llama1b_1step_smoke_v04.toml` | hosted train config | Successful v0.4 message-object-compatible smoke config used for run `msisq47uw7tcnvuxn5aejrbg`. |
| `configs/llama1b_50step_v04.toml` | hosted train config | Completed v0.4 50-step follow-up config used for run `wpw270lopu0vrzyfx9otn6w1`. |
| `configs/llama1b_50step_v05.toml` | hosted train config | Blocked reference config; meta-llama path failed renderer validation and sprints mirror failed free-tier env checks. |
| `configs/qwen08b_50step_v05.toml` | hosted train config | Completed v0.5 Qwen 0.8B anti-stuffing run `t06x036p2njx21ts5fi5p4vm`. |
| `configs/qwen08b_30step_v06.toml` | hosted train config | Completed v0.6 Qwen 0.8B schema-penalty run `fdzqzv4ridlnhond78eghitd`. |
| `configs/qwen08b_30step_v06_resume_from25_retry.toml` | hosted train config | Completed v0.6 Qwen 0.8B resume retry run `jspr0dm70xv1nzv2jkz8u8ug`; regenerated a fresh final adapter. |
| `configs/qwen08b_30step_v06_resume_retry2_from25.toml` | hosted train config | Stopped v0.6 Qwen 0.8B second resume retry run `pnm7mpulnx3j8y1oyjz2sxwx`; launch and native restart both stalled at trainer checkpoint broadcast 26. |
| `configs/qwen08b_30step_v06_diff_3acct_2to3.toml` | hosted train config | Completed v0.6 Qwen 0.8B difficulty ablation run `uvzzmvybz365g0qqgwbo2san`; 3 accounts and 2-3 turns. |
| `configs/qwen08b_30step_v06_diff_3acct_3to4.toml` | hosted train config | Completed v0.6 Qwen 0.8B difficulty ablation retry run `xn4ncn6hfi6pexy78mtt5cen`; 3 accounts and 3-4 turns. First attempt `xvpykb8rxhq1kzg5wtnm9ty6` stalled at checkpoint 1. |
| `configs/qwen08b_30step_v06_diff_4acct_3to4.toml` | hosted train config | Completed v0.6 Qwen 0.8B difficulty ablation run `epzwm0i1cbluvcx27ya4caan`; 4 accounts and 3-4 turns. |
| `configs/qwen08b_30step_v06_diff_4acct_4to5.toml` | hosted train config | Stopped v0.6 Qwen 0.8B batch-128 attempts `jvwvglhzbp2h8abmhtkgf6ri` and `ylzr995pao3587n4xgjnrj1r`; both stalled at trainer checkpoint broadcast 1. |
| `configs/qwen08b_30step_v06_diff_4acct_4to5_b64.toml` | hosted train config | Completed v0.6 Qwen 0.8B batch-64 difficulty ablation run `zhc48qkatvucpcaqvsekd9sm`; 4 accounts and 4-5 turns. |
| `configs/qwen08b_30step_v06_diff_4acct_5to6_b64.toml` | hosted train config | Stopped v0.6 Qwen 0.8B batch-64 difficulty attempt `rzu3o8g5dro2qol7qbfbti1y`; superseded by batch-32 retry. |
| `configs/qwen08b_30step_v06_diff_4acct_5to6_b32.toml` | hosted train config | Completed v0.6 Qwen 0.8B batch-32 difficulty ablation run `o4qsl2ttfmlnf07bba1uo4qg`; 4 accounts and 5-6 turns. |
| `configs/qwen08b_30step_v06_diff_4acct_6to7_b32.toml` | hosted train config | Completed v0.6 Qwen 0.8B batch-32 difficulty run `t4kf6tmab09foppeih32pvx6`; 4 accounts and 6-7 turns. |
| `configs/qwen2b_30step_v06_diff_4acct_6to7_b32.toml` | hosted train config | Completed matched v0.6 Qwen 2B scaling run `wc5nvpymcd093n8x9c7yedgt`; 4 accounts and 6-7 turns. |
| `episode.yaml` | episode record | Structured record with local smoke results and next steps. |
| `notebook.md` | lab notes | Human-readable observations, decisions, and next steps. |

## External Links

| Label | URL | Notes |
| --- | --- | --- |
| Prime env | https://app.primeintellect.ai/dashboard/environments/abugoot/meta-memory-state | Public env `abugoot/meta-memory-state@0.6.0`, content hash `790e961c`; wheel SHA256 `7f801e266c7d6660648af91d6646134bbb661eaf1e75612db49720a2e4b60a70`. |
| 50-step run | https://app.primeintellect.ai/dashboard/training/wpw270lopu0vrzyfx9otn6w1 | Completed Llama 1B follow-up showing reward improvement plus answer-stuffing/truncation. |
| v0.5 Qwen 50-step run | https://app.primeintellect.ai/dashboard/training/t06x036p2njx21ts5fi5p4vm | Completed Qwen 0.8B anti-stuffing follow-up showing reward improvement without candidate stuffing/truncation. |
| v0.6 Qwen 30-step run | https://app.primeintellect.ai/dashboard/training/fdzqzv4ridlnhond78eghitd | Completed Qwen 0.8B schema-penalty follow-up showing clean formatting and short outputs, with arithmetic fidelity still imperfect. |
| v0.6 Qwen resume retry run | https://app.primeintellect.ai/dashboard/training/jspr0dm70xv1nzv2jkz8u8ug | Completed step-25-to-30 retry to regenerate the final adapter. |
| v0.6 Qwen second resume retry run | https://app.primeintellect.ai/dashboard/training/pnm7mpulnx3j8y1oyjz2sxwx | Stopped after repeated trainer checkpoint broadcast stall at step 26. |
| v0.6 Qwen difficulty ablation run | https://app.primeintellect.ai/dashboard/training/uvzzmvybz365g0qqgwbo2san | Completed 3-account / 2-3 turn difficulty ablation. |
| v0.6 Qwen 3-4 turn stopped attempt | https://app.primeintellect.ai/dashboard/training/xvpykb8rxhq1kzg5wtnm9ty6 | Stopped after trainer checkpoint broadcast stall at step 1. |
| v0.6 Qwen 3-4 turn retry | https://app.primeintellect.ai/dashboard/training/xn4ncn6hfi6pexy78mtt5cen | Completed 3-account / 3-4 turn difficulty ablation retry. |
| v0.6 Qwen 4-account 3-4 turn run | https://app.primeintellect.ai/dashboard/training/epzwm0i1cbluvcx27ya4caan | Completed 4-account / 3-4 turn difficulty ablation. |
| v0.6 Qwen 4-account 4-5 turn batch-64 run | https://app.primeintellect.ai/dashboard/training/zhc48qkatvucpcaqvsekd9sm | Completed 4-account / 4-5 turn batch-64 difficulty ablation. |
| v0.6 Qwen 4-account 5-6 turn batch-64 attempt | https://app.primeintellect.ai/dashboard/training/rzu3o8g5dro2qol7qbfbti1y | Stopped with no recorded usage; superseded by batch-32 completion. |
| v0.6 Qwen 4-account 5-6 turn batch-32 run | https://app.primeintellect.ai/dashboard/training/o4qsl2ttfmlnf07bba1uo4qg | Completed 4-account / 5-6 turn batch-32 difficulty ablation. |
| v0.6 Qwen 0.8B 4-account 6-7 turn run | https://app.primeintellect.ai/dashboard/training/t4kf6tmab09foppeih32pvx6 | Completed 4-account / 6-7 turn batch-32 difficulty run with a mid-run length/repetition spike. |
| v0.6 Qwen 2B 4-account 6-7 turn scaling run | https://app.primeintellect.ai/dashboard/training/wc5nvpymcd093n8x9c7yedgt | Completed matched 4-account / 6-7 turn batch-32 scaling run without length/repetition pathology. |
