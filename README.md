# Product Data Pipeline

## Overview
This project implements a data ingestion and ad generation pipeline using Airflow, pandas, Mlflow, and Hugging Face Transformers.
The pipeline performs the following tasks:
1. Preprocess product data: Clean product names, descriptions, and categories
2. Prepare prompts: Generate ad prompts based on processed data
3. Ad generation: Generate social media ads using GPT-2 model.
4. Track metrics and artifacts: Use mlflow to log data metrics and processed files.
This project is fully containerized using Docker and Docker compose

## Directory Structure
project-root/
├─ dags/                     
│  └─ data_ingestion_dag.py
├─ training/                
│  ├─ preprocess.py
│  ├─ prepare_prompts.py
│  └─ ad_generator.py
├─ data/                     
│  ├─ raw/products.csv
│  └─ processed/
├─ logs/                    
├─ plugins/                  
├─ airflow_db/              
├─ docker-compose.yml
└─ README.md

## Technology Stack
Language: Python
Model: Fine-tuned LLM 
Backend API: FASTAPI
Workflow Orchestration: Apache Airflow
Experiment Tracking: MLFlow
Containerization: Docker
CI/CD: Github Actions
Kubernetes: K8s
Monitoring: Prometheus + Grafana

## Steps to run:
Install local requirements:
pip install -r requirements.txt 

Local development uses lightweight CPU-only dependencies
Training, MlFlow, and Airflow run in containerized environments

### Docker Setup
1. docker-compose up -d
2. http://localhost:8080/
3. Trigger the DAG manually or wait for the daily schedule.
Database has been set for persistence for convenience of airflow.

## Data Ingestion Pipeline 
- Raw product data ingested from CSV/API
- Preprocessing includes text normalization
- Prompt construction for generative model
- Airflow DAG orchestrates ingestion and preprocessing
- Clean data stored in `data/processed/`

## Data Preprocessing
- File: training/preprocess.py
- Reads data/raw/products.csv
- Cleans text
- Writes processed file to data/processed/products_clean.csv
- Logs metrics and artifacts to MlFlow

## Ad Generation
- Uses Hugging Face Transformers with GPT-2
- CPU-only inference
- Generates social-media-ready promotional text
- Includes heuristic content quality scoring

## Model Inference API
- REST API built using FastAPI
- Endpoint: POST /generate-ad
- Returns generated ad text, quality score, and latency
- Swagger UI available at /docs
- Locally available at: http://127.0.0.1:8000/docs

## Sample input for FAST API GUI
{
  "product_name": "Wireless Bluetooth Headphones",
  "category": "Electronics",
  "description": "High-quality noise cancelling headphones with long battery life"
}

## Docker Deployment
```bash
docker build -t ad-generator .
docker run -p 8000:8000 ad-generator
```

## Prometheus Monitoring
- Monitors FastAPI performance
- Outputs metrics at /metric endpoint

## GitHub Actions
Since github actions for Mlops Classroom isn't working, here's the link to the personal repository where Github Actions is working:
https://github.com/S-Amna-Amir/creative-ad-generator

### Note: Due to storage issues, my ubuntu setup crashed a few hours ago, and I have not been able to get it back up again. Sadly, all screenshot and file proofs are unretrievable for the moment.


