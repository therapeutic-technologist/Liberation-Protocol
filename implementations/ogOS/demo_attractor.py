from lava.magma.core.process.process import Process
from lava.magma.core.process.ports.ports import OutPort
from lava.magma.core.model.py.model import PyLoihiProcessModel
from lava.magma.core.run_conditions import RunSteps
from lava.magma.core.run_configs import Loihi1SimCfg
import numpy as np

# 1. Minimal spiking process ---------------------------------
class ToyAttractor(Process):
    def __init__(self, n=100):
        super().__init__()
        self.a_out = OutPort(shape=(n,))

class PyToyAttractorModel(PyLoihiProcessModel):
    a_out: OutPort
    def run_spk(self):
        # send a random 5 % of neurons as spikes each tick
        spikes = np.random.rand(*self.a_out.shape) < 0.05
        self.a_out.send(spikes)

# 2. Instantiate network -------------------------------------
N = 100
attractor = ToyAttractor(n=N)

# 3. Attach your PhiMeter ------------------------------------
from phi_meter import PhiMeter   # assumes phi_meter.py is in same dir
meter = PhiMeter(n_neurons=N, run_id="demo")

attractor.a_out.connect(meter.s_in)

# 4. Run for 10 k steps on any Loihi or CPU back-end ----------
from lava.magma.core.run_configs import RunConfig
attractor.run(condition=RunSteps(num_steps=10_000),
              run_cfg=Loihi1SimCfg(select_sub_proc_model=True))
attractor.stop()
