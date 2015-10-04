import ConfigParser
import numpy as np
import sys

import qucsator

def tolerance_range(component):
    component_value = component.value.value
    delta = component_value * float(component.tolerance) / 100.0
    return (component_value - delta, component_value + delta)

# TODO: factor the range = ... out?
def equally_spaced(component, nr_samples):
    range = tolerance_range(component)
    step = float(range[1] - range[0]) / nr_samples
    return np.arange(range[0], range[1], step=step)

def uniform(component, nr_samples):
    range = tolerance_range(component)
    return np.random.uniform(range[0], range[1], nr_samples)

def sample_component(component, nr_samples):
    # TODO: perhaps this should simple be set in all components
    #sampler = getattr(component, "distribution", equally_spaced)
    sampler = getattr(component, "distribution", uniform)
    return sampler(component, nr_samples)

# TODO: this with the original and new netlist is horrible, components should keep track of their nominal value for cases such as this!
def set_component_to_random_sample(original_netlist, new_netlist, component_name):
    original = original_netlist.circuit.get_component(component_name)
    new = new_netlist.circuit.get_component(component_name)

    sampler = getattr(original, "distribution", uniform)

    new.value.value = sampler(original, 1)[0]

if __name__ == "__main__":
    config = ConfigParser.SafeConfigParser()
    config.read('pyqucs.cfg')

    netlist = qucsator.Netlist("FMLowPass.net")
    print netlist.circuit

    sim = qucsator.Simulation(config)
    sim.simulate(netlist)
