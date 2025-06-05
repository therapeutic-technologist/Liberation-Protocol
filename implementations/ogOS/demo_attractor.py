"""
demo_attractor.py  –  minimal 100-neuron attractor + Φ-meter
Run via:  python -m implementations.ogOS.demo_attractor
The network writes demo_phi.log with Φ-proxy events.
"""

from .phi_meter import PhiMeter            # ← single, relative import
import numpy as np

from lava.magma.core.process.process import AbstractProcess as Process
from lava.magma.core.process.ports.ports import OutPort
from lava.magma.core.model.py.model import PyLoihiProcessModel
from lava.magma.core.decorator import implements
from lava.magma.core.sync.protocols.loihi_protocol import LoihiProtocol
from lava.magma.core.run_conditions import RunSteps
from lava.magma.core.run_configs import Loihi1SimCfg


# --------------------------- Toy Attractor -------------------------------- #
class ToyAttractor(Process):
    def __init__(self, n=100):
        super().__init__()
        self.a_out = OutPort(shape=(n,))


@implements(proc=ToyAttractor, protocol=LoihiProtocol)
class PyToyAttractorModel(PyLoihiProcessModel):
    a_out: OutPort

    def run_spk(self):
        spikes = (np.random.rand(*self.a_out.shape) < 0.05).astype(np.int8)
        self.a_out.send(spikes)


# ---------------------------- main routine -------------------------------- #
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
