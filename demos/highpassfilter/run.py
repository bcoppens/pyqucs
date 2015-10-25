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
base_file_original = "FMHighPass"

schematic_original = qucsator.Schematic(config, base_file_original + ".sch")
schematic_original.to_netlist(base_file_original+ ".net")

netlist_original = qucsator.Netlist(base_file_original + ".net")

# Now make this physical
netlist_realisation = copy.deepcopy(netlist_original)

# A subset of more specialised components:
coilcraft_0603hp = [
    physical.PhysicalInductor("0603HP-23NXGL", circuit.Value(23e-09, tolerance=2), R_S=0.183, Q=40, SRF=3.00e9),
    physical.PhysicalInductor("0603HP-24NXGL", circuit.Value(24e-09, tolerance=2), R_S=0.074, Q=42, SRF=2.95e9),
    physical.PhysicalInductor("0603HP-27NXGL", circuit.Value(27e-09, tolerance=2), R_S=0.150, Q=44, SRF=2.80e9),
    physical.PhysicalInductor("0603HP-39NXGL", circuit.Value(39e-09, tolerance=2), R_S=0.19,  Q=48, SRF=2.45e9),
    physical.PhysicalInductor("0603HP-43NXGL", circuit.Value(43e-09, tolerance=2), R_S=0.17,  Q=45, SRF=2.45e9)
]

coilcraft_sq = [
    physical.PhysicalInductor("0806SQ-16NGL", circuit.Value(15.7e-09, tolerance=2), R_S=0.009, Q=90, SRF=4.4e9),
    physical.PhysicalInductor("0806SQ-19NGL", circuit.Value(19.4e-09, tolerance=2), R_S=0.010, Q=90, SRF=4.0e9),

    physical.PhysicalInductor("0807SQ-17NGL", circuit.Value(17.0e-09, tolerance=2), R_S=0.009, Q=100, SRF=4.0e9),
    physical.PhysicalInductor("0807SQ-22NGL", circuit.Value(22.0e-09, tolerance=2), R_S=0.010, Q=100, SRF=3.5e9),

    physical.PhysicalInductor("0908SQ-17NGL", circuit.Value(16.6e-09, tolerance=2), R_S=0.008, Q=130, SRF=3.4e9),
    physical.PhysicalInductor("0908SQ-25NGL", circuit.Value(25.0e-09, tolerance=2), R_S=0.010, Q=130, SRF=2.5e9),
    physical.PhysicalInductor("0908SQ-28NGL", circuit.Value(27.3e-09, tolerance=2), R_S=0.010, Q=130, SRF=3.2e9),
]

coilcraft = coilcraft_0603hp + coilcraft_sq

murata = [
    physical.CapacitorModel(circuit.Value(18e-12, tolerance="1"), name="GRM1885C1H180FA01D"),
    physical.CapacitorModel(circuit.Value(20e-12, tolerance="1"), name="GRM1885C1H200FA01D")
]

library_components = physical.map_library_components(netlist_realisation, inductor_library=coilcraft, capacitor_library=murata)
physical.print_library_map(netlist_realisation, library_components)

physical.substitute_library_components(netlist_realisation, library_components)

capacitors = [ ("C%i" % i) for i in range(1, 7) ]
inductors = [ ("L%i" % i) for i in range(1, 8) ]

for c in capacitors:
    # Use on purpose a more leaky capacitor, so the difference shows up in the graphs :)
    physical.model_capacitor(netlist_realisation, c, R_L = "10 k", R_ESR = "0.1", L_ESL = "1 nH")

# TODO: look at the trick from the qucs test cases to wrap the simulation data into multi-dimensional arrays?

def acceptable_circuit(sim):
    for (idx, freq) in enumerate(sim.data["frequency"]):
        # Passband: after 137MHz
        if freq >= 137e6:
            if sim.data["dBS21"][idx] <= -1:
                return False
        # Stopband: below 110MHz
        if freq <= 110e6:
            if sim.data["dBS21"][idx] >= -15:
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

plot.axvline(x=137e6, color='red', hold=True, linewidth=1)
plot.axvline(x=110e6, color='red', hold=True, linewidth=1)

plot.ylim(-20, 0)

minorLocator = MultipleLocator(0.25)
axes.yaxis.set_minor_locator(minorLocator)
axes.xaxis.grid(True, which='minor')

plot.show()
