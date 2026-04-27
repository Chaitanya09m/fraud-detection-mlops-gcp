import os
import base64
import json

from fastapi import FastAPI, Request
from google.auth.transport.requests import Request as GoogleAuthRequest
from google.oauth2 import id_token
import google.auth
import requests

app = FastAPI()

PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
JOB_NAME = os.getenv("JOB_NAME", "fraud-train-job")


def get_access_token():
    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    credentials.refresh(GoogleAuthRequest())
    return credentials.token


@app.post("/")
async def trigger_job(request: Request):
    envelope = await request.json()

    if "message" not in envelope:
        return {"error": "Invalid Pub/Sub message"}

    message = envelope["message"]

    if "data" in message:
        decoded_data = base64.b64decode(message["data"]).decode("utf-8")
        print(f"Received GCS event: {decoded_data}")

    url = (
        f"https://run.googleapis.com/v2/projects/{PROJECT_ID}"
        f"/locations/{REGION}/jobs/{JOB_NAME}:run"
    )

    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json={})

    print(f"Cloud Run Job trigger status: {response.status_code}")
    print(response.text)

    return {
        "status": "triggered",
        "job_response_code": response.status_code,
    }
