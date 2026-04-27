# Architecture

This project implements an event-driven MLOps pipeline on Google Cloud Platform for credit card fraud detection.

## System Flow

1. A CSV file is uploaded to Google Cloud Storage.
2. Cloud Storage sends an OBJECT_FINALIZE event to Pub/Sub.
3. Pub/Sub pushes the event to the Cloud Run trigger service.
4. The trigger service starts the Cloud Run training job.
5. The training job loads data from GCS, trains an XGBoost model, and uploads model artifacts to GCS.
6. The Cloud Run FastAPI service loads the latest model and serves real-time predictions.

## Architecture Diagram

GCS Data Upload  
→ Pub/Sub Topic  
→ Cloud Run Trigger Service  
→ Cloud Run Training Job  
→ GCS Model Registry  
→ Cloud Run Inference API

## Components

### Training Service
Located in `training/`.  
Responsible for preprocessing data, applying SMOTE, training the XGBoost model, and uploading `fraud_model.pkl` and `scaler.pkl` to GCS.

### Inference API
Located in `api/`.  
Provides a `/predict` endpoint for real-time fraud prediction.

### Trigger Service
Located in `trigger/`.  
Receives Pub/Sub events and starts the training job automatically.