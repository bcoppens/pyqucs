class RawComponent():
    def __init__(self, str):
        self.str = str

    def to_netlist(self):
        return self.str

    def __str__(self):
        return "Raw: '%s'" % self.str

class Inductor():
    def __init__(self, name, inductance, str):
        self.str = str
        self.name = name
        self.inductance = inductance

    def to_netlist(self):
        return self.str % self.inductance

    def __repr__(self):
        return "Inductor %s @ %s '%s'" % (self.name, self.inductance, self.str)

class Circuit:
    def __init__(self):
        self.components = []

    def add(self, component):
        self.components.append(component)

    def __str__(self):
        return str(self.components)
