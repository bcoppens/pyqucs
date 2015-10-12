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
    netlist.circuit.add(circuit.Resistor(r_l, R_L, circuit.Resistor.base_string % r_l, net_begin, net_after_orig))
                        
    l_esl = netlist.circuit.next_internal_name_for("L_ESL")
    netlist.circuit.add(circuit.Inductor(l_esl, L_ESL, circuit.Inductor.base_string % l_esl, net_after_orig, net_after_ind))
                        
    r_esr = netlist.circuit.next_internal_name_for("R_ESR")
    netlist.circuit.add(circuit.Resistor(r_esr, R_ESR, circuit.Resistor.base_string % r_esr, net_after_ind, net_end))
