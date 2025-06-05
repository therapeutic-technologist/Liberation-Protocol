#!/usr/bin/env python
"""
run_demo.py
-----------
One-click wrapper:
1. Tries to import Lava.
2. If missing, installs requirements into current interpreter.
3. Runs demo_attractor.py and prints first 5 lines of the log.
"""

import subprocess, sys, importlib.util, pathlib, time, json

ROOT = pathlib.Path(__file__).resolve().parent
REQ  = ROOT.parent.parent / "requirements.txt"

def ensure_lava():
    if importlib.util.find_spec("lava") is not None:
        return
    print("Lava not found. Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(REQ)])

def run_demo():
    demo_path = ROOT / "demo_attractor.py"
    subprocess.check_call([sys.executable, str(demo_path)])
    log_path = ROOT / "demo_phi.log"
    print("\nFirst 5 log lines:")
    with log_path.open() as fp:
        for _ in range(5):
            print(fp.readline().rstrip())

if __name__ == "__main__":
    ensure_lava()
    run_demo()
