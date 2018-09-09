"""Demonstrates Deutsch's problem.

=== REFERENCE ===

=== EXAMPLE OUTPUT ===

"""

import random

import cirq
from cirq.ops import H, X, measure

def main():
    # Choose qubits to use.
    q0, q1 = [cirq.LineQubit(i) for i in range(2)]

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
    print('Result:')
    print(result)

def make_oracle(q0, q1, secret_function):
    """ Gates implementing the secret function f(x)."""

    if secret_function[0]:
        yield cirq.X(q1)

    if secret_function[0] != secret_function[1]:
        yield cirq.CNOT(q0, q1)

def make_deutsch_circuit(q0, q1, oracle):
    c = cirq.Circuit()

    # Initialize qubits.
    c.append([X(q1)])
    c.append([H(q0), H(q1)])

    # Query oracle.
    c.append(oracle)

    # Measure in X basis.
    # c.append([H(q0), cirq.measure(*q0, key='result')])
    c.append([H(q0), measure(q0, key='result')])
    return c

if __name__ == '__main__':
    main()
