# Import necessary libraries
from qutip import basis, tensor, Qobj, qeye, sigmax, sigmaz, sigmap, sigmam, snot
import pandas as pan
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.quantum_info import partial_trace
from qiskit.circuit.library import UnitaryGate
from qiskit.result import marginal_counts
from math import pi, sqrt
import numpy as np
from itertools import product
import os


def Theory(Steps, omega, kappa, pa, pd, P01, P10):
    """
    Generate and run quantum circuits for a noisy passive unitary evolution.

    Parameters:
    Steps (int): Number of steps in the collisional model.
    omega (float): Parameter for Hamiltonian(Frequency of the driving field).
    kappa (float): Parameter for Hamiltonian(The coupling strength between QB and the ancilla).
    pa (float): Probability parameter for noise(Amplitude dampin channel).
    pd (float): Probability parameter for noise(Dephasing channel).
    P01 (float): Probability for measuring the state of ancilla 0 prepared in 1.
    P10 (float): Probability for measuring the state of ancilla 1 prepared in 0.

    Returns:
    list: List of passive energy values.
    CSV files: For optimal unitary for each step
    """
    
    # Define the initial state of the battery
    Battery = basis(2, 0)
    Ancilla = basis(2, 0)

    def initialize():
        """
        Initialize the joint state and density matrix.

        Returns:
        Qobj: Density matrix of the initialized state.
        """
        Joint_State = tensor(basis(2, 0), basis(2, 0))
        Density = Joint_State * Joint_State.dag()
        return Density

    # Define projective measurements
    P00 = 1 - P10
    P11 = 1 - P01
    P0 = P00 * basis(2, 0) * basis(2, 0).dag() + P01 * basis(2, 1) * basis(2, 1).dag()
    P1 = P11 * basis(2, 1) * basis(2, 1).dag() + P10 * basis(2, 0) * basis(2, 0).dag()
    PP = tensor(qeye(2), snot() * P0 * snot().dag())
    PM = tensor(qeye(2), snot() * P1 * snot().dag())
    
    # Define noise operators
    Noise_Identity = tensor(qeye(2), qeye(2))
    Noise_z = tensor(sigmaz(), qeye(2))
    AP0 = tensor(Qobj([[1, 0], [0, sqrt(1 - pa)]]), qeye(2))
    AP1 = tensor(Qobj([[0, sqrt(pa)], [0, 0]]), qeye(2))

    # Define the Hamiltonian and the unitary gate for charging
    H = omega * (tensor(sigmax(), qeye(2))) + kappa * (tensor(sigmam(), sigmap()) + tensor(sigmap(), sigmam()))
    M_Unitary = (-1j * H).expm()

    def steps_sample_space(steps):
        """
        Generate the sample space for the given number of steps.

        Parameters:
        steps (int): Number of steps.

        Returns:
        tuple: Sorted sample space and corresponding decimal trajectories.
        """
        outcomes = list(product([0, 1], repeat=steps))
        sample_space = [list(outcome) for outcome in outcomes]
        sample_space = [[1 if outcome == 1 else 0 for outcome in step] for step in sample_space]
        decimal_trajectories = [int(''.join(map(str, step)), 2) for step in sample_space]
        sorted_lists = sorted(zip(sample_space, decimal_trajectories), key=lambda x: x[1])
        sorted_sample_space, sorted_decimal_trajectories = zip(*sorted_lists)
        
        for items in sorted_sample_space:
            items.reverse()

        return sorted_sample_space, sorted_decimal_trajectories

    def find_unitary(Rho):
        """
        Find the unitary matrix to diagonalize the density matrix.

        Parameters:
        Rho (Qobj): Density matrix to be diagonalized.

        Returns:
        Qobj: Unitary matrix.
        """
        E = Rho.eigenstates()
        S1 = E[1][0].full()
        S2 = E[1][1].full()
        Di = Qobj([[S1[0][0], S2[0][0]], [S1[1][0], S2[1][0]]]).dag()
        Diagonal_Density = Di * Rho * Di.dag()
        Test_Matrix = Diagonal_Density.full()

        if Test_Matrix[0][0] > Test_Matrix[1][1]:
            Unitary = Di
        else:
            Unitary = sigmax() * Di

        return Unitary

    # Start the loop to save density matrix for each step
    Passive = []
    H = 0.5 * (qeye(2) - sigmaz())
    j = 0

    for step in range(Steps):
        Passive_Energy = 0
        data_list = []
        j += 1
        num = f'{omega}-{kappa}-{j}'
        Trajectories, decimal = steps_sample_space(j)

        for Trajectory in Trajectories:
            Density = initialize()
            E = 0

            for Measure_Type in Trajectory:
                Evolved = M_Unitary * Density * M_Unitary.dag()  # Charge and interact the qubit with a specific theta in each step
                Evolved = pd * Noise_Identity * Evolved * Noise_Identity.dag() + (1 - pd) * Noise_z * Evolved * Noise_z.dag()
                Evolved = AP0 * Evolved * AP0.dag() + AP1 * Evolved * AP1.dag()

                if Measure_Type == 0:
                    Meas_Den_P = Evolved * PP
                    Probability_P = Meas_Den_P.tr()
                    Meas_Den_P = Meas_Den_P / Probability_P
                    P_Den = Meas_Den_P.ptrace(0)
                    Battery = P_Den
                    Density = tensor(Battery, Ancilla * Ancilla.dag())
                else:
                    Meas_Den_M = Evolved * PM
                    Probability_M = Meas_Den_M.tr()
                    Meas_Den_M = Meas_Den_M / Probability_M
                    M_Den = Meas_Den_M.ptrace(0)
                    Battery = M_Den
                    Density = tensor(Battery, Ancilla * Ancilla.dag())

            Rho = Battery
            Unitary = find_unitary(Rho)
            Matrix = Unitary.full()
            a = Matrix[0][0]
            b = Matrix[1][1]
            c = Matrix[0][1]
            d = Matrix[1][0]
            G_Den = (Unitary * Battery * Unitary.dag()) * H
            E = G_Den.tr()
            Passive_Energy += E
            data_list.append({'a': a, 'b': b, 'c': c, 'd': d})

        # Convert the list of dictionaries to a DataFrame and save it to a CSV file
        df = pan.DataFrame(data_list)
        directory = "Unitaries"
        file = f'Output-Mixed-Passive-{num}.csv'
        csv_file_path= os.path.join(directory, file)

        df.to_csv(csv_file_path, index=False, header=False)
        Passive.append(Passive_Energy / 2**j)

    return Passive



