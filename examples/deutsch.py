"""Demonstrates Deutsch's algorithm.

Deutsch's algorithm is one of the simplest demonstrations of quantum parallelism
and interference. It takes a black-box oracle implementing a Boolean function f(x),
and determines whether f(0) and f(1) have the same parity using just one query.
This version of Deutsch's algorithm is a simplified and improved version from
Nielsen and Chuang's textbook.

=== REFERENCE ===

Deutsch, David. "Quantum theory, the Church-Turing Principle and the universal
quantum computer." Proc. R. Soc. Lond. A, 400:97, 1985.

Nielsen, Michael A. and Isaac L. Chuang. "Quantum Computation and Quantum
Information", Cambridge University Press, 2000, pp.32-34.

=== EXAMPLE OUTPUT ===

Secret function:
f(x) = <0, 1>
Circuit:
0: ───────H───@───H───M('result')───
              │
1: ───X───H───X─────────────────────
Result f(0)⊕f(1):
result=1
"""

import random

import cirq
from cirq.ops import H, X, CNOT, measure


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
