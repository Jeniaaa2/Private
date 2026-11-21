import math
import random
import time
from collections import deque

# --------------------------------------------------
# A toy simulation of a single spiking neuron
# --------------------------------------------------
class LeakyIntegrateAndFire:
    def __init__(self, tau_m=20.0, v_rest=-65.0, v_threshold=-50.0, v_reset=-65.0, dt=0.1):
        self.tau_m    = tau_m           # membrane time constant (ms)
        self.v_rest   = v_rest          # resting potential (mV)
        self.v_th     = v_threshold     # spike threshold (mV)
        self.v_reset  = v_reset         # reset potential (mV)
        self.dt       = dt              # integration step (ms)
        self.v_m      = v_rest          # current membrane potential

    def step(self, i_syn):
        """One integration step driven by synaptic input i_syn (nA)."""
        # Exponential decay + input drive
        dv = (-(self.v_m - self.v_rest) + i_syn) * (self.dt / self.tau_m)
        self.v_m += dv

        if self.v_m >= self.v_th:
            self.v_m = self.v_reset
            return True     # spike occurred
        return False          # no spike

# --------------------------------------------------
# A very simple “synapse” that samples a Poisson train
# --------------------------------------------------
class PoissonSpikeSource:
    def __init__(self, rate=10.0, dt=0.1):
        self.rate = rate          # spikes per second
        self.dt   = dt
        self.p    = self.rate * (self.dt / 1000.0)  # probability per step

    def generate(self):
        """Return 1 if a spike occurs, otherwise 0."""
        return 1.0 if random.random() < self.p else 0.0

# --------------------------------------------------
# Core simulation loop
# --------------------------------------------------
def simulate(duration_ms=1000, dt=0.1):
    neuron     = LeakyIntegrateAndFire(dt=dt)
    source     = PoissonSpikeSource(rate=20.0, dt=dt)
    spike_times = []

    t = 0.0
    while t < duration_ms:
        i_syn = 0.5 * source.generate()          # synaptic current (nA)
        spiked = neuron.step(i_syn)
        if spiked:
            spike_times.append(t)
        t += dt
        # Small sleep to mimic real-time if desired
        # time.sleep(dt / 1000.0)

    return spike_times

# --------------------------------------------------
# Entry point
# --------------------------------------------------
if __name__ == "__main__":
    spikes = simulate(duration_ms=1000, dt=0.1)
    print(f"Detected {len(spikes)} spikes in 1 second of simulation.")
    print(f"Spike times (ms): {spikes[:10]}{'...' if len(spikes)>10 else ''}")