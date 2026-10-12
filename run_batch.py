#!/usr/bin/env python3
"""run_batch.py — run vibe_bench.py ids sequentially in ONE process (for
long-cap batches that exceed the foreground window). Streams vibe_bench.py's
stdout live. Usage:
  python3 run_batch.py --max-tokens 24000 --results results/bench_vibe_20261011_B24k.jsonl --ids b_html,b_python
All flags pass straight through to vibe_bench.py (same resume-safe semantics:
rows already in --results are skipped)."""
import subprocess
import sys

cmd = [sys.executable, "vibe_bench.py"] + sys.argv[1:]
print(f"[run_batch] {' '.join(cmd)}", flush=True)
sys.exit(subprocess.call(cmd))