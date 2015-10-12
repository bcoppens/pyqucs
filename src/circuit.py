import re

class RawComponent():
    def __init__(self, str):
        self.name = "<RAW_COMPONENT>"
        self.str = str

    def to_netlist(self):
        return self.str

    def __str__(self):
        return "Raw: '%s'" % self.str

class SimpleComponent():
    # All the other properties are optional, so leave those out for now. Subclasses should override this once optional parameters
    # are supported that differ across components, and I should probably define some kind of setter-method rather than hardcode it in the constructor
    base_string = '%s:%s %%s %%s %s="%%s"\n'

    def __init__(self, name, value, str, port1, port2):
        if str is None:
            str = self.base_string % (self.component_symbol, name, self.component_symbol) # For a resistor, this translates to 'R:name %s %s R="%s"'
        self.str = str
        self.name = name
        self.value = value

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

class Value:
    def __init__(self, str, tolerance=0):
        # TODO: parse pico/femto, etc, sigh
        # TODO: this should just parse a %f + p|n|f|m|etc Ohm|etc?
        s = str.split(" ") # TODO very poor man's parsing, but suffices for now

        self.tolerance = tolerance

        # TODO: with a regex, perhaps? But this definitely suffices for now
        try:
            self.value = float(s[0])
            self.symbolic = False
        except ValueError:
            # It wasn't a valid floating point value, so assume it's a symbolic reference
            self.value = s[0]
            self.symbolic = True

        self.suffices = s[1:]
    def to_netlist(self):
        return " ".join([str(self.value)] + self.suffices)

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
