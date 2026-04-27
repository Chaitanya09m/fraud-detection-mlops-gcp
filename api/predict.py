import os
import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from google.cloud import storage
import tempfile

app = FastAPI()

model = None
scaler = None


class TransactionInput(BaseModel):
    data: list[float]


def load_model():
    global model, scaler

    bucket_name = os.getenv("BUCKET_NAME")

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    with tempfile.TemporaryDirectory() as tmpdir:
        model_path = f"{tmpdir}/fraud_model.pkl"
        scaler_path = f"{tmpdir}/scaler.pkl"

        bucket.blob("models/latest/fraud_model.pkl").download_to_filename(model_path)
        bucket.blob("models/latest/scaler.pkl").download_to_filename(scaler_path)

        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)

    print("✅ Model loaded from GCS")


@app.on_event("startup")
def startup_event():
    load_model()


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/predict")
def predict(transaction: TransactionInput):
    data = transaction.data

    if len(data) != 30:
        return {
            "error": "Input must contain exactly 30 values: Time, V1-V28, Amount"
        }

    arr = np.array(data).reshape(1, -1)
    arr_scaled = scaler.transform(arr)

    prediction = model.predict(arr_scaled)[0]
    probability = model.predict_proba(arr_scaled)[0][1]

    return {
        "fraud": int(prediction),
        "fraud_probability": float(probability),
        "fraud_probability_percent": round(float(probability) * 100, 2)
    }
