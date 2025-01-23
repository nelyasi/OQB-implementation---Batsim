# Import necessary libraries
from qiskit.result import marginal_counts

def RetrieveDaemonic(Jobid, Service, Steps, shots):
    """
    Retrieve and calculate passive energy values from a quantum job result.

    Parameters:
    Jobid (str): The ID of the quantum job to retrieve.
    Service (object): The quantum service object to use for retrieving the job.
    Steps (int): The number of steps (or qubits) to process.
    shots (int): The total number of shots (repetitions of the experiment) used to obtain the measurement results.

    Returns:
    list: A list of passive energy values calculated from the job results.
    """

    # Retrieve the job using the given Jobid and Service
    job = Service.job(Jobid)
    # Get the results of the job
    results = job.result()
    # Get the counts (measurement results) from the job results
    counts = results.get_counts()
    # Initialize an empty list to store passive energy values
    Passive = []

    # Iterate over a range from 1 to Steps + 1
    for m in range(1, Steps + 1):
        # Get the marginal counts for the m-th measurement, focusing on the m-th qubit
        midcirc_count = marginal_counts(results.get_counts()[m - 1], indices=[m])
        # Calculate the passive energy for the m-th qubit
        Passive_E = 1 - midcirc_count['0'] / shots
        # Append the calculated passive energy to the Passive list
        Passive.append(Passive_E)    

    # Return the list of passive energy values
    return Passive


def RetrieveUnconditional(Jobid1, Jobid2, Service, Steps, shots):
    """
    Retrieve and calculate energy, passive energy, and ergotropy values from two quantum job results.

    Parameters:
    Jobid1 (str): The ID of the first quantum job to retrieve (for energy values).
    Jobid2 (str): The ID of the second quantum job to retrieve (for passive energy values).
    Service (object): The quantum service object to use for retrieving the jobs.
    Steps (int): The number of steps (or qubits) to process.
    shots (int): The total number of shots (repetitions of the experiment) used to obtain the measurement results.

    Returns:
    tuple: A tuple containing two lists:
        - Energy (list): A list of energy values calculated from the first job results.
        - Ergo (list): A list of ergotropy values calculated from the energy and passive energy values.
    """

    # Initialize lists to store energy, passive energy, and ergotropy values
    Energy = []
    Passive = []
    Ergo = []

    # Retrieve the job using the given Jobid1 and Service
    job = Service.job(Jobid1)
    results = job.result()
    counts = results.get_counts()
    # Calculate energy values for each step
    for i in range(Steps):
        E = 1 - counts[i]['0'] / shots
        Energy.append(E)
    # print(E)  # Uncomment for debugging purposes

    # Retrieve the job using the given Jobid2 and Service
    job = Service.job(Jobid2)
    results = job.result()
    counts = results.get_counts()
    # Calculate passive energy values for each step
    for i in range(Steps):
        E = counts[i]['1'] / shots
        Passive.append(E)

    # Calculate ergotropy values
    for k in range(len(Energy)):
        Ergotropy = Energy[k] - Passive[k]
        if Ergotropy < 0:
            Ergotropy = 0
        Ergo.append(Ergotropy)
        # print(Ergotropy)  # Uncomment for debugging purposes

    # Return the energy and ergotropy values
    return Energy, Ergo



def RetrieveDaemonic_offline(Jobid, mode,  Steps, shots):
    """
    Retrieve and calculate passive energy values from a quantum job result.

    Parameters:
    Jobid (str): The ID of the quantum job to retrieve.
    Service (object): The quantum service object to use for retrieving the job.
    Steps (int): The number of steps (or qubits) to process.
    shots (int): The total number of shots (repetitions of the experiment) used to obtain the measurement results.

    Returns:
    list: A list of passive energy values calculated from the job results.
    """

    # Retrieve the job using the given Jobid1
    from qiskit_ibm_runtime import RuntimeDecoder
    import json
    with open(f"Jobs/{mode}/{Jobid}.json", "r") as file:
        results = json.load(file, cls=RuntimeDecoder)
    # Get the counts (measurement results) from the job results
    counts = results.get_counts()
    # Initialize an empty list to store passive energy values
    Passive = []

    # Iterate over a range from 1 to Steps + 1
    for m in range(1, Steps + 1):
        # Get the marginal counts for the m-th measurement, focusing on the m-th qubit
        midcirc_count = marginal_counts(results.get_counts()[m - 1], indices=[m])
        # Calculate the passive energy for the m-th qubit
        Passive_E = 1 - midcirc_count['0'] / shots
        # Append the calculated passive energy to the Passive list
        Passive.append(Passive_E)    

    # Return the list of passive energy values
    return Passive


def RetrieveUnconditional_offline(Jobid1, Jobid2, mode, Steps, shots):
    """
    Retrieve and calculate energy, passive energy, and ergotropy values from two quantum job results.

    Parameters:
    Jobid1 (str): The ID of the first quantum job to retrieve (for energy values).
    Jobid2 (str): The ID of the second quantum job to retrieve (for passive energy values).
    Service (object): The quantum service object to use for retrieving the jobs.
    Steps (int): The number of steps (or qubits) to process.
    shots (int): The total number of shots (repetitions of the experiment) used to obtain the measurement results.

    Returns:
    tuple: A tuple containing two lists:
        - Energy (list): A list of energy values calculated from the first job results.
        - Ergo (list): A list of ergotropy values calculated from the energy and passive energy values.
    """

    # Initialize lists to store energy, passive energy, and ergotropy values
    Energy = []
    Passive = []
    Ergo = []

    # Retrieve the job using the given Jobid1
    from qiskit_ibm_runtime import RuntimeDecoder
    import json
    with open(f"Jobs/{mode}/{Jobid1}.json", "r") as file:
        results = json.load(file, cls=RuntimeDecoder)
    counts = results.get_counts()
    # Calculate energy values for each step
    for i in range(Steps):
        E = 1 - counts[i]['0'] / shots
        Energy.append(E)
    # print(E)  # Uncomment for debugging purposes

    # Retrieve the job using the given Jobid2 and Service
    # Retrieve the job using the given Jobid1
    from qiskit_ibm_runtime import RuntimeDecoder
    import json
    with open(f"Jobs/{mode}/{Jobid2}.json", "r") as file:
        results = json.load(file, cls=RuntimeDecoder)
    counts = results.get_counts()
    # Calculate passive energy values for each step
    for i in range(Steps):
        E = counts[i]['1'] / shots
        Passive.append(E)

    # Calculate ergotropy values
    for k in range(len(Energy)):
        Ergotropy = Energy[k] - Passive[k]
        if Ergotropy < 0:
            Ergotropy = 0
        Ergo.append(Ergotropy)
        # print(Ergotropy)  # Uncomment for debugging purposes

    # Return the energy and ergotropy values
    return Energy, Ergo

