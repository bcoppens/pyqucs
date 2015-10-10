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
    def __init__(self, name, value, str):
        self.str = str
        self.name = name
        self.value = value
        self.tolerance = 10 # a default value, TODO: should this be set everywhere? Probably...

    def to_netlist(self):
        return self.str % self.value.to_netlist()

class Inductor(SimpleComponent):
    pass

class Resistor(SimpleComponent):
    pass

class Value:
    def __init__(self, str):
        # TODO: parse pico/femto, etc, sigh
        # TODO: this should just parse a %f + p|n|f|m|etc Ohm|etc?
        s = str.split(" ") # TODO very poor man's parsing, but suffices for now

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

    def add(self, component):
        self.components_ordered.append(component)
        self.components[component.name] = component

    def __str__(self):
        return str(self.components)

    def get_component(self, name):
        return self.components[name]
