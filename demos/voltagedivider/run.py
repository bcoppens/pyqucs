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

base_file = "VoltageDivider"

schematic = qucsator.Schematic(config, base_file + ".sch")
schematic.to_netlist(base_file + ".net")

netlist = qucsator.Netlist(base_file + ".net")

# Set some tolerances that we'll be using later
for r in ["R1", "R2"]:
    netlist.circuit.get_component(r).value.tolerance = 10

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

    sampled_net = pyqucs.netlist_for_sampling(netlist)

    for r1_range in range(0,70):
        pyqucs.set_component_to_random_sample(sampled_net, "R1")

        for r2_range in range(0,70):
            pyqucs.set_component_to_random_sample(sampled_net, "R2")

            sim.simulate(sampled_net)

            total += 1
            if acceptable_circuit(sim):
                success += 1

    return float(success) / float(total)

def sensitivity(netlist, component_name, sweep_components, trials_per_value):
    # This is needed in addition to the set_component_to_random_sample, because I want to sweep over the component values, updating their nominal values
    net = copy.deepcopy(netlist)

    component = net.circuit.get_component(component_name)

    sampled_net_component = pyqucs.netlist_for_sampling(net) # Because equally_spaced needs a netlist_for_sampling, meh. TODO
    sampled_component = sampled_net_component.circuit.get_component(component_name)

    x_vals = []
    y_vals = []

    for comp_val in pyqucs.equally_spaced(sampled_component.value, 20): # This range is created before the component value is updated
        component.value.value = comp_val

        sampled_net = pyqucs.netlist_for_sampling(net)

        success = 0

        for i in range(0, trials_per_value):
            for other in sweep_components:
                pyqucs.set_component_to_random_sample(sampled_net, other)

            sim.simulate(sampled_net)

            if acceptable_circuit(sim):
                success += 1
        x_vals.append(comp_val)
        y_vals.append(float(success)/float(trials_per_value))

    return (x_vals, y_vals)


def plot_2_sensitivities(data_r1, data_r2):
    f, (ax1, ax2) = plot.subplots(1, 2, sharey=True)

    width = data_r1[0][1] - data_r1[0][0]

    ax1.bar(data_r1[0], data_r1[1], width=width)
    ax1.set_title('R1')

    ax2.bar(data_r2[0], data_r2[1], width=width)
    ax2.set_title('R2')

    plot.show()


print "Computing original yield..."
circuit_yield = sweep(netlist)
print "Yield is %f" % circuit_yield

print "Computing sensitivity of R1"
data_r1 = sensitivity(netlist, "R1", ["R2"], 100)

print "Computing sensitivity of R2"
data_r2 = sensitivity(netlist, "R2", ["R1"], 100)

plot_2_sensitivities(data_r1, data_r2)


print "Setting R2 to 27 and doing sensitivity again..."
netlist.circuit.get_component("R2").value.value = 27

print "Computing sensitivity of R1"
data_r1 = sensitivity(netlist, "R1", ["R2"], 100)

print "Computing sensitivity of R2"
data_r2 = sensitivity(netlist, "R2", ["R1"], 100)

plot_2_sensitivities(data_r1, data_r2)

print "Computing final yield..."
circuit_yield = sweep(netlist)
print "Yield is %f" % circuit_yield
