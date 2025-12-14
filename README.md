[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/EsmaCwYg)

## Technology Stack
Language: Python
Model: Fine-tuned LLM 
Backend API: FASTAPI
Workflow Orchestration: Apache Airflow
Experiment Tracking: MLFlow
Containerization: Docker
CI/CD: Github Actions
Cloud Platform: 
Kubernetes: Managed K8s
Monitoring: Prometheus + Grafana
Artifact Storage: 

## Steps to run:
Install local requirements:
pip install -r requirements.txt 

Local development uses lightweight CPU-only dependencies
Training, MlFlow, and Airflow run in containerized environments

## Data Ingestion Pipeline

- Raw product data ingested from CSV/API
- Preprocessing includes text normalization
- Prompt construction for generative model
- Airflow DAG orchestrates ingestion and preprocessing
- Clean data stored in `data/processed/`

## Ad Generation

- Uses a lightweight pretrained LLM (Flan-T5 Small)
- CPU-only inference
- Generates social-media-ready promotional text
- Includes heuristic content quality scoring

## Model Inference API

- REST API built using FastAPI
- Endpoint: POST /generate-ad
- Returns generated ad text, quality score, and latency
- Swagger UI available at /docs