def Implement(Steps, omega, kappa, backend, shots, qubits):
    """
    Generate and run quantum circuits for a noisy passive energy calculation.

    Parameters:
    Steps (int): Number of steps in the collisional model.
    omega (float): Parameter for Hamiltonian(Frequency of the driving field).
    kappa (float): Parameter for Hamiltonian(The coupling stregnth between QB and the ancilla).
    backend (Backend): IBM backend to run the circuits.
    shots (int): Number of shots for the quantum circuit execution.
    qubits (list): Initial layout for the quantum circuits(Target qubits which are selected via Mapomatic).

    Returns:
    list: List of passive energy values.
    """
    
    num = f'{omega}.{kappa}'

    # Define the Hamiltonian
    H = omega * (tensor(sigmax(), qeye(2))) + kappa * (tensor(sigmam(), sigmap()) + tensor(sigmap(), sigmam()))
    
    # Generate the Unitary gate for the system
    M_Unitary = (-1j * H).expm()
    M_gate = UnitaryGate(M_Unitary)

    def get_values_from_csv(file_path, row_number):
        """
        Retrieve values from a specific row in a CSV file.

        Parameters:
        file_path (str): Path to the CSV file.
        row_number (int): Row number to retrieve values from.

        Returns:
        list: List of values from the specified row.
        """
        try:
            # Read the CSV file into a DataFrame
            df = pan.read_csv(file_path, header=None)

            # Check if the row number is valid
            if 0 <= row_number < df.shape[0]:
                return df.iloc[row_number, :].tolist()
            else:
                print("Invalid row number. Please enter a valid row number.")
                return None
        except FileNotFoundError:
            print(f"File not found at the path: {file_path}")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    circuits = []
    j = 0

    # Loop over the number of steps
    for step in range(Steps):
        Passive_Energy = 0
        data_list = []
        j += 1
        num = f'{omega}-{kappa}-{j}'
        directory = "Unitaries"
        file = f'Output-Mixed-Passive-{num}.csv'
        csv_file_path= os.path.join(directory, file)

        # Circuit setup
        q0 = QuantumRegister(1, name='battery')
        q1 = QuantumRegister(1, name='ancilla')
        creg = ClassicalRegister(j + 1)
        qc = QuantumCircuit(q0, q1, creg)

        # Create an empty list to save the measurement results
        result_ = []

        # Start the collisional model for an arbitrary number of steps
        for i in range(j):
            qc.append(M_gate, [q1, q0])
            qc.h(q1)
            qc.measure(q1, creg[i])
            qc.barrier()
            with qc.if_test((creg[i], 1)):
                qc.x(q1)
        
        with qc.switch(creg) as case: 
            for i in range(2**j):
                with case(i):
                    # Retrieve the values from the CSV file
                    Values = get_values_from_csv(csv_file_path, i)
                    a = Values[0]
                    b = Values[1]
                    c = Values[2]
                    d = Values[3]
                    
                    # Create the unitary matrix using the obtained values
                    matrix = [[a, c], [d, b]]
                    
                    # Convert it into a gate
                    Unitary = UnitaryGate(matrix, label=r'$U_{Con}$')

                    # Apply the gate to the battery qubit
                    qc.append(Unitary, q0)

        qc.measure(q0, creg[j])
        qc = transpile(qc, backend=backend, initial_layout=qubits)
        circuits.append(qc)

    # Run the circuits on the backend
    job = backend.run(circuits, shots=shots)
    results = job.result()
    counts = results.get_counts()
    Passive = []

    # Calculate passive energy values
    for m in range(1, j + 1):
        midcirc_count = marginal_counts(results.get_counts()[m - 1], indices=[m])
        Passive_E = 1 - midcirc_count['0'] / shots
        Passive.append(Passive_E)    

    return Passive

