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

def sensitivity(netlist, component_name, sweep_components, trials_per_value):
    net = copy.deepcopy(netlist)

    original_component = netlist.circuit.get_component(component_name)
    component = net.circuit.get_component(component_name)

    ok_samples = []

    for comp_val in pyqucs.equally_spaced(original_component, 20):
        component.value.value = comp_val

        for i in range(0, trials_per_value):
            for other in sweep_components:
                pyqucs.set_component_to_random_sample(netlist, net, other)

            sim.simulate(net)

            if acceptable_circuit(sim):
                ok_samples.append(comp_val) # TODO: this is probably not ideal :)

    return ok_samples


def plot_2_sensitivities(data_r1, data_r2):
    f, (ax1, ax2) = plot.subplots(1, 2, sharey=True)
    ax1.hist(data_r1, 10, histtype='bar')
    ax1.set_title('R1')

    ax2.hist(data_r2, 10, histtype='bar')
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
