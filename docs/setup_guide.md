# Setup Guide

## 1. Enable GCP Services

```bash
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  storage.googleapis.com \
  pubsub.googleapis.com \
  cloudbuild.googleapis.com
````

## 2. Create GCS Bucket

```bash
gsutil mb -l us-central1 gs://<PROJECT_ID>-fraud-bucket
```

## 3. Upload Base Dataset

```bash
gsutil cp creditcard.csv gs://<PROJECT_ID>-fraud-bucket/data/base/creditcard_base.csv
```

## 4. Create Artifact Registry Repository

```bash
gcloud artifacts repositories create fraud-repo \
  --repository-format=docker \
  --location=us-central1
```

## 5. Build and Deploy Training Job

```bash
cd training

gcloud builds submit \
  --tag us-central1-docker.pkg.dev/<PROJECT_ID>/fraud-repo/fraud-train:v1
```

## 6. Build and Deploy API

```bash
cd api

gcloud builds submit \
  --tag us-central1-docker.pkg.dev/<PROJECT_ID>/fraud-repo/fraud-api:v1
```

## 7. Build and Deploy Trigger Service

```bash
cd trigger

gcloud builds submit \
  --tag us-central1-docker.pkg.dev/<PROJECT_ID>/fraud-repo/fraud-trigger:v1
```

## 8. Test Prediction

```bash
curl -X POST "<API_URL>/predict" \
  -H "Content-Type: application/json" \
  --data-raw '{"data":[1000,-1,0.5,0.1,-0.2,0,0.03,-0.07,0.12,-0.05,0.01,-0.02,0.08,0,-0.03,0.04,-0.01,0.02,-0.04,0.05,-0.02,0.01,0,-0.01,0.02,-0.01,0.01,0,-0.02,50]}'
```
