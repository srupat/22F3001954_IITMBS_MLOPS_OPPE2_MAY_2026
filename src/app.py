import json
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel, Field


MODEL_PATH = Path(
    os.getenv(
        "MODEL_PATH",
        "artifacts/heart_disease_model.joblib",
    )
)

artifact = joblib.load(MODEL_PATH)

model = artifact["model"]
FEATURES = artifact["features"]

app = FastAPI(
    title="Heart Disease Prediction API",
    version="1.0.0",
)


class HeartDiseaseInput(BaseModel):
    sno: int = Field(ge=0)
    age: int = Field(ge=1, le=120)
    gender: int = Field(ge=0, le=1)
    cp: int = Field(ge=0, le=4)

    trestbps: float = Field(ge=50, le=300)
    chol: float = Field(ge=50, le=800)

    fbs: int = Field(ge=0, le=1)
    restecg: int = Field(ge=0, le=2)

    thalach: float = Field(ge=40, le=250)

    exang: int = Field(ge=0, le=1)
    oldpeak: float = Field(ge=-5, le=15)

    slope: int = Field(ge=0, le=3)
    ca: int = Field(ge=0, le=4)
    thal: int = Field(ge=0, le=3)


@app.get("/")
def root():
    return {
        "service": "heart-disease-classifier",
        "status": "running",
    }


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: HeartDiseaseInput):
    request_id = str(uuid4())

    features = data.model_dump()

    frame = pd.DataFrame(
        [[features[name] for name in FEATURES]],
        columns=FEATURES,
    )

    prediction = str(model.predict(frame)[0])

    probability = None

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(frame)[0]
        classes = [str(c) for c in model.classes_]

        if "yes" in classes:
            probability = float(
                probabilities[classes.index("yes")]
            )

    log_record = {
        "severity": "INFO",
        "event": "prediction",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": request_id,
        "input_features": features,
        "predicted_output": prediction,
        "heart_disease_probability": probability,
    }

    # GKE collects stdout. Because this is single-line JSON,
    # Cloud Logging can ingest it as structured logging.
    print(json.dumps(log_record), flush=True)

    return {
        "request_id": request_id,
        "prediction": prediction,
        "heart_disease_probability": probability,
    }
