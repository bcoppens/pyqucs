import ConfigParser
import copy
import sys

import matplotlib.pyplot as plot

import pyqucs
import qucsator

# run in this directory as:
# $ PYTHONPATH=../../src python run.py

config = ConfigParser.SafeConfigParser()
config.read('pyqucs.cfg')

base_file = "LowPassFilter"

schematic = qucsator.Schematic(config, base_file + ".sch")
schematic.to_netlist(base_file + ".net")

netlist = qucsator.Netlist(base_file + ".net")

# Set tolerances and distributions
for (components, tolerance, distribution) in [ ( ["C1", "C5"], 5, pyqucs.create_normal(0.18) ),
                                               ( ["L2", "L4"], 5, pyqucs.uniform ),
                                               ( ["C3"],       5, pyqucs.create_normal(0.29) ) ]:
    for c in components:
        comp = netlist.circuit.get_component(c)
        comp.tolerance = tolerance
        comp.distribution = distribution

sim = qucsator.Simulation(config)
sim.simulate(netlist)

#print sim.data


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

def sample(netlist, components, nr_trials):
    success = 0

    net = copy.deepcopy(netlist)

    for trial in range(0, nr_trials):
        for comp in components:
            pyqucs.set_component_to_random_sample(netlist, net, comp)

        sim.simulate(net)

        if acceptable_circuit(sim):
            success += 1

    #...
    return float(success) / float(nr_trials)

#plot.plot(sim.data["frequency"], sim.data["dBS21"])
#plot.ylim(-2, 0)
#plot.show()

print "Original acceptable? ..."
print acceptable_circuit(sim)

print "Sampling 100..."
percent_ok = sample(netlist, ["C1", "C5", "L2", "L4", "C3"], 100)
print "%f %% OK" % (100.0*percent_ok)
