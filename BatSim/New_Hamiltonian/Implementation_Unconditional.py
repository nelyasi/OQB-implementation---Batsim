from math import *
from numpy import *
from pandas import *
from qiskit import *
from qutip import *
import qiskit.quantum_info
import qiskit.result
from qiskit.circuit import SwitchCaseOp
from qiskit.circuit.library import UnitaryGate
from qiskit.visualization import *
from qiskit.result import marginal_counts
import pandas as pd


def Energy_Ergotropy(Steps, omega, kappa, backend, shots, qubits):
    Ergo_Circuits = []
    Energy_Circuits = []

    label = f'{omega}@{kappa}'
    def get_values_from_csv(file_path, row_number):
        try:
            # Read the csv file into a DataFrame, specifying that the first column may contain complex numbers
            df = pd.read_csv(file_path, header=None)

            # Check if the specified row_number is valid
            if 0 <= row_number < df.shape[0]:
                # Get the values of the specified row
                row_values = df.iloc[row_number, :].tolist()
                return row_values
            else:
                print("Invalid row number. Please enter a valid row number.")
                return None

        except FileNotFoundError:
            print(f"File not found at the path: {file_path}")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
    #Adressing directory of the csv file
    csv_file_path = f'output{label}.csv'
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    Energy = []
    Passive = []
    #Circuit setup
    H = omega * (tensor(sigmax(), qeye(2))) + kappa * (
    tensor(sigmam(), sigmap()) + tensor(sigmap(), sigmam()))
    # Generating the Unitary gate which is responsible for charging the battey and correlating it with the ancilla 
    M_Unitary = (-1j * H).expm()
    M_gate = UnitaryGate(M_Unitary)

    q0 = QuantumRegister(1, name = 'battery')
    q1 = QuantumRegister(1, name = 'ancilla')
    creg  = ClassicalRegister(1)
    qc = QuantumCircuit(q0, q1, creg)
    #Creat an empty list to save the measurement results 
    result_  = []
    j = 0
    #Start the collisional model for arbitrary number of steps 
    for step in range(0, Steps):
        j = j + 1
        q0 = QuantumRegister(1, name = 'battery')
        q1 = QuantumRegister(1, name = 'ancilla')
        creg  = ClassicalRegister(1)
        qc = QuantumCircuit(q0, q1, creg)
        for i in range(j):
            qc.append(M_gate, [q1, q0])
            qc.barrier()
            qc.reset(q1)
            qc.barrier()
        qc.measure(q0, creg[0])
        qc = transpile(qc, backend = backend, initial_layout = qubits)
        Energy_Circuits.append(qc)
    job = backend.run(Energy_Circuits, shots = shots)
    results = job.result()
    counts = results.get_counts()
    for i in range(Steps):
        E  = 1 - counts[i]['0']/shots 
        Energy.append(E)
    #print(E)

    #Circuit setup
    q0 = QuantumRegister(1, name = 'battery')
    q1 = QuantumRegister(1, name = 'ancilla')
    creg  = ClassicalRegister(1)
    qc = QuantumCircuit(q0, q1, creg)

    result_  = []
    j = 0
    #Start the collisional model for arbitrary number of steps 
    for step in range(0, Steps):
        j = j + 1
        q0 = QuantumRegister(1, name = 'battery')
        q1 = QuantumRegister(1, name = 'ancilla')
        creg  = ClassicalRegister(1)
        qc = QuantumCircuit(q0, q1, creg)
        for i in range(j):
            qc.append(M_gate, [q1, q0])
            qc.barrier()
            qc.reset(q1)
            qc.barrier()
        Values = get_values_from_csv(csv_file_path, step)
        Unit = Values[0]
        if Unit == 1:
            qc.x(q0)
        qc.measure(q0, creg[0])
        qc = transpile(qc, backend = backend, initial_layout= qubits)
        Ergo_Circuits.append(qc)
    job = backend.run(Ergo_Circuits, shots = shots)
    results = job.result()
    counts = results.get_counts()
    for i in range(0, Steps):
        E = counts[i]['1']/shots
        Passive.append(E)
    Ergo = []

    for k in range(len(Energy)):
        Ergotropy = Energy[k] - Passive[k]
        if Ergotropy < 0:
            Ergotropy = 0
        Ergo.append(Ergotropy)
        #print(Ergotropy)

    return Energy, Ergo
    
