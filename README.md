# End-to-End MLOps Pipeline on GCP for Credit Card Fraud Detection

This project implements a cloud-native, event-driven MLOps pipeline on Google Cloud Platform for automated credit card fraud detection.

## Project Overview

The system automatically retrains an XGBoost fraud detection model whenever new transaction data is uploaded to Google Cloud Storage. The trained model is stored in GCS as a lightweight model registry and served through a FastAPI inference API deployed on Cloud Run.

## Architecture

GCS Data Upload → Pub/Sub Event → Cloud Run Trigger Service → Cloud Run Training Job → GCS Model Registry → Cloud Run Inference API

## Technologies Used

- Google Cloud Storage
- Pub/Sub
- Cloud Run
- Cloud Run Jobs
- Artifact Registry
- Docker
- FastAPI
- XGBoost
- scikit-learn
- SMOTE
- Cloud Logging

## Components

### 1. Training Service

The training component reads the base dataset from GCS, preprocesses the data, applies SMOTE to handle class imbalance, trains an XGBoost classifier, and uploads the model artifacts to GCS.

### 2. Inference API

The inference API loads the latest model and scaler from GCS and exposes a `/predict` endpoint for real-time fraud prediction.

### 3. Trigger Service

The trigger service receives Pub/Sub push events from Cloud Storage and starts the Cloud Run training job automatically.

## Current Status

- Automated training pipeline implemented
- Cloud Run API deployed
- Pub/Sub-based retraining trigger implemented
- Model registry stored in GCS
- Monitoring and CI/CD planned as future enhancements

## Future Enhancements

- Jenkins CI/CD pipeline
- Prometheus and Grafana monitoring
- Model versioning and rollback
- Drift detection
- Load testing
