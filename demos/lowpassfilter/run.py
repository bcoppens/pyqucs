import ConfigParser
import copy
import sys

import matplotlib.pyplot as plot
from matplotlib.ticker import MultipleLocator

import circuit
import physical
import pyqucs
import qucsator

# run in this directory as:
# $ PYTHONPATH=../../src python run.py

config = ConfigParser.SafeConfigParser()
config.read('pyqucs.cfg')

# TODO: automatically generate the LowPassFilter from LowPassFilterOriginal :)
base_file_original = "LowPassFilterOriginal"

schematic_original = qucsator.Schematic(config, base_file_original + ".sch")
schematic_original.to_netlist(base_file_original+ ".net")

netlist_original = qucsator.Netlist(base_file_original + ".net")

# Now make this physical
netlist_realisation = copy.deepcopy(netlist_original)

# Use component values from a standard set of components
physical.realise_with_library_components(netlist_realisation)

# If they would have been decently labeled, this was easier:
#capacitors = [ ("C%i" % i) for i in range(1, 5) ]
#inductors = [ ("L%i" % i) for i in range(1, 6) ]
capacitors = [ "C1", "C3", "C5" ]
inductors = [ "L2", "L4" ]

# Set tolerances and distributions, ideally these would already be set in the library, though
# TODO: make the normal tolerances be centered with an appropriately scaled sigma, like so: pyqucs.create_normal(0.18 * 1e-12) ?
for (components, tolerance, distribution) in [ ( capacitors, 5, pyqucs.uniform ),
                                               ( inductors, 5, pyqucs.uniform ) ]:
    for c in components:
        for n in [ netlist_realisation ]:
            comp = netlist_realisation.circuit.get_component(c)
            comp.value.tolerance = tolerance
            comp.value.distribution = distribution

for c in capacitors:
    # Use on purpose a more leaky capacitor, so the difference shows up in the graphs :)
    physical.model_capacitor(netlist_realisation, c, R_L = "10 k", R_ESR = "0.1", L_ESL = "0")

for l in inductors:
    physical.model_inductor(netlist_realisation, l, R_P = "100 M", R_S = "0.1", C_P = "0")
    #physical.model_inductor_Q_SRF(netlist_realisation, l, R_S = 0.1, Q = 12, SRF = 1000e+06)

# TODO: look at the trick from the qucs test cases to wrap the simulation data into multi-dimensional arrays?

def acceptable_circuit(sim):
    for (idx, freq) in enumerate(sim.data["frequency"]):
        # Passband: 0-500MHz
        if freq <= 500e6:
            if sim.data["dBS21"][idx] <= -1.5:
                return False
            if abs(sim.data["S[1,1]"][idx]) >= 0.33:
                return False
            if abs(sim.data["S[2,2]"][idx]) >= 0.33:
                return False
        # Stopband: 1GHz-3GHz (the S-parameter sweep only goes to 2GHz actually)
        # TODO something is wrong here!
        #elif freq >= 1e9 and freq <= 3e9:
        #    if sim.data["dBS21"][idx] >= -40:
                return False
    return True

def sample(netlist, components, nr_trials, callback=None):
    success = 0

    sampled_net = pyqucs.netlist_for_sampling(netlist)

    for trial in range(0, nr_trials):
        for comp in components:
            pyqucs.set_component_to_random_sample(sampled_net, comp)

        sim.simulate(sampled_net)

        if callback is not None:
            callback(sim)

        if acceptable_circuit(sim):
            success += 1

    #...
    return float(success) / float(nr_trials)

# TODO: more flexible, make configurable to only keep a subset, for example only dbS21 and S[1,1] or so
class DataKeeper():
    def __init__(self):
        self.datasets = []
    def __call__(self, sim):
        self.datasets.append(sim.data)

sim = qucsator.Simulation(config)

print "Original acceptable? ..."
sim.simulate(netlist_original)
print acceptable_circuit(sim)

orig_data = sim.data["frequency"], sim.data["dBS21"]

print "More physical model..."
sim.simulate(netlist_realisation)
realisation_data = sim.data["frequency"], sim.data["dBS21"]

print "Sampling 100..."

datakeeper = DataKeeper()

percent_ok = sample(netlist_realisation, capacitors + inductors, 100, callback=datakeeper)

print "%f %% OK" % (100.0*percent_ok)

fig, axes = plot.subplots()

for dataset in datakeeper.datasets:
    plot.plot(dataset["frequency"], dataset["dBS21"], color='grey', alpha=0.5, marker=None, hold=True)
    plot.plot(dataset["frequency"], dataset["dBS11"], color='green', alpha=0.5, marker=None, hold=True)

plot.plot(orig_data[0], orig_data[1], color='black', marker='.', hold=True)
plot.plot(realisation_data[0], realisation_data[1], color='blue', marker='.', hold=True)

plot.axvline(x=500e6, color='red', hold=True, linewidth=2)

plot.ylim(-2, 0)

minorLocator = MultipleLocator(0.25)
axes.yaxis.set_minor_locator(minorLocator)
axes.xaxis.grid(True, which='minor')

plot.show()
