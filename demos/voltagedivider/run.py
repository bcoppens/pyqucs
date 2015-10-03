import ConfigParser
import sys

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

print netlist.circuit.get_component("R1").value.value
print netlist.circuit.get_component("R1").value.suffices
