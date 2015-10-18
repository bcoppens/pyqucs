import circuit

# All these functions 'destructively' update the netlist

# Replace a capacitor in a netlist with set of passive components that model capacitor leakage R_L, equivalent series resistance R_ESR and equivalent series inductance L_ESL
def model_capacitor(netlist, capacitor, R_L, R_ESR, L_ESL):
    c = netlist.circuit.get_component(capacitor)
    
    net_begin = c.port1
    net_end   = c.port2

    net_after_orig = netlist.circuit.next_internal_name_for("after_orig")
    net_after_ind  = netlist.circuit.next_internal_name_for("after_ind")

    c.port2 = net_after_orig

    r_l = netlist.circuit.next_internal_name_for("R_L")
    netlist.circuit.add(circuit.Resistor(r_l, R_L, None, net_begin, net_after_orig))
                        
    l_esl = netlist.circuit.next_internal_name_for("L_ESL")
    netlist.circuit.add(circuit.Inductor(l_esl, L_ESL, None, net_after_orig, net_after_ind))
                        
    r_esr = netlist.circuit.next_internal_name_for("R_ESR")
    netlist.circuit.add(circuit.Resistor(r_esr, R_ESR, None, net_after_ind, net_end))

# Replace an inductor in a netlist with set of passive components that model parallel losses R_P (such as core losses), self-capacitance C_P, and the conductive resitance R_S
def model_inductor(netlist, inductor, R_P, R_S, C_P):
    l = netlist.circuit.get_component(inductor)

    net_begin = l.port1
    net_end   = l.port2

    net_after_orig = netlist.circuit.next_internal_name_for("after_orig")

    l.port2 = net_after_orig

    r_s = netlist.circuit.next_internal_name_for("R_S")
    netlist.circuit.add(circuit.Resistor(r_s, R_S, None, net_after_orig, net_end))

    c_p = netlist.circuit.next_internal_name_for("C_P")
    netlist.circuit.add(circuit.Capacitor(c_p, C_P, None, net_begin, net_end))

    r_p = netlist.circuit.next_internal_name_for("R_P")
    netlist.circuit.add(circuit.Resistor(r_p, R_P, None, net_begin, net_end))
