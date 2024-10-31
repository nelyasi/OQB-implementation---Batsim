from qiskit import transpile, QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from math import exp

def Noise_Data(backend, shots, qubits, simulator):
    """
    Perform measurements on a quantum backend to extract probabilities and decoherence rates.

    Parameters:
    - backend (qiskit.providers.backend.Backend): Quantum backend to run the circuits.
    - shots (int): Number of shots for each circuit execution.
    - qubits (list): List of qubit indices, where qubits[0] is the Battery qubit and qubits[1] is the Ancilla qubit.
    - simulator (bool): True if using a simulator backend, False otherwise.

    Returns:
    - P01 (float): Probability for measuring the state of ancilla 0 prepared in 1.
    - P10 (float): Probability for measuring the state of ancilla 1 prepared in 0.
    - pa (float): Probability parameter for noise(Amplitude damping channel).
    - pd (float): Probability parameter for noise(Dephasing channel).
    """
    # Fetch backend properties to extract T1 and T2 values
    properties = backend.properties()
    backend_data = properties.to_dict()

    # Assign qubit indices for clarity
    Ancilla = qubits[1]
    Battery = qubits[0]

    # If simulator is True, use AerSimulator with backend properties
    if simulator:
        backend = AerSimulator().from_backend(backend)

    # Circuit for calculating P01: Ancilla measurement when Battery is |1>
    q1 = QuantumRegister(1)
    c1 = ClassicalRegister(1)
    qc1 = QuantumCircuit(q1, c1)
    qc1.x(q1)
    qc1.measure(q1, c1)
    qc1 = transpile(qc1, backend, initial_layout=[Ancilla])

    # Circuit for calculating P10: Ancilla measurement when Battery is |0>
    q2 = QuantumRegister(1)
    c2 = ClassicalRegister(1)
    qc2 = QuantumCircuit(q2, c2)
    qc2.measure(q2, c2)
    qc2 = transpile(qc2, backend, initial_layout=[Ancilla])

    # Run both circuits on the backend
    job = backend.run([qc1, qc2], shots=shots)
    result = job.result()
    counts = result.get_counts()

    # Calculate P01 and P10 probabilities
    P10 = counts[0]['0'] / shots  # Probability of ancilla being 1 when battery is |0>
    P01 = counts[1]['1'] / shots  # Probability of ancilla being 0 when battery is |1>

    # Extract T1 and T2 values for the battery qubit
    pa = 1 - exp(-(backend_data['qubits'][Battery][7]['value']*0.001 )/ backend_data['qubits'][Battery][0]['value'])  # T1 relaxation probability
    pd = 1 - exp(-(backend_data['qubits'][Battery][7]['value']*0.001)/ backend_data['qubits'][Battery][1]['value'])     # T2 dephasing probability

    # Print probabilities and decoherence rates for debugging or information
    print(f"P01: {P01}, P10: {P10}, pa: {pa}, pd: {pd}")

    return P01, P10, pa, pd
