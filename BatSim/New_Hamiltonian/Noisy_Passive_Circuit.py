import pandas as pd
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.quantum_info import partial_trace
from qiskit.circuit import SwitchCaseOp
from qiskit.circuit.library import UnitaryGate
from qiskit.result import marginal_counts
from math import *
from numpy import *
from pandas import *
from qiskit import *
from qutip import *
import qiskit.quantum_info
import qiskit.visualization
import qiskit.result

def Noisy_Passive_Circuit(Steps, omega, kappa, p, backend, shots, qubits):
    num = f'{omega}.{kappa}'

    H = omega * (tensor(sigmax(), qeye(2))) + kappa * (
    tensor(sigmam(), sigmap()) + tensor(sigmap(), sigmam()))
    # Generating the Unitary gate which is responsible for charging the battey and correlating it with the ancilla 
    M_Unitary = (-1j * H).expm()
    M_gate = UnitaryGate(M_Unitary)

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

    

    import pandas as pd
    circuits = []
    j = 0


    for step in range(Steps):
        Passive_Energy = 0
        data_list = []
        j += 1
        num = f'{omega}-{kappa}-{j}'
        csv_file_path = f'Output-Mixed-Passive-{num}.csv'
        #Circuit setup
        q0 = QuantumRegister(1, name = 'battery')
        q1 = QuantumRegister(1, name = 'ancilla')
        creg  = ClassicalRegister(j+1)
        qc = QuantumCircuit(q0, q1, creg)

        #Creat an empty list to save the measurement results 
        result_  = []

        #Start the collisional model for arbitrary number of steps 
        for i in range(j):
            qc.append(M_gate, [q1, q0])
            qc.h(q1)
            qc.measure(q1, creg[i])
            qc.barrier()
            with qc.if_test((creg[i], 1)):
                qc.x(q1)
            #qc.x(q1)
            #qc.barrier()
        with qc.switch(creg) as case: 
            for i in range(2**j):
                with case(i):
                    #Calling the Excel file created in the prevous code and search for the decimal code to find the corresponding Theta and Phi
                    Values = get_values_from_csv(csv_file_path, i)
                    a =  Values[0]
                    b =  Values[1]
                    c =  Values[2]
                    d =  Values[3]
                    #Theta = float(real(Theta))
                    #Phi = float(real(Phi))
                    #Creating the Unitary matrix using the obtained Theta and Phi
                    matrix = [[a, c], [d, b]]
                    #Converting it into a gate 
                    Unitary = UnitaryGate(matrix, label=r'$U_{Con}$')

                    #Applying the gate to the battery qubit 
                    qc.append(Unitary,q0)

        qc.measure(q0, creg[j])
        qc = transpile(qc, backend=backend, initial_layout= qubits)
        circuits.append(qc)
    job = backend.run(circuits, shots = shots)
    results = job.result()
    counts = results.get_counts()
    Passive = []
    for m in range(1, j + 1):
        midcirc_count = marginal_counts(results.get_counts()[m-1], indices=[m])
        Passive_E = 1- midcirc_count['0']/shots
        Passive.append(Passive_E)    


    return Passive

