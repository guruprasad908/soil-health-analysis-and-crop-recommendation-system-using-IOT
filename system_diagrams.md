# System Diagrams

This document contains the architectural diagrams for the Soil Crop Recommender System, illustrating the structure, behavior, and hardware connections.

## 1. Class Diagram (Backend Models)

This diagram represents the core data structures used in the FastAPI backend, including database models (SQLAlchemy) and data transfer objects (Pydantic).

```mermaid
classDiagram
    class Base {
        <<SQLAlchemy Declarative Base>>
    }

    class Prediction {
        +int id
        +string farmer_name
        +string phone
        +string location
        +float land_size
        +float nitrogen
        +float phosphorus
        +float potassium
        +float temperature
        +float humidity
        +float ph
        +float rainfall
        +string soil_type
        +string predicted_crop
        +string model_used
        +float confidence
        +datetime timestamp
    }

    class NPKReading {
        +int id
        +int n
        +int p
        +int k
        +string device_id
        +datetime timestamp
    }

    class UNOReading {
        +int id
        +float temperature
        +float humidity
        +int moisture
        +string device_id
        +datetime timestamp
    }

    class PredictionInput {
        <<Pydantic Model>>
        +string farmer_name
        +string phone
        +string location
        +float land_size
        +float N
        +float P
        +float K
        +float temperature
        +float humidity
        +float ph
        +float rainfall
        +string soil_type
        +string model_name
    }

    Base <|-- Prediction
    Base <|-- NPKReading
    Base <|-- UNOReading
    PredictionInput ..> Prediction : Creates
```

## 2. Sequence Diagram (Prediction Flow)

This diagram illustrates the sequence of interactions when a user requests a crop prediction.

```mermaid
sequenceDiagram
    actor User
    participant Frontend as React Dashboard
    participant Backend as FastAPI Server
    participant DB as SQLite Database
    participant ML as Stacking Model

    User->>Frontend: Fills Form / Clicks Predict
    activate Frontend
    
    Note over Frontend: Fetches latest sensor data<br/>if fields are empty
    
    Frontend->>Backend: POST /predict (Input Data)
    activate Backend
    
    Backend->>Backend: Validate Input (Pydantic)
    
    Backend->>ML: predict(features)
    activate ML
    ML-->>Backend: {crop: "Rice", confidence: 0.95}
    deactivate ML
    
    Backend->>DB: Save Prediction Record
    activate DB
    DB-->>Backend: Confirmation
    deactivate DB
    
    Backend-->>Frontend: JSON Response (Result + PDF URL)
    deactivate Backend
    
    Frontend->>User: Display Result & Charts
    deactivate Frontend
```

## 3. Activity Diagram (System Workflow)

This diagram shows the overall workflow of the system, from data collection to final report generation.

```mermaid
stateDiagram-v2
    [*] --> DataCollection
    
    state DataCollection {
        [*] --> ReadSensors
        ReadSensors --> TransmitData : WiFi
        TransmitData --> StoreInDB
        StoreInDB --> [*]
    }

    DataCollection --> UserInteraction
    
    state UserInteraction {
        [*] --> OpenDashboard
        OpenDashboard --> ViewLiveReadings
        ViewLiveReadings --> FillPredictionForm
        FillPredictionForm --> TriggerPrediction
    }

    TriggerPrediction --> Processing
    
    state Processing {
        [*] --> ValidateData
        ValidateData --> RunEnsembleModel
        RunEnsembleModel --> GenerateReport
    }

    Processing --> ResultDisplay
    
    state ResultDisplay {
        [*] --> ShowPrediction
        ShowPrediction --> DownloadPDF
        DownloadPDF --> [*]
    }
    
    ResultDisplay --> [*]
```

## 4. IoT Hardware Block Diagram

This diagram visualizes the physical connections and communication protocols between the hardware components.

```mermaid
graph TD
    subgraph "Field Unit 1 (Soil Nutrients)"
        NPK_Sensor[NPK Sensor] -- "RS485 (Modbus)" --> MAX485[MAX485 Module]
        MAX485 -- "UART (Serial)" --> ESP8266[ESP8266 NodeMCU]
        ESP8266 -- "WiFi (HTTP POST)" --> Router[WiFi Router]
    end

    subgraph "Field Unit 2 (Environmental)"
        DHT[DHT11 Sensor] -- "Digital Pin" --> UNO[Arduino UNO R4 WiFi]
        Moist[Capacitive Moisture] -- "Analog Pin" --> UNO
        UNO -- "WiFi (HTTP POST)" --> Router
    end

    subgraph "Central Server"
        Router -- "Local Network" --> Server[Laptop/Server]
        Server --> Backend[FastAPI Backend]
        Backend --> DB[(SQLite DB)]
        Backend --> Frontend[React Frontend]
    end

    style ESP8266 fill:#f96,stroke:#333,stroke-width:2px
    style UNO fill:#69f,stroke:#333,stroke-width:2px
    style NPK_Sensor fill:#ff9,stroke:#333
    style DHT fill:#ff9,stroke:#333
    style Moist fill:#ff9,stroke:#333
```
