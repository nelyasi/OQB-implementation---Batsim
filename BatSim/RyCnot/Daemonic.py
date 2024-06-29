# Import necessary libraries
import numpy as np
import pandas as pan
from itertools import product
from math import pi, sqrt

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import partial_trace
from qiskit.result import marginal_counts

from qutip import basis, tensor, Qobj, qeye, sigmax, sigmaz, ry, snot
from qutip.qip.operations import cnot
import os

def Theory(Steps, Charge, pa, pd, P01, P10):
    """
    Generate a Noisy Passive Unitary and compute Passive energies.

    Parameters:
    - Steps (int): Number of steps in the computation.
    - Charge (float): Charge parameter for quantum operations.
    - pa (float): Probability parameter for noise model.
    - pd (float): Probability parameter for noise model.
    - P01 (float): Probability parameter for measurement outcomes.
    - P10 (float): Probability parameter for measurement outcomes.

    Returns:
    - Passive (list): List of Passive energies calculated.
    - CSV (file): CSV files defining unitaries for each trajectory in eachs step. 
    """

    # Define initial states and projective measurements
    Battery = basis(2, 0)
    Ancilla = basis(2, 0)
    def initialize():
        Joint_State = tensor(basis(2, 0), basis(2, 0))
        Density = Joint_State*Joint_State.dag()
        return Density 
    
    #Projective Measurements
    #Plus  = Qobj([[1, 2*p-1], [2*p-1, 1]])
    #Minus = Qobj([[1, 1-2*p], [1-2*p, 1]])
    #PP = tensor(qeye(2), Plus)
    #PM = tensor(qeye(2), Minus)
    P00 = 1 - P01
    P11 = 1 - P10
    P0 = P00*basis(2, 0)*basis(2, 0).dag() + P01*basis(2, 1)*basis(2, 1).dag()
    P1 = P11*basis(2, 1)*basis(2, 1).dag() + P10*basis(2, 0)*basis(2, 0).dag()
    PP = tensor(qeye(2), snot()*P0*snot().dag())
    PM = tensor(qeye(2), snot()*P1*snot().dag())
    Noise_Identity = tensor(qeye(2), qeye(2))
    Noise_z = tensor(sigmaz(), qeye(2))
    AP0 = tensor(Qobj([[1, 0], [0, sqrt(1 - pa)]]), qeye(2))
    AP1 = tensor(Qobj([[0, sqrt(pa)], [0, 0]]), qeye(2))

    #Charging Operator
    Ry = tensor(ry(Charge, target=0), qeye(2)) 
    #Define the number of Steps

    def steps_sample_space(steps):
        # Find out the sample space 
        outcomes = list(product([0, 1], repeat=steps))

        #Save the sample space in a list
        sample_space = [list(outcome) for outcome in outcomes]

        #Consider + as 0 and - as 1
        sample_space = [[1 if outcome == 1 else 0 for outcome in step] for step in sample_space]

        #Convert every trajectory from binary to decimal and save it in another list
        decimal_trajectories = [int(''.join(map(str, step)), 2) for step in sample_space]
        
        #Sort both lists together in ascending order
        sorted_lists = sorted(zip(sample_space, decimal_trajectories), key=lambda x: x[1])
        sorted_sample_space, sorted_decimal_trajectories = zip(*sorted_lists)
        for items in sorted_sample_space:
            items.reverse()


        return sorted_sample_space, sorted_decimal_trajectories
    #Finding the Trajectories and save the in the following list 
    Trajectories, decimal = steps_sample_space(Steps) 
    # The following function will be used to find out the unitary matrix for leading us to passive state 

    def find_unitary(Rho):
        #Then I will calculate the eigenstates of the density matrix to diagonalize it.
        E = Rho.eigenstates()
        S1 = E[1][0].full()
        S2 = E[1][1].full()
        Di = Qobj([[S1[0][0], S2[0][0]], [S1[1][0], S2[1][0]]]).dag()
        Diagonal_Density = Di*Rho*Di.dag()
        Test_Matrix = Diagonal_Density.full()
        if Test_Matrix[0][0] > Test_Matrix[1][1]:
            Final_Density = Test_Matrix
            Unitary = Di
        elif Test_Matrix[0][0] <= Test_Matrix[1][1]:
            Final_Density = sigmax()*Diagonal_Density*sigmax()
            Unitary = sigmax()*Di
        return Unitary


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    
    #Staring Loop Process To save density matix for each steps 
    Passive_Energy = 0
    data_list = []
    j = 0
    Passive = []
    H  = 0.5*(qeye(2) - sigmaz())

    for step in range(Steps):
        Passive_Energy = 0
        data_list = []
        j += 1
        num = f'{Charge}-{j}'
        directory = "Unitaries"
        file = f'Output-Mixed-Passive-{num}.csv'
        csv_file_path= os.path.join(directory, file)
        Trajectories, decimal = steps_sample_space(j) 
        for Trajectory in Trajectories:
            Density = initialize()
            E = 0
            for Measure_Type in Trajectory:
                Evolved = cnot()*Ry*Density*Ry.dag()*cnot().dag()   #Charge and interact the Qubit with a specefic \theta in each step
                Evolved = AP0*Evolved*AP0.dag()  +  AP1*Evolved*AP1.dag()
                Evolved = pd*Noise_Identity*Evolved*Noise_Identity.dag()  +  (1-pd)*Noise_z*Evolved*Noise_z.dag()
                if Measure_Type == 0:
                    Meas_Den_P = Evolved*PP
                    Probabilty_P = Meas_Den_P.tr()
                    Meas_Den_P = Meas_Den_P/Probabilty_P
                    P_Den = Meas_Den_P.ptrace(0)
                    Battery = P_Den
                    Density = tensor(Battery, Ancilla*Ancilla.dag())
                if Measure_Type == 1:
                    Meas_Den_M = Evolved*PM
                    Probabilty_M = Meas_Den_M.tr()
                    Meas_Den_M = Meas_Den_M/Probabilty_M
                    M_Den = Meas_Den_M.ptrace(0)
                    Battery = M_Den
                    Density = tensor(Battery, Ancilla*Ancilla.dag())

            Rho = Battery
            Unitary = find_unitary(Rho)
            Matrix = Unitary.full()
            a  = Matrix[0][0]
            b  = Matrix[1][1]
            c  = Matrix[0][1]
            d  = Matrix[1][0]
            G_Den = (Unitary*Battery*Unitary.dag())*H
            E = G_Den.tr()
            #print(Unitary*Battery*Unitary.dag())
            Passive_Energy += E
            data_list.append({'a': a, 'b': b, 'c': c, 'd': d})

        # Convert the list of dictionaries to a DataFrame
        df = pan.DataFrame(data_list)
        # Save the DataFrame to an Excel file
        directory = "Unitaries"
        file = f'Output-Mixed-Passive-{num}.csv'
        csv_file_path= os.path.join(directory, file)
        df.to_csv(csv_file_path, index=False, header=False)
        Passive.append(Passive_Energy/2**j)

    return Passive

def Implement(Steps, Charge, backend, shots, qubits):
    """
    Generate a Noisy Passive Circuit and compute Passive probabilities.

    Parameters:
    - Steps (int): Number of steps in the circuit generation.
    - Charge (float): Charge parameter for QB charge.
    - backend (qiskit.providers.BaseBackend): Backend for running quantum circuits.
    - shots (int): Number of shots (measurements) per quantum circuit execution.
    - qubits (list): List of qubits to use for circuit execution.

    Returns:
    - Passive (list): List of Passive energies calculated for each step.
    """

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
        num = f'{Charge}-{j}'
        directory = "Unitaries"
        file = f'Output-Mixed-Passive-{num}.csv'
        csv_file_path= os.path.join(directory, file)
        #Circuit setup
        q0 = QuantumRegister(1, name = 'battery')
        q1 = QuantumRegister(1, name = 'ancilla')
        creg  = ClassicalRegister(j+1)
        qc = QuantumCircuit(q0, q1, creg)

        #Creat an empty list to save the measurement results 
        result_  = []

        #Start the collisional model for arbitrary number of steps 
        for i in range(j):
            qc.ry(Charge, q0)
            qc.cx(q0, q1)
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


