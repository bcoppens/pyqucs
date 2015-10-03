import ConfigParser
import sys

import qucsator

# run in this directory as:
# $ PYTHONPATH=../../src python run.py

config = ConfigParser.SafeConfigParser()
config.read('pyqucs.cfg')

schematic = qucsator.Schematic(config, "VoltageDivider.sch")
schematic.to_netlist("VoltageDivider.net")

netlist = qucsator.Netlist("VoltageDivider.net")

print netlist.circuit

sim = qucsator.Simulation(config)
sim.simulate(netlist)
