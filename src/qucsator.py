import os
import re
import subprocess

import circuit

# This entire file is hacky as hell! The way these files are 'parsed' is totally fragile. On the other hand, the 'formats' are not really well-defined to start with
# This works for Qucs 0.0.19 (some git checkout)

# TODO: Python 3.4 has subprocess.DEVNULL
DEVNULL = open(os.devnull, 'wb')

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

            # These simple passive component definitions all have the same form for what we're interested in
            simple_models = { "C": circuit.Capacitor, "L": circuit.Inductor, "R": circuit.Resistor  }
            if component_type in simple_models:
                value_regex = '%s="([^\"]+)"' % component_type
                replace = '%s="%%s"' % component_type # => "R=%s" for example
                type = simple_models[component_type]

                # TODO: check that this is ok for polarized caps
                params = line_s[1].split(" ")

                value = circuit.Value(re.search(value_regex, line).group(1))
                meta_line = re.sub(value_regex, replace, line)
                meta_line = re.sub("^(%s:[^ ]+) ([^ ]+) ([^ ]+)" % component_type, "\\1 %s %s", meta_line) # Make the netlist names replacable
                component = type(component_name, value, meta_line, port1=params[1], port2=params[2])
            else:
                component = circuit.RawComponent(line)

            self.circuit.add(component)

    def __str__(self):
        s = ""
        for c in self.circuit.components_ordered:
            s += ",%s" % str(c)
        return s

    def output(self, filename):
        # TODO use 'with'?
        file = open(filename, "w")
        for c in self.circuit.components_ordered:
            file.write(c.to_netlist())
        file.close()

    def __init__(self, filename):
        self.circuit = None
        self.parse(filename) # sets circuit

class Schematic:
    def __init__(self, config, filename):
        self.filename = filename
        self.qucs = config.get("DEFAULT", "qucs", vars={"qucs": "qucs"})
        self.config = config

    def to_netlist(self, netlist_file):
        subprocess.check_call([self.qucs, "--netlist", "-i", self.filename, "-o", netlist_file], stdout=DEVNULL, stderr=DEVNULL)

class Simulation:
    def parse_datapoint(self, line):
        # Horrible format
        #   -3.3e+01
        #   -1.2e-01-j8.4e-02

        regex_re = "([+-])(\d+.\d+e[+-]\d+|inf|nan)([+-]?)" # The last group matches the sign of the imaginary part, if any
        regex_im = "(\d+.\d+e[+-]\d+|inf|nan)"
        components = line.split("j")
        m = re.search(regex_re, components[0])

        r = float(m.group(2))
        negative = (m.group(1) == '-')
        if negative:
            r = -r

        if len(components) > 1:
            negative = (m.group(3) == '-')
            m = re.search(regex_im, components[1])
            i = float(m.group(1))
            if negative:
                i = -i
            return complex(r, i)
        return r

    def read_from_datafile(self, datafile):
        # TODO more rigorous testing with more complext netlist files (multiple simulations)
        self.data = {}
        self.depends = {}

        current_datalist = None
        current_name = None

        for line in open(datafile, "r"):
            if line.startswith("<indep "):
                current_name = line.split(" ")[1] # TODO: verify that we read in as much data lines as claimed in [2] here?
                current_datalist = []

            elif line.startswith("</indep>") or line.startswith("</dep>"):
                self.data[current_name] = current_datalist
                current_datalist = None

            elif line.startswith("<dep "):
                regex = "<dep ([^ ]+) ([^>]+)>"
                m = re.search(regex, line)
                current_name = m.group(1)
                dependent = m.group(2)

                self.depends[current_name] = dependent
                current_datalist = []

            elif current_datalist is not None:
                current_datalist.append(self.parse_datapoint(line))

    def simulate(self, netlist):
        netlist_base = self.config.get("DEFAULT", "netlist_tmp_base", vars={"netlist_tmp_base": "temp"})
        netlist_file_in = netlist_base + ".net"
        datafile = netlist_base + ".dat"

        netlist.output(netlist_file_in) # TODO mktemp?
        subprocess.check_call([self.qucsator, "-i", netlist_file_in, "-o", datafile], stdout=DEVNULL, stderr=DEVNULL)

        self.read_from_datafile(datafile)

    def __init__(self, config):
        self.qucsator = config.get("DEFAULT", "qucsator", vars={"qucsator": "qucsator"})
        self.config = config
