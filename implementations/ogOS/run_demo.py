# implementations/ogOS/run_demo.py  (import-and-run wrapper)

import subprocess, sys, pathlib, importlib.util, importlib

ROOT = pathlib.Path(__file__).resolve().parent
REQ  = ROOT.parent.parent / "requirements.txt"
LOG  = ROOT / "demo_phi.log"

def ensure_lava() -> None:
    if importlib.util.find_spec("lava") is None:
        print("Lava not found – installing requirements…")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(REQ)]
        )

def run_demo() -> None:
    # Import exactly once, then alias it so Lava finds the same object
    demo = importlib.import_module("implementations.ogOS.demo_attractor")
    sys.modules["demo_attractor"] = demo        # ← single-name alias

    demo.main()                                 # run the network

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
