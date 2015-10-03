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

    def to_netlist(self):
        return self.str % self.value

class Inductor(SimpleComponent):
    pass

class Resistor(SimpleComponent):
    pass

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
