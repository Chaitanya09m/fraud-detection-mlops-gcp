# 🚀 End-to-End MLOps Pipeline for Credit Card Fraud Detection

This project implements a **production-style MLOps system** that automates model retraining, deployment, and monitoring using Google Cloud Platform and modern DevOps tools.

---

## 🧠 Problem Statement

Traditional ML systems require manual retraining and deployment when new data arrives.

This project solves that by building a **fully automated, event-driven pipeline** that:

- Retrains models on new data automatically
- Deploys updated APIs via CI/CD
- Monitors system performance in real time

---

## 🏗️ System Architecture

        ┌──────────────┐
        │   New Data   │
        └──────┬───────┘
               ↓
        Google Cloud Storage (GCS)
               ↓
          Pub/Sub Event
               ↓
      Cloud Run Trigger Service
               ↓
      Cloud Run Training Job
               ↓
        Model stored in GCS
               ↓
     FastAPI Inference Service
               ↓
            Predictions

### CI/CD Pipeline

GitHub → Jenkins → Docker → Artifact Registry → Cloud Run

### Monitoring Pipeline

Cloud Run API → /metrics → Prometheus → Grafana Dashboard

---

## ⚙️ Key Features

### 🔁 Automated Model Retraining
- Triggered via **GCS → Pub/Sub → Cloud Run Jobs**
- Uses **XGBoost + SMOTE + preprocessing**
- Stores latest model in GCS (`models/latest/`)

---

### 🚀 CI/CD with Jenkins
- Automated pipeline for:
  - Docker image build
  - Push to Artifact Registry
  - Deployment to Cloud Run
- Supports continuous deployment on code updates

---

### 📊 Monitoring & Observability
- Instrumented FastAPI with **Prometheus metrics**
- Built **Grafana dashboards** to track:
  - API request rate
  - Prediction traffic
  - Error rate (4xx responses)
  - Success ratio

---

## 📁 Project Structure

api/ → FastAPI inference service
training/ → Model training pipeline
trigger/ → Pub/Sub trigger service
monitoring/
├── prometheus/ → Prometheus config
└── grafana/ → Dashboard JSON
Jenkinsfile → CI/CD pipeline
docs/ → Architecture and setup

---

## 🔧 Technologies Used

- **Cloud**: Google Cloud Platform (GCS, Pub/Sub, Cloud Run)
- **MLOps**: Docker, Jenkins, Artifact Registry
- **ML**: XGBoost, SMOTE, Scikit-learn
- **Backend**: FastAPI
- **Monitoring**: Prometheus, Grafana

---

## 📈 Example Metrics

- Request rate (req/sec)
- Prediction endpoint traffic
- Error rate monitoring
- Success vs failure ratio

---

## 🎯 Key Learning Outcomes

- Built a **fully automated MLOps pipeline**
- Implemented **event-driven retraining architecture**
- Designed **CI/CD for ML systems**
- Integrated **real-time monitoring and observability**

---

## 🚀 Future Improvements

- Alerting (Slack/email) for failures
- Model drift detection
- Kubernetes-based deployment (GKE)

---

## 👤 Author

Chaitanya Mishra


