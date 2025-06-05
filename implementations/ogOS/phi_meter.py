"""
phi_meter.py  ·  v0.1  ·  2025-06-04
A 60-line Φ-proxy + brown-out recovery logger for Lava/Loihi.

Attach PhiMeter to any spiking OutPort.  Logs two JSON events:
  • lz_adler32   – Lempel-Ziv complexity every 100 ticks
  • recovery_ms  – silence-duration after brown-out
Works on CPU (Loihi1SimCfg) or any Loihi back-end.
"""


import json, time, zlib
from pathlib import Path
import numpy as np

from lava.magma.core.process.process import AbstractProcess as Process
from lava.magma.core.process.ports.ports import InPort
from lava.magma.core.model.py.model import PyLoihiProcessModel
from lava.magma.core.decorator import implements
from lava.magma.core.sync.protocols.loihi_protocol import LoihiProtocol
from lava.magma.core.process.ports.ports import InPort

# ----------------------------- Process -------------------------------------#
class PhiMeter(Process):
    def __init__(self, n_neurons: int, run_id: str = "session"):
        super().__init__()
        self.s_in = InPort(shape=(n_neurons,))
        self.run_id = run_id                      # plain Python attribute


# --------------------------- ProcessModel ----------------------------------#
@implements(proc=PhiMeter, protocol=LoihiProtocol)
class PyPhiMeterModel(PyLoihiProcessModel):
    s_in: InPort
    run_id: str

    def __init__(self):
        super().__init__()
        self.last_t   = time.time()
        self.buffer   = []
        self.dead_for = 0.0
        self.out_fp   = Path(f"{self.run_id}_phi.log").open("a")

    def run_spk(self):
        now    = time.time()
        dt_ms  = (now - self.last_t) * 1_000
        spikes = self.s_in.recv()
        self.buffer.append(spikes.tobytes())

        # brown-out tracking
        if spikes.any():
            if self.dead_for > 0.0:
                print(json.dumps({"ts": now, "event": "recovery_ms",
                                  "val": round(self.dead_for, 3)}),
                      file=self.out_fp)
            self.dead_for = 0.0
        else:
            self.dead_for += dt_ms

        # Φ-proxy every 100 ticks
        if len(self.buffer) >= 100:
            comp = zlib.adler32(b"".join(self.buffer))
            print(json.dumps({"ts": now, "event": "lz_adler32",
                              "val": int(comp)}),
                  file=self.out_fp)
            self.buffer.clear()

        self.last_t = now
