import ConfigParser
import copy
import sys

import pyqucs
import qucsator

# run in this directory as:
# $ PYTHONPATH=../../src python run.py

config = ConfigParser.SafeConfigParser()
config.read('pyqucs.cfg')

base_file = "VoltageDivider"

schematic = qucsator.Schematic(config, base_file + ".sch")
schematic.to_netlist(base_file + ".net")

netlist = qucsator.Netlist(base_file + ".net")

sim = qucsator.Simulation(config)
sim.simulate(netlist)

print "Nominal Vout voltage is: %f " % sim.data["Vout.V"][0]

def acceptable_circuit(sim):
    if sim.data["Vout.V"][0] < 4.0 or sim.data["Vout.V"][0] > 5.0:
        return False
    if sim.data["Rin"][0] < 50 or sim.data["Rin"][0] > 70:
        return False
    return True

def sweep(netlist):
    total   = 0
    success = 0

    net = copy.deepcopy(netlist)

    r1 = net.circuit.get_component("R1")
    r2 = net.circuit.get_component("R2")

    #print pyqucs.sample_component(r1, 70)

    # These come from the original netlist, so we do not sample over the updated values :-)
    for r1_val in pyqucs.sample_component(netlist.circuit.get_component("R1"), 70):
        for r2_val in pyqucs.sample_component(netlist.circuit.get_component("R2"), 70):
            r1.value.value = r1_val
            r2.value.value = r2_val

            sim.simulate(net)

            total += 1
            if acceptable_circuit(sim):
                success += 1

    return float(success) / float(total)

print "Sweeping..."

circuit_yield = sweep(netlist)

print "Yield is %f" % circuit_yield
