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

    def output(self, filename):
        for c in self.circuit.components:
            print c

    def __init__(self, filename):
        self.circuit = None
        self.parse(filename) # sets circuit

class Simulation:
    def simulate():
        pass

    def __init__(self, config):
        self.qucsator = config.get(None, "qucsator", vars={"qucsator": "qucsator"})
