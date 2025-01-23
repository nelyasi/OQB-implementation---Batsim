![BatSim Package Overview](BatSim_Package_Overview.png)


# BatSim

## Overview

In this repository, we provide a collection of notebooks designed for easy reproduction of the plots shown in the paper titled ["Experimental simulation of daemonic work extraction in open quantum batteries on a digital quantum computer", arXiv:2410.16567](https://arxiv.org/abs/2410.16567). To streamline the code, all necessary functions have been consolidated into a package called "BatSim" (Battery Simulation), with its components detailed below.


## Package Structure

The BatSim package is composed of four main sub-packages:

### 1. Physical
This sub-package is based on a model that provides the charging of the quantum battery (QB) and correlates it with an ancilla using the unitary gate generated from the Hamiltonian.

### 2. BestQubits
This sub-package is designed for finding the best qubits in terms of low readout error to maximize the power of IBM devices and enhance the results. It includes:
- **Select**: Module with one attributes:
  - **Q_Physical**: Selects the best qubits based on the Physical model.

### 3. Calibration
This sub-package includes:
- **Data**: Module with one attribute:
  - **Noise_Data**: Obtains the parameters needed for engineering our proposed noise model to mimic hardware behavior in theoretical calculations and find the best optimal unitary gates.

### 4. Plot
This sub-package is designed for plotting the results in two modes: noisy and ideal. It includes:
- **data_plot**: Module with two attributes:
  - **specifications**: For single plotting.
  - **compare**: For comparison plotting.

## Installation

To install the BatSim package, clone the repository and install the required dependencies:

```bash
git clone https://github.com/nelyasi/OQB-implementation---Batsim.git
cd BatSim
```
## Notebook Structure

This repository contains several notebooks, each with a specific purpose:

-**RunMe_Main**: This main notebook executes our proposed protocol and model on IBM devices, generating final results and plots based on selected Hamiltonian parameters.

-**RunJobIDs_Offline**: For offline access, we have saved jobs in `.json` format in the "Jobs" folder. This notebook enables result retrieval without an internet connection. 


## RunMe_Main

### Setting Parameters

In your notebook, you can set the parameters for running the code as follows:

```python
Steps = 10
alpha = 1
kappa = 1
shots = 10000
```

### Backend Selection

Choose the backend for running your circuits and find the best qubits:

```python
service = QiskitRuntimeService(channel="ibm_quantum")
backend = service.get_backend('ibm_osaka')
properties = backend.properties()
qubits = Select.Q_Physical(Steps=Steps, omega=omega, kappa=kappa, backend=backend)
qubits = qubits[0]
backend_data = properties.to_dict()
```

### Noise Parameters Calculation

Obtain noise parameters from the Data module:

```python
P01, P10, pa, pd = Data.Noise_Data(backend=backend, shots=shots, qubits=qubits, simulator=True)

# If running on a simulator, uncomment the following line
# backend = AerSimulator().from_backend(backend)
```

### Daemonic and Unconditional Model Execution

Calculate theoretical and implemented results using the Daemonic and Unconditional modules:

```python
Passive_Theory = Daemonic.Theory(Steps=Steps, Charge=Charge, pa=pa, pd=pd, P01=P01, P10=P10)
Passive_Im = Daemonic.Implement(Steps=Steps, Charge=Charge, backend=backend, shots=shots, qubits=qubits)

Energy_Theory, Ergotropy_Theory = Unconditional.Theory(Steps=Steps, Charge=Charge, pa=pa, pd=pd)
Energy_Im, Ergotropy_Im = Unconditional.Implement(Steps=Steps, Charge=Charge, backend=backend, shots=shots, qubits=qubits)

Daemonic_Theory = [xi - yi for xi, yi in zip(Energy_Theory, Passive_Theory)]
Daemonic_Im = [xi - yi for xi, yi in zip(Energy_Im, Passive_Im)]
```

## RunJobIDs_Offline

This notebook loads directly downloaded data from IBM systems for the plots shown in the paper, without requiring an internet connection. Each run generates two plots: one comparing the noisy and ideal models, and another showing the ideal results independently. 

As described in the paper, there are four plots for each Hamiltonian parameter set, with κ values of 1 or 2. To produce the plots, set κ to either 1 or 2 and adjust `figure_num` from 0 to 3 to generate all four plots.

```python
Steps = 10  # Number of steps for the collisional model
alpha = 1  # drving field parameter for the physical Hamiltonian model
kappa = 1 # coupling parameter for the physical Hamiltonian model
shots = 10000  # Number of shots for running the circuit
figure_num = 0 #In the paper, there are four samples for the two modes of paramters \kappa =  1 or 2. To have the first, seocond, third and the fourth plots, you have to put 0, 1, 2 and 3 respectively 
```

## Authors 
Seyed Navid Elyasi, [Matteo A. C. Rossi](https://github.com/matteoacrossi), Marco G. Genoni
