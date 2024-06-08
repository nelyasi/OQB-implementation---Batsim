from qutip import *
from qutip.qip.operations import *
from math import *
import pandas as pan
from numpy import *

def Energy_Ergotropy(Steps, Charge, pa, pd):
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

    excel_file_path = f'output{label}.xlsx' #Saving path of the Output Data 

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
    csv_file_path = f'output{label}.csv'
    df.to_csv(csv_file_path, index=False, header=False)
    return E, Unconditional_Ergotropy
