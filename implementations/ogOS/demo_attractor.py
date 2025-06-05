"""
demo_attractor.py  ·  Minimal 100-neuron recurrent net + PhiMeter.
Run:  python demo_attractor.py
Creates demo_phi.log with Φ-proxy events.
"""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from .phi_meter import PhiMeter
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
#from phi_meter import PhiMeter
from implementations.ogOS.phi_meter import PhiMeter

import sys, pathlib, numpy as np

from lava.magma.core.process.process import AbstractProcess as Process
from lava.magma.core.process.ports.ports import OutPort
from lava.magma.core.model.py.model import PyLoihiProcessModel
from lava.magma.core.decorator import implements
from lava.magma.core.sync.protocols.loihi_protocol import LoihiProtocol
from lava.magma.core.run_conditions import RunSteps
from lava.magma.core.run_configs import Loihi1SimCfg

#from phi_meter import PhiMeter


# --------------------------- Toy Attractor ---------------------------------#
class ToyAttractor(Process):
    def __init__(self, n=100):
        super().__init__()
        self.a_out = OutPort(shape=(n,))          # dtype inferred at runtime


@implements(proc=ToyAttractor, protocol=LoihiProtocol)
class PyToyAttractorModel(PyLoihiProcessModel):
    a_out: OutPort 

    def run_spk(self):
        # Random 5 % spike rate
        spikes = (np.random.rand(*self.a_out.shape) < 0.05).astype(np.int8)
        self.a_out.send(spikes)


# ----------------------------- Build graph ---------------------------------#
N = 100
def main():
    N = 100
    attractor = ToyAttractor(n=N)
    meter     = PhiMeter(n_neurons=N, run_id="demo")
    attractor.a_out.connect(meter.s_in)

    attractor.run(condition=RunSteps(num_steps=10_000),
                  run_cfg=Loihi1SimCfg(select_sub_proc_model=True))
    attractor.stop()
    print("Finished. Check demo_phi.log for output.")


if __name__ == "__main__":
    main()