# train_model.py

import os
import tempfile
import pandas as pd
import joblib

from google.cloud import storage
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE


def load_data():
    bucket_name = os.getenv("BUCKET_NAME")

    if not bucket_name:
        raise ValueError("BUCKET_NAME environment variable is not set.")

    data_path = f"gs://{bucket_name}/data/base/creditcard_base.csv"

    print(f"📂 Loading data from {data_path}")
    df = pd.read_csv(data_path)
    print(f"✅ Data loaded successfully with shape: {df.shape}")

    return df


def preprocess_data(df):
    print("⚙️ Preprocessing data...")

    X = df.drop("Class", axis=1)
    y = df["Class"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X_scaled, y)

    print(f"✅ Resampled data shape: {X_res.shape}")
    print(f"✅ Fraud cases after SMOTE: {sum(y_res)}")

    return X_res, y_res, scaler


def train_model(X_train, y_train):
    print("🤖 Training XGBoost model...")

    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        tree_method="hist",
        n_jobs=-1,
        eval_metric="logloss"
    )

    model.fit(X_train, y_train)

    print("✅ Model training complete.")
    return model


def evaluate_model(model, X_test, y_test):
    print("📊 Evaluating model...")

    preds = model.predict(X_test)

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, preds))

    print("Classification Report:")
    print(classification_report(y_test, preds))


def save_model(model, scaler):
    bucket_name = os.getenv("BUCKET_NAME")

    if not bucket_name:
        raise ValueError("BUCKET_NAME environment variable is not set.")

    print("💾 Saving model locally first...")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    with tempfile.TemporaryDirectory() as tmpdir:
        model_file = os.path.join(tmpdir, "fraud_model.pkl")
        scaler_file = os.path.join(tmpdir, "scaler.pkl")

        joblib.dump(model, model_file)
        joblib.dump(scaler, scaler_file)

        print("☁️ Uploading model artifacts to GCS...")

        bucket.blob("models/latest/fraud_model.pkl").upload_from_filename(model_file)
        bucket.blob("models/latest/scaler.pkl").upload_from_filename(scaler_file)

    print(f"✅ Model uploaded to gs://{bucket_name}/models/latest/fraud_model.pkl")
    print(f"✅ Scaler uploaded to gs://{bucket_name}/models/latest/scaler.pkl")


def main():
    df = load_data()

    X_res, y_res, scaler = preprocess_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X_res,
        y_res,
        test_size=0.2,
        random_state=42
    )

    model = train_model(X_train, y_train)

    evaluate_model(model, X_test, y_test)

    save_model(model, scaler)


if __name__ == "__main__":
    main()
