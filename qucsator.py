import re
import subprocess

import circuit

# Hacky as hell

class Netlist:
    def parse(self, filename):
        self.circuit = circuit.Circuit()
        for line in open(filename, "r"):
            if line.startswith("#") or line == "" or line == "\n": # TODO ...
                continue

            # L:L2 _net0 _net1 L="75nH" I=""
            # TODO: can the name contain a space?
            line_s = line.split(":")
            component_type = line_s[0]
            component_name = line_s[1].split(" ")[0]
            value_regex = None

            if component_type == "L":
                value_regex = 'L="([^\"]+)"'
                replace = 'L="%s"'

                # TODO: factor out with value_regex is not None?
                inductance = re.search(value_regex, line).group(1)
                meta_line = re.sub(value_regex, replace, line)
                component = circuit.Inductor(component_name, inductance, meta_line)
            else:
                component = circuit.RawComponent(line)

            self.circuit.add(component)

    def __str__(self):
        s = ""
        for c in self.circuit.components:
            s += ",%s" % str(c)
        return s

    def output(self, filename):
        # TODO use 'with'?
        file = open(filename, "w")
        for c in self.circuit.components:
            file.write(c.to_netlist())
        file.close()

    def __init__(self, filename):
        self.circuit = None
        self.parse(filename) # sets circuit

class Simulation:
    def simulate(self, netlist):
        netlist_base = self.config.get("DEFAULT", "netlist_tmp_base", vars={"netlist_tmp_base": "temp"})
        netlist_file_in = netlist_base + ".net"
        datafile = netlist_base + ".dat"

        netlist.output(netlist_file_in) # TODO mktemp?
        subprocess.check_call([self.qucsator, "-i", netlist_file_in, "-o", datafile])

    def __init__(self, config):
        self.qucsator = config.get("DEFAULT", "qucsator", vars={"qucsator": "qucsator"})
        self.config = config
