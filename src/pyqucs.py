import ConfigParser
import numpy as np
import sys

import qucsator

def tolerance_range(component_value, tolerance, step=None):
    delta = component_value * float(tolerance) / 100.0
    if step is None:
        return np.arange(component_value - delta, component_value + delta)
    return np.arange(component_value - delta, component_value + delta, step=step)

if __name__ == "__main__":
    config = ConfigParser.SafeConfigParser()
    config.read('pyqucs.cfg')

    netlist = qucsator.Netlist("FMLowPass.net")
    print netlist.circuit

    sim = qucsator.Simulation(config)
    sim.simulate(netlist)
