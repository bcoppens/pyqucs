import ConfigParser
import copy
import numpy as np
import sys

# We want 2 different 'versions' of a circuit:
# * The version that the user created, with the specified nominal values
# * A random sample of that circuit, given the specified tolerances of that user-created circuit
# To create that random sample, it's cleanest to just read the nominal value and sample around that point, and set a new nominal value. However, that
# would overwrite the old value, and if we are iterating in a loop to evaluate multiple circuit instances, they wouldn't be sampling around the same
# original point anymore. But also you don't want to clone a fresh circuit for every such sampling, because that's wasteful.
# And I feel a bit doubtful that having a nominal_value / randomized_value available by default in the user-accessible circuit might lead to 
# a desynchronization if one nominal_value is updated but randomized_value isn't, etc.
# TODO: the above is probably cleaner, but I think about if this could be done with custom getters/setters or so to automatically clean the right values,
# although it might be that then too much happens behind the scenes, and might introduce other subtle errors
#
# Solution (probably not the cleanest one; ): before you
# sample, you use netlist_for_sampling(circuit), which internally clones, and sets nominal_value. set_component_to_random_sample will then
# refer to the nominal_value at all times. Making the netlist_for_sampling explicit will hopefully reduce the risk of desyncing

def netlist_for_sampling(netlist):
    for_sampling = copy.deepcopy(netlist)

    for name, component in for_sampling.circuit.components.iteritems():
        component.initialize_nominal_value()

    return for_sampling

def tolerance_range(component):
    component_value = component.nominal_value.value
    delta = component_value * float(component.nominal_value.tolerance) / 100.0
    return (component_value - delta, component_value + delta)

# TODO: factor the range = ... out?
def equally_spaced(component, nr_samples):
    range = tolerance_range(component)
    step = float(range[1] - range[0]) / nr_samples
    return np.arange(range[0], range[1], step=step)

def uniform(component, nr_samples):
    range = tolerance_range(component)
    return np.random.uniform(range[0], range[1], nr_samples)

# TODO: should this actually mean it is actually a normal but 'cut off' around +/- tolerance?
def normal(component, sigma, nr_samples):
    return np.random.normal(component.nominal_value.value, sigma, nr_samples)

def create_normal(sigma):
    return lambda component, nr_samples: normal(component, sigma, nr_samples)

def sample_component(component, nr_samples):
    # TODO: this *should* be set on values instead, since a component could have multiple values
    sampler = getattr(component, "distribution", uniform)
    return sampler(component, nr_samples)

# This should only be performed on a netlist from netlist_for_sampling
def set_component_to_random_sample(netlist, component_name):
    component = netlist.circuit.get_component(component_name)

    sampler = getattr(component, "distribution", uniform)

    component.value.value = sampler(component, 1)[0]
