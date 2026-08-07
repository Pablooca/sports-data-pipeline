# ⚽ Football Event Data Pipeline (Medallion Architecture)

![CI Pipeline](https://img.shields.io/github/actions/workflow/status/Pablooca/sports-data-pipeline/ci.yml?branch=main&label=CI%20Pipeline&logo=github)
![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue?logo=python)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![License](https://img.shields.io/badge/license-MIT-green)

[Español](#español) | [English](#english)

---

## Español

### 📌 Tabla de Contenidos
- [Descripción General](#descripción-general)
- [Arquitectura y Flujo de Datos](#-arquitectura-y-flujo-de-datos)
- [Explicación de Capas e Infraestructura](#-explicación-de-capas-e-infraestructura)
- [Data Quality y Gobernanza](#-data-quality-y-gobernanza)
- [Resultado Final (Capa Gold)](#-resultado-final-capa-gold)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Instalación y Ejecución](#-instalación-y-ejecución)

---

### Descripción General
Pipeline ETL profesional desarrollado en Python para la ingesta, limpieza, modelado y agregación de datos de eventos futbolísticos (StatsBomb Open Data) aplicando la arquitectura Medallion (**Bronze**, **Silver** y **Gold**).

---

### 📐 Arquitectura y Flujo de Datos

```text
┌────────────────┐      ┌─────────────────────────┐      ┌───────────────────────────┐      ┌─────────────────────────────┐
│  StatsBomb API │ ───> │  Bronze Layer (Raw)     │ ───> │  Silver Layer (Clean)     │ ───> │  Gold Layer (Analytics)     │
│  (Event Data)  │      │  Apache Parquet (Raw)   │      │  Decoupled Coordinates    │      │  Player Performance Metrics │
└────────────────┘      └─────────────────────────┘      └───────────────────────────┘      └─────────────────────────────┘
```

---

### 🧱 Explicación de Capas e Infraestructura

1. **Capa Bronze (Ingesta Cruda):** 
   * Ingesta automatizada de partidos y eventos mediante la API de StatsBomb.
   * Persistencia en formato binario **Apache Parquet** para optimizar compresión e I/O.
   * Preservación del esquema original sin modificaciones para auditoría y trazabilidad.

2. **Capa Silver (Limpieza y Modelado):**
   * Normalización de estructuras anidadas y tipado de datos.
   * Descomposición de vectores de localización `[x, y]` en coordenadas individuales para eventos de inicio y fin (pases y tiros).
   * Filtrado y estructuración de atributos analíticos clave (`match_id`, `player`, `type`, `pass_outcome`).

3. **Capa Gold (Agregación de Negocio):**
   * Modelado analítico orientado a *scouting* y análisis táctico.
   * Generación de métricas avanzadas: pases completados, pases al último tercio rival, precisión de pase (%) y *Expected Goals* (xG) acumulados por jugador.
   * Preparación de esquemas optimizados para consumo en herramientas BI (Power BI/Tableau) o modelos de Machine Learning.

4. **DataOps y Calidad de Código:**
   * Pruebas unitarias integradas con **Pytest**.
   * Integración Continua (CI) mediante **GitHub Actions** para formateo (**Black**) y linter (**Flake8**) en cada *Pull Request*.

---

### 🛡️ Data Quality y Gobernanza
* **Validación de Límites del Campo:** Verificación de coordenadas dentro del rango oficial de StatsBomb ($0 \le x \le 120$, $0 \le y \le 80$).
* **Integridad Referencial:** Control estricto de nulos en identificadores clave (`match_id`, `player`, `event_id`).
* **Calidad de Código en CI/CD:** Ejecución automática de linters (`flake8`) y formateadores (`black`) en el flujo de integración de GitHub.

---

### 📊 Resultado Final (Capa Gold)

Ejemplo del dataset analítico generado tras la ejecución del pipeline:

| Team | Player | Total Passes | Successful Passes | Final Third Passes | Total xG | Pass Accuracy (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| FC Barcelona | Lionel Messi | 68 | 59 | 14 | 0.84 | 86.76% |
| FC Barcelona | Frenkie de Jong | 82 | 77 | 9 | 0.05 | 93.90% |
| Real Madrid | Luka Modrić | 71 | 64 | 11 | 0.12 | 90.14% |

---

### 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **Procesamiento de Datos:** Pandas, PyArrow, StatsBombPy
* **Testing & Calidad:** Pytest, Black, Flake8
* **Automatización & CI/CD:** GitHub Actions
* **Formato de Almacenamiento:** Apache Parquet

---

### 🚀 Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/sports-data-pipeline.git](https://github.com/tu-usuario/sports-data-pipeline.git)
   cd sports-data-pipeline
   ```

2. **Crear entorno virtual e instalar dependencias:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -e .
   ```

3. **Ejecutar el pipeline:**
   ```bash
   python main.py
   ```

4. **Ejecutar suite de pruebas:**
   ```bash
   pytest
   ```

---

## English

### 📌 Table of Contents
- [Overview](#overview)
- [Architecture and Data Flow](#-architecture-and-data-flow)
- [Layer & Infrastructure Breakdown](#-layer--infrastructure-breakdown)
- [Data Quality & Governance](#-data-quality--governance)
- [Expected Output (Gold Layer)](#-expected-output-gold-layer)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)

---

### Overview
Professional ETL pipeline built in Python to ingest, clean, transform, and aggregate football event data (StatsBomb Open Data) following the Medallion Architecture (**Bronze**, **Silver**, and **Gold**).

---

### 📐 Architecture and Data Flow

```text
┌────────────────┐      ┌─────────────────────────┐      ┌───────────────────────────┐      ┌─────────────────────────────┐
│  StatsBomb API │ ───> │  Bronze Layer (Raw)     │ ───> │  Silver Layer (Clean)     │ ───> │  Gold Layer (Analytics)     │
│  (Event Data)  │      │  Apache Parquet (Raw)   │      │  Decoupled Coordinates    │      │  Player Performance Metrics │
└────────────────┘      └─────────────────────────┘      └───────────────────────────┘      └─────────────────────────────┘
```

---

### 🧱 Layer & Infrastructure Breakdown

1. **Bronze Layer (Raw Ingestion):**
   * Automated extraction of matches and event logs via StatsBomb API.
   * Storage in binary **Apache Parquet** format to optimize compression and I/O operations.
   * Preserves raw schema integrity for auditability and full data traceability.

2. **Silver Layer (Cleaning & Transformation):**
   * Normalization of nested JSON structures and data type casting.
   * Spatial decomposition of `[x, y]` location vectors into individual coordinates for pass and shot events.
   * Filtering and structuring of key analytical attributes (`match_id`, `player`, `type`, `pass_outcome`).

3. **Gold Layer (Business Aggregation):**
   * Domain-driven modeling tailored for tactical analysis and scouting workflows.
   * Computation of advanced metrics: completed passes, final-third entries, pass accuracy (%), and cumulative Expected Goals (xG) per player.
   * Optimized tables ready for BI tools (Power BI/Tableau) or downstream Machine Learning models.

4. **DataOps & Code Quality:**
   * Unit testing suite implemented with **Pytest**.
   * Continuous Integration (CI) pipeline via **GitHub Actions** running automated linting (**Flake8**) and code formatting (**Black**).

---

### 🛡️ Data Quality & Governance
* **Pitch Coordinate Bounds:** Validation of spatial data within official StatsBomb pitch boundaries ($0 \le x \le 120$, $0 \le y \le 80$).
* **Null Pointer Prevention:** Strict integrity checks on primary keys (`match_id`, `player`, `event_id`).
* **CI/CD Quality Gates:** Automated execution of linters (`flake8`) and code formatters (`black`) on GitHub PR events.

---

### 📊 Expected Output (Gold Layer)

Sample output dataset generated by the pipeline execution:

| Team | Player | Total Passes | Successful Passes | Final Third Passes | Total xG | Pass Accuracy (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| FC Barcelona | Lionel Messi | 68 | 59 | 14 | 0.84 | 86.76% |
| FC Barcelona | Frenkie de Jong | 82 | 77 | 9 | 0.05 | 93.90% |
| Real Madrid | Luka Modrić | 71 | 64 | 11 | 0.12 | 90.14% |

---

### 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Data Processing:** Pandas, PyArrow, StatsBombPy
* **Testing & Quality:** Pytest, Black, Flake8
* **CI/CD & Automation:** GitHub Actions
* **Storage Format:** Apache Parquet

---

### 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/tu-usuario/sports-data-pipeline.git](https://github.com/tu-usuario/sports-data-pipeline.git)
   cd sports-data-pipeline
   ```

2. **Set up virtual environment & dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -e .
   ```

3. **Run the ETL pipeline:**
   ```bash
   python main.py
   ```

4. **Run unit tests:**
   ```bash
   pytest
   ```