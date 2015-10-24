import copy
import numbers
import re

class RawComponent():
    def __init__(self, str):
        self.name = "<RAW_COMPONENT>"
        self.str = str

    # See the comment at the top of pyqucs.py
    def initialize_nominal_value(self):
        pass

    def to_netlist(self):
        return self.str

    def __str__(self):
        return "Raw: '%s'" % self.str

class SimpleComponent():
    # All the other properties are optional, so leave those out for now. Subclasses should override this once optional parameters
    # are supported that differ across components, and I should probably define some kind of setter-method rather than hardcode it in the constructor
    base_string = '%s:%s %%s %%s %s="%%s"\n'

    def initialize_nominal_value(self):
        self.nominal_value = copy.deepcopy(self.value) # TODO, sigh

    def __init__(self, name, value, str, port1, port2):
        if str is None:
            str = self.base_string % (self.component_symbol, name, self.component_symbol) # For a resistor, this translates to 'R:name %s %s R="%s"'
        self.str = str
        self.name = name
        self.value = value
        self.nominal_value = None

        self.port1 = port1
        self.port2 = port2

    def to_netlist(self):
        return self.str % (self.port1, self.port2, self.value.to_netlist()) # TODO: include self.name

class Inductor(SimpleComponent):
    component_symbol = "L"

class Capacitor(SimpleComponent):
    component_symbol = "C"

class Resistor(SimpleComponent):
    component_symbol = "R"

unitprefixes = { "E": 1e+18, "P": 1e+15, "T": 1e+12, "G": 1e+09, "M": 1e+06, "k": 1e+03, "m": 1e-03, "u": 1e-06, "n": 1e-09, "p": 1e-12, "f": 1e-15 }
units = set({"S", "s", "K", "H", "F", "Hz", "V", "A", "W", "m"})

class Value:
    def __init__(self, v, tolerance=0):
        self.tolerance = tolerance
        self.unit = ""
        self.symbolic = False

        if isinstance(v, float) or isinstance(v, numbers.Integral):
            self.value = v
            return

        str = v

        # TODO very poor man's parsing, but suffices for now, in the end I might want to make an actual parser here
        # This means that the suffixes should be split from the value by spaces for now...
        s = str.split(" ")

        # TODO: with a regex, perhaps? But this definitely suffices for now
        try:
            self.value = float(s[0])

            # Try to parse some suffixes. Doesn't parse them all, though... (in particular, when a unit partially prefix overlaps with a unit, like f(emto) and f(eet) TODO?)
            suffixes = "".join(s[1:])
            for pos, char in enumerate(suffixes):

                # For now, this allows for multiple unit prefixes and units combined...
                if char == "O" and suffixes[pos:pos+3] == "Ohm":
                    self.unit = "Ohm"
                elif char == "H" and suffixes[pos:pos+2] == "Hz":
                    self.unit = "Hz"
                elif char in unitprefixes:
                    self.value = unitprefixes[char] * self.value
                elif char in units:
                    self.unit = char
                else:
                    print "Warning: Unknown suffix '%s' in '%s'" % (char, str)

        except ValueError:
            # It wasn't a valid floating point value, so assume it's a symbolic reference
            self.value = str
            self.symbolic = True

    def to_netlist(self):
        return " ".join([str(self.value)] + [self.unit])

class Circuit:
    def __init__(self):
        self.components_ordered = []
        self.components = {}

        self.internal_names = {} # map prefix -> highest id

    def add(self, component):
        self.components_ordered.append(component)
        self.components[component.name] = component

    def next_internal_name_for(self, prefix):
        if prefix in self.internal_names:
            next = self.internal_names[prefix] + 1
        else:
            next = 0

        self.internal_names[prefix] = next

        return "%s_pyqucs_internal_%i" % (prefix, next)

    def __str__(self):
        return str(self.components)

    def get_component(self, name):
        return self.components[name]
