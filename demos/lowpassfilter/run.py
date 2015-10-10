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

sim = qucsator.Simulation(config)
sim.simulate(netlist)

print sim.data



def acceptable_circuit(sim):
    return True

def sweep(netlist):
    total   = 0
    success = 0

    net = copy.deepcopy(netlist)

    r1 = net.circuit.get_component("R1")
    r2 = net.circuit.get_component("R2")
    #...
    return float(success) / float(total)

plot.plot(sim.data["frequency"], sim.data["dBS21"])
plot.ylim(-2, 0)
plot.show()

print "Original acceptable? ..."
print acceptable_circuit(sim)
