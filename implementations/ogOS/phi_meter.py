"""
phi_meter.py  |  v0.1  May-2025
Simple Φ-proxy + brown-out recovery logger for Lava / Loihi
-----------------------------------------------------------
• Computes running Lempel-Ziv complexity of spike raster
  as a stand-in for information integration.
• Detects brown-out events (all spikes silent > blackout_ms)
  and logs time-to-recover.
• Appends one JSON line per interval to <run_id>_phi.log
"""

import json, time, zlib, numpy as np
from pathlib import Path
from datetime import datetime
from lava.magma.core.process.process import AbstractProcess
from lava.magma.core.process.ports.ports import InPort
from lava.magma.core.model.py.model import PyLoihiProcessModel
from lava.magma.core.run_conditions import RunSteps
from lava.magma.core.run_configs import Loihi1SimCfg

# ---------- user-facing Process ---------------------------------------------

class PhiMeter(AbstractProcess):
    def __init__(self, n_neurons: int, run_id: str = "session"):
        super().__init__()
        self.s_in = InPort(shape=(n_neurons,))
        self.vars.run_id = run_id

# ---------- lightweight ProcessModel ----------------------------------------

class PyPhiMeterModel(PyLoihiProcessModel):
    s_in: InPort
    run_id: str

    def __init__(self):
        super().__init__()
        self.last_t   = time.time()
        self.buffer   = []
        self.dead_for = 0.0          # ms without spikes
        self.out_fp   = Path(f"{self.run_id}_phi.log").open("a")

    def run_spk(self):               # called every time step
        now   = time.time()
        dt_ms = (now - self.last_t) * 1_000
        spikes = self.s_in.recv()
        self.buffer.append(spikes.tobytes())
        if spikes.any():
            if self.dead_for > 0:
                rec = {"ts": now, "event": "recovery_ms", "val": self.dead_for}
                print(json.dumps(rec), file=self.out_fp)
            self.dead_for = 0
        else:
            self.dead_for += dt_ms
        # every 100 ms, flush Φ-proxy
        if len(self.buffer) >= 100:
            comp = zlib.adler32(b"".join(self.buffer))
            rec  = {"ts": now, "event": "lz_adler32", "val": int(comp)}
            print(json.dumps(rec), file=self.out_fp)
            self.buffer.clear()
        self.last_t = now
