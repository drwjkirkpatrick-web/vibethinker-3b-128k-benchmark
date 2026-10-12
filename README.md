# VibeThinker-3B 128K benchmark — runbook & settings

**Model:** VibeThinker-3B Q4_K_M (1.93 GB, qwen2 arch) — native ctx **131072 (128K)**,
NO YaRN needed at 64K. No MTP/DSpark drafter exists for it. ChatML template with
native tool calls, **no template thinking-switch** — its reasoning is emitted as
visible content (meta-planning + prompt restatement before every deliverable).

**Tested config:** `-c 65536` f16 KV (64K, 2× headroom under native), `-ngl 99`,
`-b 512 -ub 512 -fa on --jinja --fit off -np 1 -t 6`. Sampling per request:
temp 0.3, top_p 0.95, top_k 40, min_p 0.0 (standard suite sampling).

## Cap profile v3 (saved 2026-10-11 night — the default going forward)

**A 6500 · B 24000 · C 4096 (function-call 1024) · D 3072**

B was doubled to 24K after VibeThinker truncated 3/3 B-prompts at the 2000 cap
*and* still hit 4000 (b_html, b_python) — a deep-budget probe to find where
verbose models actually complete; trim once measured. Historical profiles for
apples-to-apples: v2 (B 4000), v1 (A 6000, B 2000, C 2048/512, D 1024).
Canonical spec: `~/projects/lfm25-3b-64k-benchmark/prompts_abcd.json` (v3).

## Launch safety — the rules that keep llama-server alive

1. `vibe_bench.py` launches every llama-server with `start_new_session` (setsid)
   and kills via bracket patterns (`[l]lama-server`) — a killed runner never
   orphans a server, and kill_server never matches its own wrapper cmdline.
2. **Long batches** (any test that can exceed the ~420 s foreground window —
   6K+ tokens at this model's 20 tok/s): run the sequential runner via the
   terminal tool with `background=true, notify=true`:
   `python3 run_batch.py --max-tokens 24000 --results results/bench_vibe_20261011_B24k.jsonl --ids b_html,...`
   Tracked, timeout-proof, survives context switches; JSONL resume skips done ids.
3. **NEVER** shell-level `setsid nohup ... & disown` wrappers — refused by the
   terminal tool, and they bypass process tracking entirely.
4. Foreground calls only for batches that fit the window (~<5 min total).
5. Keepalive cron stays PAUSED during campaigns (comment the line); restore
   after: uncomment, `~/bin/llm-64k start`, curl `/health`.

## Results state

| File | What |
|---|---|
| `results/bench_vibe_20261011.jsonl` | D @1024 (12) + B @2000 (3, all truncated) |
| `results/bench_vibe_20261011_D3072.jsonl` | D @3072 retest — 3/12 truncated, traps 5/5 |
| `results/bench_vibe_20261011_A6500.jsonl` | A @6500 — 4/5 clean, a_iambic hard loop |
| `results/grades_D3072.json`, `results/grades_A6500.json` | graded verdicts |
| `results/bench_vibe_20261011_B4000.jsonl` | b_html/b_python @4000 (truncated) |
| `results/bench_vibe_20261011_B24k.jsonl` | B @24000 deep-budget run (in progress) |

Headline so far: flat **20.3 tok/s** (no drafter), RSS 4.75 GB, ~8 s loads,
traps 5/5, honest math/code — but heavy visible meta-reasoning burns 3–10× the
tokens of Qwen/LFM per deliverable, with hard loops on strict-form poetry and
open-ended deduction (switches/boxes/piano).
