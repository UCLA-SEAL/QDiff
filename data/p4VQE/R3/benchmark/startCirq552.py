#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/15/20 4:49 PM
# @File    : grover.py

# qubit number=4
# total number=12
import cirq
import cirq.google as cg
from typing import Optional
import sys
from math import log2
import numpy as np

#thatsNoCode

from cirq.contrib.svg import SVGCircuit

# Symbols for the rotation angles in the QAOA circuit.
def make_circuit(n: int, input_qubit):
    c = cirq.Circuit()  # circuit begin

    c.append(cirq.H.on(input_qubit[1]))  # number=2
    c.append(cirq.H.on(input_qubit[2]))  # number=3
    c.append(cirq.H.on(input_qubit[3]))  # number=4
    c.append(cirq.Y.on(input_qubit[3])) # number=5

    c.append(cirq.SWAP.on(input_qubit[1],input_qubit[0])) # number=6
    c.append(cirq.Y.on(input_qubit[2])) # number=8
    c.append(cirq.Y.on(input_qubit[2])) # number=9
    c.append(cirq.CNOT.on(input_qubit[2],input_qubit[0])) # number=10
    c.append(cirq.CNOT.on(input_qubit[2],input_qubit[0])) # number=11
    # circuit end

    c.append(cirq.measure(*input_qubit, key='result'))

    return c

def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)

if __name__ == '__main__':
    qubit_count = 4

    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    circuit = make_circuit(qubit_count,input_qubits)
    circuit = cg.optimized_for_sycamore(circuit, optimizer_type='sqrt_iswap')

    circuit_sample_count =2000

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=circuit_sample_count)

    frequencies = result.histogram(key='result', fold_func=bitstring)
    writefile = open("../data/startCirq552.csv","w+")

    print(format(frequencies),file=writefile)
    print("results end", file=writefile)

    print(circuit.__len__(), file=writefile)
    print(circuit,file=writefile)


    writefile.close()