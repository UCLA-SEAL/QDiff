# qubit number=2
# total number=10
import cirq
import qiskit

from qiskit import IBMQ
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import BasicAer, execute, transpile
from pprint import pprint
from qiskit.test.mock import FakeVigo
from math import log2,floor, sqrt, pi
import numpy as np
import networkx as nx

def build_oracle(n: int, f) -> QuantumCircuit:
    # implement the oracle O_f^\pm
    # NOTE: use U1 gate (P gate) with \lambda = 180 ==> CZ gate
    # or multi_control_Z_gate (issue #127)

    controls = QuantumRegister(n, "ofc")
    target = QuantumRegister(1, "oft")
    oracle = QuantumCircuit(controls, target, name="Of")
    for i in range(2 ** n):
        rep = np.binary_repr(i, n)
        if f(rep) == "1":
            for j in range(n):
                if rep[j] == "0":
                    oracle.x(controls[j])
            oracle.mct(controls, target[0], None, mode='noancilla')
            for j in range(n):
                if rep[j] == "0":
                    oracle.x(controls[j])
            # oracle.barrier()
    # oracle.draw('mpl', filename='circuit/deutsch-oracle.png')
    return oracle


def make_circuit(n:int,f) -> QuantumCircuit:
    # circuit begin

    input_qubit = QuantumRegister(n, "qc")
    target = QuantumRegister(1, "qt")
    prog = QuantumCircuit(input_qubit, target)

    # inverse last one (can be omitted if using O_f^\pm)
    prog.x(target)

    # apply H to get superposition
    for i in range(n):
        prog.h(input_qubit[i])

    prog.h(input_qubit[1]) # number=1
    prog.h(input_qubit[1]) # number=4
    prog.h(target)
    prog.barrier()

    # apply oracle O_f
    oracle = build_oracle(n, f)
    prog.append(
        oracle.to_gate(),
        [input_qubit[i] for i in range(n)] + [target])

    # apply H back (QFT on Z_2^n)
    for i in range(n):
        prog.h(input_qubit[i])
    prog.barrier()

    # measure
    #for i in range(n):
    #    prog.measure(input_qubit[i], classicals[i])

    prog.cx(input_qubit[0],input_qubit[1]) # number=7
    prog.x(input_qubit[1]) # number=8
    prog.cx(input_qubit[0],input_qubit[1]) # number=9
    prog.x(input_qubit[1]) # number=3
    prog.cx(input_qubit[1],input_qubit[0]) # number=5
    prog.cx(input_qubit[1],input_qubit[0]) # number=6
    # circuit end
    return prog




if __name__ == '__main__':
    n = 2
    f = lambda rep: rep[-1]
    # f = lambda rep: "1" if rep[0:2] == "01" or rep[0:2] == "10" else "0"
    # f = lambda rep: "0"
    prog = make_circuit(n, f)
    sample_shot =2800
    backend = BasicAer.get_backend('qasm_simulator')

    circuit1 = transpile(prog,FakeVigo())
    circuit1.x(qubit=3)
    circuit1.x(qubit=3)
    circuit1.measure_all()
    prog = circuit1


    info = execute(prog, backend=backend, shots=sample_shot).result().get_counts()

    writefile = open("../data/startQiskit145.csv","w")
    print(info,file=writefile)
    print("results end", file=writefile)
    print(circuit1.depth(),file=writefile)
    print(circuit1,file=writefile)
    writefile.close()
