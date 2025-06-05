#!/usr/bin/env python
"""
run_demo.py  –  one-click launcher
• Verifies Lava import; if missing (local clone) installs from requirements.
• Runs demo_attractor.py and prints first 5 log lines.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from phi_meter import PhiMeter

import subprocess, sys, importlib.util, pathlib

ROOT  = pathlib.Path(__file__).resolve().parent
REQ   = ROOT.parent.parent / "requirements.txt"
DEMOP = ROOT / "demo_attractor.py"
LOG   = ROOT / "demo_phi.log"


def ensure_lava():
    if importlib.util.find_spec("lava") is not None:
        return
    print("Lava not found – installing requirements...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", str(REQ)]
    )


def run_demo():
    subprocess.check_call([sys.executable, str(DEMOP)])

    print("\nFirst 5 log lines:")
    with LOG.open() as fp:
        for _ in range(5):
            print(fp.readline().rstrip())


if __name__ == "__main__":
    ensure_lava()
    run_demo()
