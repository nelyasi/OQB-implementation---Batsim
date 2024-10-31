graph TD
    A["BatSim (Battery Simulation)"]

    %% Main sub-packages
    A --> B["Physical"]
    A --> C["BestQubits"]
    A --> D["Calibration"]
    A --> E["Plot"]

    %% Physical sub-package
    B --> B1["Daemonic"]
    B --> B2["Unconditional"]
    B1 --> B1a["Theory"]
    B1 --> B1b["Implement"]
    B2 --> B2a["Theory"]
    B2 --> B2b["Implement"]

    %% BestQubits sub-package
    C --> C1["Select"]
    C1 --> C1a["Q_Physical"]

    %% Calibration sub-package
    D --> D1["Data"]
    D1 --> D1a["Noise_Data"]

    %% Plot sub-package
    E --> E1["Single Mode"]
    E --> E2["Comparison Mode"]
    E --> E3["data_plot"]
    E3 --> E3a["specifications"]
    E3 --> E3b["compare"]
