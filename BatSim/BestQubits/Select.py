import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate
import mapomatic as mm
import numpy as np
from qiskit import *
import mapomatic as mm
from qutip import *
from qiskit.circuit.library import UnitaryGate

def Q_Physical(Steps, omega, kappa, backend):
    """
    Function to perform a quantum circuit simulation for physical selection.

    Parameters:
    - Steps (int): Number of steps for the collisional model.
    - omega (float): Parameter for the Hamiltonian(driving field).
    - kappa (float): Parameter for the Hamiltonian(coupling stength).
    - backend (qiskit.providers.backend.Backend): Quantum backend for execution.

    Returns:
    - float: Score from the evaluation of layouts for the quantum circuit.
    """
    # Define the Hamiltonian for the physical model
    H = omega * (tensor(sigmax(), qeye(2))) + kappa * (
        tensor(sigmam(), sigmap()) + tensor(sigmap(), sigmam()))

    # Generate the unitary gate from the Hamiltonian
    M_Unitary = (-1j * H).expm()
    M_gate = UnitaryGate(M_Unitary)

    # Quantum circuit setup
    q0 = QuantumRegister(1, name='battery')
    q1 = QuantumRegister(1, name='ancilla')
    creg = ClassicalRegister(Steps + 1)
    qc = QuantumCircuit(q0, q1, creg)

    # Start the collisional model for the specified number of steps
    for i in range(Steps):
        qc.append(M_gate, [q1, q0])
        qc.h(q1)
        qc.measure(q1, creg[i])
        qc.barrier()
        qc.reset(q1)

    # Transpile the circuit for the backend
    trans_qc = transpile(qc, backend)
    small_qc = mm.deflate_circuit(trans_qc)
    layouts = mm.matching_layouts(small_qc, backend)
    scores = mm.evaluate_layouts(small_qc, layouts, backend)

    return scores[0]
