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

import random

import cirq
from cirq.ops import H, X, CNOT, measure

def main():
    qubit_count = 8
    circuit_sample_count = 3

    # Choose qubits to use.
    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    output_qubit = cirq.GridQubit(qubit_count, 0)

    # Pick a secret 2-bit function and create a circuit to query the oracle.
    secret_function = [random.randint(0, 1) for _ in range(2)]
    oracle = make_oracle(q0, q1, secret_function)
    print('Secret function:\nf(x) = <{}>'.format(', '.join(str(e) for e in secret_function)))

    # Embed the oracle into a quantum circuit querying it exactly once.
    circuit = make_deutsch_circuit(q0, q1, oracle)
    print('Circuit:')
    print(circuit)

    # Simulate the circuit.
    simulator = cirq.google.XmonSimulator()
    result = simulator.run(circuit)
    print('Result f(0)⊕f(1):')
    print(result)

def make_oracle(q0, q1, secret_function):
    """ Gates implementing the secret function f(x)."""

    if secret_function[0]:
        yield [CNOT(q0, q1), X(q1)]

    if secret_function[1]:
        yield CNOT(q0, q1)

def make_deutsch_circuit(q0, q1, oracle):
    c = cirq.Circuit()

    # Initialize qubits.
    c.append([X(q1)])
    c.append([H(q0), H(q1)])

    # Query oracle.
    c.append(oracle)

    # Measure in X basis.
    c.append([H(q0), measure(q0, key='result')])
    return c

if __name__ == '__main__':
    main()
