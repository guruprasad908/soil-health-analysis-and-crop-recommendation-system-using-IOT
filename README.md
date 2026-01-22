# Soil Health & Intelligent Crop Recommendation System

<p align="center">
  <img src="images/readme_banner.png" alt="Project Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn">
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

---

##  Overview
The **Soil Health & Intelligent Crop Recommendation System** is a cutting-edge Agricultural IoT solution designed to empower farmers with data-driven insights. By combining real-time sensor data with high-precision machine learning models, the system offers personalized crop suggestions, fertilizer strategies, and detailed soil analysis.

###  Key Features
- ** Real-time IoT Monitoring**: Integration with NPK sensors, DHT11, and Capacitive Moisture sensors for live soil auditing.
- ** Stacking Ensemble Intelligence**: High-accuracy predictions using a meta-learner architecture (RF, GB, XGB, SVM).
- ** Professional Reporting**: Automated generation of bilingual (English/Kannada) PDF soil health reports.
- ** Interactive Dashboard**: Modern React-based UI with live gauges, historical trends, and farm visualization.
- ** Smart Weather Integration**: Hyper-local weather forecasting and historical climate analysis.

---

##  System Architecture

### 1. High-Level Data Flow
```mermaid
graph TD
    classDef bwGraph fill:#ffffff,stroke:#000000,stroke-width:2px,stroke-dasharray: 5 5;
    classDef bwNode fill:#ffffff,stroke:#000000,stroke-width:1px;
    
    subgraph Data_Sources
        ESP[ESP8266 + NPK Sensor]:::bwNode
        UNO[Arduino + DH11/Moisture]:::bwNode
        USER[Farmer Manual Input]:::bwNode
    end
    
    subgraph Core_Backend
        API[FastAPI Server]:::bwNode
        DB[(SQLite Database)]:::bwNode
        ML[Ensemble ML Engine]:::bwNode
    end
    
    subgraph Interaction_Layer
        WEB[React Web App]:::bwNode
        PDF[PDF Report Engine]:::bwNode
    end

    ESP & UNO -->|HTTP POST| API
    USER <--> WEB
    API <--> DB
    API -->|Features| ML
    ML -->|Prediction| API
    API -->|Data| WEB
    API --> PDF
    
    class Data_Sources,Core_Backend,Interaction_Layer bwGraph
```

### 2. Backend Architecture (FastAPI Engine)
The backend is built for speed and modularity, managing the bridge between hardware and intelligence.
```mermaid
graph LR
    classDef bwNode fill:#ffffff,stroke:#000000,stroke-width:1px;
    
    REQ[Client Request]:::bwNode --> ROUTE[FastAPI Routers]:::bwNode
    ROUTE --> AUTH[Auth / Validation]:::bwNode
    
    subgraph Services
        S_ML[ML Prediction Service]:::bwNode
        S_W[Weather Service]:::bwNode
        S_P[PDF Generator]:::bwNode
    end
    
    ROUTE --> Services
    Services --> DB[(SQLAlchemy ORM)]:::bwNode
    S_ML --> MODELS[[Stacking Model Store]]:::bwNode
```

### 3. Frontend Architecture (React Ecosystem)
A component-based architecture designed for high responsiveness and accessibility.
```mermaid
graph TD
    classDef bwNode fill:#ffffff,stroke:#000000,stroke-width:1px;

    UI[Root Component]:::bwNode --> CTX[Context API <br/> Theme/Language]:::bwNode
    CTX --> PAGE[Pages <br/> Dashboard/Predictions]:::bwNode
    
    subgraph UI_Components
        WID[Sensor Widgets]:::bwNode
        CHT[Recharts Analytics]:::bwNode
        FRM[Intelligent Forms]:::bwNode
    end
    
    PAGE --> UI_Components
    UI_Components --> API_S[Axios Service Layer]:::bwNode
    API_S --> BACKEND((FastAPI Endpoint)):::bwNode
```

---

##  Technology Stack
| Layer | Technologies |
|---|---|
| **Frontend** | React, Vite, Recharts, Framer Motion, CSS3 |
| **Backend** | FastAPI, Python 3.10, SQLAlchemy, Pydantic |
| **Machine Learning** | Scikit-Learn, XGBoost, CatBoost, Joblib |
| **IoT/Hardware** | Arduino UNO R4, ESP8266, RS485 NPK Sensor, DHT11 |
| **Database** | SQLite |

---

## Quick Start

### 1. Environment Setup
Clone the repository and create a virtual environment:
```bash
git clone https://github.com/guruprasad908/soil-health-analysis-and-crop-recommendation-system-using-IOT.git
cd soil-crop-recommender
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
cd frontend && npm install
```

### 3. Launch the System
**Backend:**
```bash
python start_backend.py
```
**Frontend:**
```bash
npm run dev
```

---

##  License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

##  Academic Project
This system was developed as a **Major Project for Sustainable Agriculture** as part of final year academics (2025 - 2026).

##  Contributing
We are constantly looking for ways to improve this system! Whether it's adding support for more soil types, integrating satellite data, or improving the ML models, your contributions are welcome.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

##  Contact & Socials
Feel free to reach out for collaborations or queries:

[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:guruprasadpujari78@gmail.com)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/guruprasad__pj/#)

---
<p align="center">Developed with ❤️ for Sustainable Agriculture</p>
