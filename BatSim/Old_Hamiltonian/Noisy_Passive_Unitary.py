from qutip import basis, tensor, Qobj, qeye, sigmax, sigmaz, snot
from qutip.qip.operations import cnot, ry
from math import pi, sqrt
import numpy as np
import pandas as pan
from itertools import product

def  Noisy_Passive_Unitary(Steps, Charge, pa, pd, P01, P10):
    num = f'{Charge/np.pi}.{Steps}'

    #Defining The State of the Battery 
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


    H = 0.5*(qeye(2) - sigmaz())
    for Trajectory in Trajectories:
        Density = initialize()
        E = 0
        for Measure_Type in Trajectory:
            Evolved = cnot()*Ry*Density*Ry.dag()*cnot().dag()   #Charge and interact the Qubit with a specefic \theta in each step
            Evolved = pd*Noise_Identity*Evolved*Noise_Identity.dag()  +  (1-pd)*Noise_z*Evolved*Noise_z.dag()
            Evolved = AP0*Evolved*AP0.dag()  +  AP1*Evolved*AP1.dag()
            if Measure_Type == 0:
                Meas_Den_P = Evolved*PP.dag()
                Probabilty_P = Meas_Den_P.tr()
                Meas_Den_P = Meas_Den_P/Probabilty_P
                P_Den = Meas_Den_P.ptrace(0)
                Battery = P_Den
                Density = tensor(Battery, Ancilla*Ancilla.dag())
            if Measure_Type == 1:
                Meas_Den_M = Evolved*PM.dag()
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
    csv_file_path = f'Output-Mixed-Passive-{num}.csv'
    df.to_csv(csv_file_path, index=False, header=False)

    return Passive_Energy/2**Steps
                
