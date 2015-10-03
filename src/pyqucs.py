import ConfigParser
import sys

import qucsator

config = ConfigParser.SafeConfigParser()
config.read('pyqucs.cfg')

netlist = qucsator.Netlist("FMLowPass.net")
print netlist.circuit

sim = qucsator.Simulation(config)
sim.simulate(netlist)
