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
base_file_modified = "LowPassFilter"

schematic_original = qucsator.Schematic(config, base_file_original + ".sch")
schematic_original.to_netlist(base_file_original+ ".net")

schematic = qucsator.Schematic(config, base_file_modified + ".sch")
schematic.to_netlist(base_file_modified + ".net")

netlist_original = qucsator.Netlist(base_file_original + ".net")
netlist = qucsator.Netlist(base_file_modified + ".net")

# Set tolerances and distributions
for (components, tolerance, distribution) in [ ( ["C1", "C5"], 5, pyqucs.create_normal(0.18) ),
                                               ( ["L2", "L4"], 5, pyqucs.uniform ),
                                               ( ["C3"],       5, pyqucs.create_normal(0.29) ) ]:
    for c in components:
        for n in [ netlist, netlist_original ]:
            comp = netlist.circuit.get_component(c)
            comp.value.tolerance = tolerance
            comp.distribution = distribution

# Now make this physical
netlist_realisation = copy.deepcopy(netlist_original)
for c in ["C1", "C3", "C5"]:
    # Use on purpose a more leaky capacitor, so the difference shows up in the graphs :)
    physical.model_capacitor(netlist_realisation, c, R_L = circuit.Value("10 k"), R_ESR = circuit.Value("0"), L_ESL = circuit.Value("0"))

for l in ["L2", "L4"]:
    physical.model_inductor(netlist_realisation, l, R_P = circuit.Value("100 M"), R_S = circuit.Value("0"), C_P = circuit.Value("0"))

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

percent_ok = sample(netlist, ["C1", "C5", "L2", "L4", "C3"], 100, callback=datakeeper)

print "%f %% OK" % (100.0*percent_ok)

fig, axes = plot.subplots()

for dataset in datakeeper.datasets:
    plot.plot(dataset["frequency"], dataset["dBS21"], color='grey', alpha=0.5, marker=None, hold=True)

plot.plot(orig_data[0], orig_data[1], color='black', marker='.', hold=True)
plot.plot(realisation_data[0], realisation_data[1], color='blue', marker='.', hold=True)

plot.ylim(-2, 0)

minorLocator = MultipleLocator(0.25)
axes.yaxis.set_minor_locator(minorLocator)
axes.xaxis.grid(True, which='minor')

plot.show()
