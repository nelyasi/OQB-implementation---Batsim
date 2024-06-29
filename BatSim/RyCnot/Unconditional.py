# Import necessary libraries
import numpy as np
from itertools import product
from math import pi, sqrt
from qutip import *
from qutip.qip.operations import *
from math import *
import pandas as pan
from numpy import *
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate
from qiskit.result import marginal_counts
import os

def Theory(Steps, Charge, pa, pd):
    """
    Generate a set of mutilple CSV files for generating optimal unitary gate and compute Passive energies in theoretical case 
    for each step.

    Parameters:
    Steps (int): Number of steps in the computation.
    Charge (float): Charge parameter for QB charge.
    pa (float): Probability parameter for noise(Amplitude dampin channel).
    pd (float): Probability parameter for noise(Dephasing channel).
    P01 (float): Probability for measuring the state of ancilla 0 prepared in 1.
    P10 (float): Probability for measuring the state of ancilla 1 prepared in 0.

    Returns:
    - Passive (list): List of Passive energies calculated.
    - CSV (file): Optimal unitary elements for each step. 
    """

    # Define initial states and projective measurements
    label = f'{Steps}@{Charge/pi}'
    #Defining The State of the Battery 
    Battery = basis(2, 0)
    Ancilla = basis(2, 0)
    def initialize():
        Joint_State = tensor(basis(2, 0), basis(2, 0))
        Density = Joint_State*Joint_State.dag()
        return Density 
        

    #Charging Operator
    Ry = tensor(ry(Charge, target=0), qeye(2)) 
    Noise_Identity = tensor(qeye(2), qeye(2))
    Noise_z = tensor(sigmaz(), qeye(2))
    AP0 = tensor(Qobj([[1, 0], [0, sqrt(1 - pa)]]), qeye(2))
    AP1 = tensor(Qobj([[0, sqrt(pa)], [0, 0]]), qeye(2))



    # Initialize an empty list to store the data
    E = []
    Unconditional_Ergotropy = []
    H  = 0.5*(qeye(2) - sigmaz())
    Density = initialize()
    data_list = []
    for step in range(0, Steps):
        Evolved = cnot()*Ry*Density*Ry.dag()*cnot().dag()   #Charge and interact the Qubit with a specefic \theta in each step
        Evolved = pd*Noise_Identity*Evolved*Noise_Identity.dag()  +  (1-pd)*Noise_z*Evolved*Noise_z.dag()
        Evolved = AP0*Evolved*AP0.dag()  +  AP1*Evolved*AP1.dag()
        Battery = Evolved.ptrace(0)
        Density = tensor(Battery, Ancilla*Ancilla.dag())
        #print(Battery)
        Energy = trace(Battery*H)
        E.append(Energy)
        if real(Battery[0, 0]) >= real(Battery[1, 1]):
            Unitary = 0
            Unconditional_Ergotropy.append(0)
        elif real(Battery[0, 0]) < real(Battery[1, 1]):
            Unitary = 1 
            final = sigmax()*Battery*sigmax().dag()
            Passive_Energy = trace(final*H)
            Ergotropy = Energy - Passive_Energy 
            Unconditional_Ergotropy.append(Ergotropy)
        data_list.append({'Theta': Unitary})
    # Convert the list of dictionaries to a DataFrame
    df = pan.DataFrame(data_list)

    # Save the DataFrame to an Excel file
    directory = "Unitaries"
    file = f'output{label}.xlsx' #Saving path of the Output Data 
    csv_file_path= os.path.join(directory, file)
    df.to_csv(csv_file_path, index=False, header=False)
    return E, Unconditional_Ergotropy



def Implement(Steps, Charge, backend, shots, qubits):
    """
    Calculate Energy and Ergotropy for a given number of Steps and Charge using Quantum circuits.

    Parameters:
    - Steps (int): Number of steps in the process.
    - Charge (float): Charge parameter for QB charge.
    - backend (qiskit.providers.BaseBackend): Backend for running quantum circuits.
    - shots (int): Number of shots (measurements) per quantum circuit execution.
    - qubits (list): List of qubits to use for circuit execution.

    Returns:
    - Energy (list): List of Energy values calculated.
    - Ergo (list): List of Ergotropy values calculated.
    """

    # Prepare lists to store Quantum circuits
    Ergo_Circuits = []
    Energy_Circuits = []

    label = f'{Steps}@{Charge/pi}'
    def get_values_from_csv(file_path, row_number):
        try:
            # Read the csv file into a DataFrame, specifying that the first column may contain complex numbers
            df = pan.read_csv(file_path, header=None)

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
    directory = "Unitaries"
    file = f'output{label}.xlsx' #Saving path of the Output Data 
    csv_file_path= os.path.join(directory, file)
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    Energy = []
    Passive = []
    #Circuit setup


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
            qc.ry(Charge, q0)
            qc.cx(q0, q1)
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
            qc.ry(Charge, q0)
            qc.cx(q0, q1)
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