#!/usr/bin/env python3
"""Run all five layers, guard off then guard on, and print the difference.

One command instead of ten. No API key: the model is a scripted stand-in that
emits a fixed sequence of tool calls, so every difference below is the harness
and nothing else.

Run:  python3 run_all.py            all five layers
      python3 run_all.py --layer 3  just layer 3, guard off then on
      python3 run_all.py --list     what the five layers are

Isolating one layer is the point of the pairs: read the two scripts side by side
and the only difference is where the rule lives.
"""
import argparse, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).parent
LAYERS = [
    ("1  Execution boundary", "what the agent is allowed to do"),
    ("2  Sandboxing",         "what it can reach"),
    ("3  Memory persistence", "what survives a restart"),
    ("4  Verification loops", "who checks its work"),
    ("5  Context pipelines",  "what you pay to show it anything"),
]
NAMES = ["01_no_execution_boundary 01_execution_boundary",
         "02_no_sandbox 02_sandboxing",
         "03_no_persistence 03_memory_persistence",
         "04_reviewer_can_write 04_verification_loops",
         "05_no_context_pipeline 05_context_pipelines"]


def last_lines(script, n=2):
    r = subprocess.run([sys.executable, str(ROOT / script)],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        return [f"ERROR: {script} exited {r.returncode}"]
    return [l for l in r.stdout.strip().split("\n") if l.strip()][-n:]


def main():
    p = argparse.ArgumentParser(description="Run the harness layers, guard off then on.")
    p.add_argument("--layer", type=int, choices=range(1, 6), metavar="1-5",
                   help="run one layer instead of all five")
    p.add_argument("--list", action="store_true", help="list the layers and exit")
    a = p.parse_args()

    if a.list:
        for i, (title, question) in enumerate(LAYERS, 1):
            print(f"  {i}  {title.split('  ', 1)[1]:<22} {question}")
        return

    pairs = list(zip(LAYERS, NAMES))
    if a.layer:
        pairs = [pairs[a.layer - 1]]

    for (title, question), pair in pairs:
        bad, good = pair.split()
        print(f"\n\033[1mLayer {title}\033[0m  -  {question}")
        print("  guard OFF")
        for l in last_lines(f"failures/{bad}.py"):
            print(f"    {l}")
        print("  guard ON")
        for l in last_lines(f"layers/{good}.py"):
            print(f"    {l}")
    print("\nSame agent, same script, same system prompt, both times.")
    if a.layer:
        print(f"Run without --layer for the other four, or read layers/ and failures/ side by side.")
    else:
        print("Run python3 test_harness.py to assert every one of those differences.")


if __name__ == "__main__":
    main()
