#!/usr/bin/env python
"""run_demo.py – one-click wrapper for the Φ-meter demo (import-and-run)."""

import importlib, sys, pathlib, importlib.util, subprocess

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

ROOT = pathlib.Path(__file__).resolve().parent
REQ  = ROOT.parent.parent / "requirements.txt"
LOG  = ROOT / "demo_phi.log"


def ensure_lava() -> None:
    """Install Lava + NumPy if Lava is not importable."""
    if importlib.util.find_spec("lava") is not None:
        return
    print("Lava not found – installing requirements...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", str(REQ)]
    )


def run_demo() -> None:
    """Import the demo module and call its main() function."""
    demo = importlib.import_module("implementations.ogOS.demo_attractor")
    demo.main()                       # <-- runs the network right here

    if LOG.exists():
        print("\nFirst 5 log lines:")
        with LOG.open() as fp:
            for _ in range(5):
                print(fp.readline().rstrip())
    else:
        print("⚠ demo_phi.log was not created.")


if __name__ == "__main__":
    ensure_lava()
    run_demo()
