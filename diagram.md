```mermaid
graph TD
    A[BatSim Package] --> B1[Physical]
    A --> B2[RyCnot]
    A --> B3[BestQubits]
    A --> B4[Calibration]
    A --> B5[Plot]

    B1 --> C1[Daemonic]
    B1 --> C2[Unconditional]

    B2 --> C3[Daemonic]
    B2 --> C4[Unconditional]

    C1 --> D1[Theory]
    C1 --> D2[Implement]

    C2 --> D3[Theory]
    C2 --> D4[Implement]

    C3 --> D5[Theory]
    C3 --> D6[Implement]

    C4 --> D7[Theory]
    C4 --> D8[Implement]

    B3 --> E1[Select]
    E1 --> F1[Q_RyCnot]
    E1 --> F2[Q_Physical]

    B4 --> E2[Data]
    E2 --> F3[Noise_Data]

    B5 --> E3[data_plot]
    E3 --> F4[specifications]
    E3 --> F5[compare]
