"""Demonstrates the Deutsch-Jozsa algorithm.

The Deutsch-Jozsa algorithm takes a black-box oracle implementing a Boolean
promise function f(x) over an n-bit string x, which is either constant for all
values of x, or balanced (i.e., it outputs 1 for exactly half the inputs and 0
for the other half). Any classical algorithm must make 2^{n-1} + 1 queries in
the worst case to determine whether the f(x) is constant or balanced. The
Deutsch-Jozsa algorithm does this using a single query to the oracle.

=== REFERENCE ===

Deutsch, David, and Richard Jozsa. "Rapid solutions of problems by quantum
computation." Proc. R. Soc. Lond. A, 439:553, 1992.

=== EXAMPLE OUTPUT ===

"""

import numpy as np
import random

import cirq


def main():
    qubit_count = 8
    circuit_sample_count = 3

    # Choose qubits to use.
    assert qubit_count % 2 == 0
    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    output_qubit = cirq.GridQubit(qubit_count, 0)

    # Pick a secret constant or balanced function for the oracle and create a
    # circuit to query it.
    secret_function = make_constant_or_balanced_function(qubit_count)
    oracle = make_oracle(input_qubits, output_qubit, secret_function)
    print('Secret function:\nf(x) = <{}>'.format(', '.join(str(e) for e in secret_function)))

    # Embed the oracle into a quantum circuit querying it exactly once.
    circuit = make_deutsch_jozsa_circuit(input_qubits, output_qubit, oracle)
    print('Circuit:')
    print(circuit)

    # # Simulate the circuit.
    # simulator = cirq.google.XmonSimulator()
    # result = simulator.run(circuit)
    # print('Result f(0)⊕f(1):')
    # print(result)

def make_constant_or_balanced_function(qubit_count):
    """ Create either a constant or balanced function, with equal probability."""
    if random.randint(0, 1):
        return [random.randint(0, 1)] * qubit_count
    else:
        balanced = [0] * (qubit_count // 2) + [1] * (qubit_count // 2)
        np.random.shuffle(balanced)
        return balanced

def make_oracle(input_qubits, output_qubit, secret_function):
    """ Gates implementing the secret function f(x)."""

    # TODO: Put in the actually correct oracle.
    if secret_function[0]:
        yield cirq.X(output_qubit)

    for qubit in input_qubits:
        yield cirq.CNOT(qubit, output_qubit)

def make_deutsch_jozsa_circuit(input_qubits, output_qubit, oracle):
    c = cirq.Circuit()

    # # Initialize qubits.
    c.append([
        cirq.X(output_qubit),
        cirq.H(output_qubit),
        cirq.H.on_each(input_qubits),
    ])

    # Query oracle.
    c.append(oracle)

    # Measure in X basis.
    c.append([
        cirq.H.on_each(input_qubits),
        cirq.measure(*input_qubits, key='result')
    ])

    return c

if __name__ == '__main__':
    main()
