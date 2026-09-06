# OPPE AI Usage Documentation 

## Prompts and Responses Used
Sharing all conversation history as I have used a commercial version of GPT that does not support sharing the link.

### Tool Name #1: ChatGPT
Seperating prompt from agent response by "---" (i.e a horizontal line in markdown)

---

It's time for OPPE2. Here are the instructions on what to do. We will be mostly doing everything using GCP. Give me the steps to do for the end to end pipeline.

# Heart Disease classification dataset and Training/Inference Scripts

[svg](https://github.com/IITMBSMLOps/MLOPS_MAY_2026_OPPE2#heart-disease-classification-dataset-and-traininginference-scripts)

## Dataset Description

[svg](https://github.com/IITMBSMLOps/MLOPS_MAY_2026_OPPE2#dataset-description)

This data set dates from 1988 and consists of four databases: Cleveland, Hungary, Switzerland, and Long Beach V. It contains 76 attributes, including the predicted attribute, but all published experiments refer to using a subset of 14 of them.

The "target" field refers to the presence of heart disease in the patient.

## Feature Information

[svg](https://github.com/IITMBSMLOps/MLOPS_MAY_2026_OPPE2#feature-information)

- sno - Obsevation Index
- age
- sex
- chest pain type (4 values)
- resting blood pressure
- serum cholestoral in mg/dl
- fasting blood sugar > 120 mg/dl
- resting electrocardiographic results (values 0,1,2)
- maximum heart rate achieved
- exercise induced angina
- oldpeak = ST depression induced by exercise relative to rest
- the slope of the peak exercise ST segment
- number of major vessels (0-3) colored by flourosopy
- thal: 0 = normal; 1 = fixed defect; 2 = reversable defect

## Training and Inference Notebook

[svg](https://github.com/IITMBSMLOps/MLOPS_MAY_2026_OPPE2#training-and-inference-notebook)

[IPython Notebook](https://github.com/IITMBSMLOps/MLOPS_MAY_2026_OPPE2/blob/main/HeartDiseaseTrainingAndPrediction.ipynb)

## OPPE-2: Problem Statement

Build a production-ready, explainable, observable, scalable, and maintainable deployment for a heart disease prediction model on Google Cloud Platform (GCP).

###

### Role & Objective

As an **MLOps engineer** at a healthcare firm, you need to transition a heart disease prediction model from a notebook to a production-ready environment. The model classifies whether a patient is likely to have heart disease based on 14 clinical attributes.

Your task is to build a **dockerized, API-served deployment on Google Kubernetes Engine (GKE)** with end-to-end CI/CD. You must ensure the system is **explainable, fair, observable, scalable**, and **resilient to data drift and adversarial attacks**.

## Pipeline Overview

This sequence outlines the high-level flow of the deployment pipeline. Refer to the Deliverables section below for specific implementation instructions, requirements, and marking criteria before you begin building.

1. **Data & Scripts:** Heart disease dataset and scripts from the `MLOPS_MAY_2026_OPPE2` repository (`main` branch).
2. **Responsible AI:** Explainability and fairness analysis using SHAP and Fairlearn (bias detection on gender).
3. **Deployment:** Dockerized API deployed on GKE with Kubernetes autoscaling (maximum of 3 pods) and CI/CD via GitHub Actions.
4. **Observability:** Logging and monitoring, including per-sample prediction logging using a 100-row random dataset.
5. **Stress Testing:** Performance monitoring under load using `wrk` with over 2,000 concurrent connections to analyze throughput, latency, and timeouts.
6. **Drift Detection:** Input drift analysis comparing the training data distribution against the generated prediction data.

## Deliverables

### Deliverable 1 [Mandatory]: Setup Private Git Repository

- Set up a private Git repository.
- Use the following repository name format: `<IITM_BS_ROLL_NUMBER>_IITMBS_MLOPS_OPPE2_MAY_2026` (e.g., `21F10005000_IITMBS_MLOPS_OPPE2_MAY_2026`).
- **Important:** Add collaborator access for [**IITMBSMLOps**](https://github.com/IITMBSMLOps) or **da5014\_1\@study.iitm.ac.in**.

**Before leaving the exam, verify that the collaborator invitation has been accepted by checking your GitHub repository's collaborators list.** If the invitation is still pending, notify the course team before your session ends.

### Deliverable 2 [10 Marks]: Model Explainability

Using explainability tools, describe in plain English the factors that have the **least impact** on predicting whether a patient has heart disease.

### Deliverable 3 [10 Marks]: Fairness Testing with Fairlearn

Test the model for fairness using **Fairlearn**, with **"age"** as the sensitive attribute.

### Deliverable 4 [40 Marks]: Dockerized API Deployment on GKE

Convert the provided notebook into a **dockerized, API-deployed** model running on GCP.

- Use **Kubernetes** with autoscaling (configured for a **maximum of 3 pods**) as the deployment layer.
- CI/CD workflows must be triggered using **GitHub Actions**.

### Deliverable 5 [20 Marks]: Per-Sample Prediction with Logging & Observability

Generate a **100-row random dataset** and run per-sample predictions through your deployed API.

- Log each prediction request individually with its input features, predicted output, and timestamp.
- Demonstrate observability using **GCP Cloud Logging**.

### Deliverable 6 [10 Marks]: Performance Monitoring & Stress Testing with wrk

Stress test your deployed API using `wrk` with a high-concurrency workload (**greater than 2,000 concurrent connections**).

- Analyze throughput, latency distribution, and request timeout behavior under load.
- You may reuse the 100-row random sample data generated in Deliverable 5.

### Deliverable 7 [10 Marks]: Input Drift Detection

Detect whether the distribution of incoming data has shifted from the training data.

- Compute input drift by comparing the **training data distribution** against the **100-row generated dataset** used for prediction in Deliverable 5.

**Total: 100 marks** (10 + 10 + 40 + 20 + 10 + 10)


___

Yes. We should treat OPPE2 as a fresh production pipeline and build it deliberately in stages so we do not end up debugging GKE, CI/CD, SHAP, Fairlearn, logging, and load testing simultaneously.

I inspected the notebook you uploaded. The supplied baseline loads `data/data.csv`, factorizes `gender`, drops missing rows, performs an 80/20 split, and tunes a `LogisticRegression` using `RandomizedSearchCV` over `C` with the `liblinear` solver. The notebook's recorded test score is about `0.983`. I will preserve that modeling approach while turning it into proper scripts and production artifacts.

One important interpretation: the overview mentions fairness on gender, but **Deliverable 3 explicitly requires `age` as the sensitive attribute**, so we will use age for the marked Fairlearn audit.

Our final architecture will be:

```text
Course Heart Disease dataset
        ↓
Training script
        ↓
Logistic Regression model artifact
        ├── SHAP explainability
        └── Fairlearn age fairness audit
        ↓
FastAPI prediction service
        ↓
Docker image
        ↓
Artifact Registry
        ↓
GKE Deployment
        ├── LoadBalancer
        └── HPA: 1 → max 3 pods
        ↓
GitHub Actions CI/CD
        ↓
100 generated prediction requests
        ↓
Structured prediction logs → Cloud Logging
        ↓
wrk > 2,000 concurrent connections
        ↓
Drift: training vs generated inputs
```

GKE collects workload stdout/stderr into Cloud Logging by default, and single-line JSON written by containers can become structured log entries, which is exactly what we will use for per-prediction logging. ([Google Cloud Documentation][1]) GKE HPA supports explicit `minReplicas`/`maxReplicas`, so we will hard-limit this deployment at three pods as required. ([Google Cloud Documentation][2])

---

# PHASE 1 — GCP + private repository

## 1. Create the private GitHub repo

On GitHub create:

```text
22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026
```

Set:

```text
Visibility: Private
```

Then:

```text
Settings
→ Collaborators
→ Add people
```

Add:

```text
IITMBSMLOps
```

or:

```text
da5014_1@study.iitm.ac.in
```

**Before submission, verify that the invitation is accepted.**

Do not forget this — it is mandatory.

---

# 2. Open GCP Cloud Shell

Use project:

```text
mlops-499806
```

Run:

```bash
gcloud config set project mlops-499806

PROJECT_ID="mlops-499806"
REGION="us-central1"
ZONE="us-central1-a"

gcloud config set compute/region "$REGION"
gcloud config set compute/zone "$ZONE"
```

Verify:

```bash
gcloud config list
```

---

# 3. Enable APIs

```bash
gcloud services enable \
  container.googleapis.com \
  artifactregistry.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com \
  iamcredentials.googleapis.com \
  sts.googleapis.com
```

---

# 4. Clone your private repo

```bash
cd ~

git clone https://github.com/srupat/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026.git

cd 22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026
```

Configure identity if needed:

```bash
git config --global user.name "Srujan Patwardhan"
git config --global user.email "YOUR_GITHUB_EMAIL"
```

---

# PHASE 2 — Import the assignment data

## 5. Clone the supplied OPPE2 repository temporarily

```bash
cd ~

git clone https://github.com/IITMBSMLOps/MLOPS_MAY_2026_OPPE2.git oppe2-source

cd ~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026

mkdir -p data reference src artifacts reports tests k8s scripts .github/workflows
```

Copy the provided data and notebook:

```bash
cp ~/oppe2-source/data/data.csv data/data.csv
cp ~/oppe2-source/HeartDiseaseTrainingAndPrediction.ipynb reference/
```

Check:

```bash
head data/data.csv
```

Then remove the temporary source clone:

```bash
rm -rf ~/oppe2-source
```

---

# 6. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate

python --version
pip install --upgrade pip
```

Create runtime requirements:

```bash
cat > requirements.txt <<'EOF'
fastapi
uvicorn[standard]
pandas
numpy
scikit-learn
joblib
pydantic
EOF
```

Create development/analysis requirements:

```bash
cat > requirements-dev.txt <<'EOF'
-r requirements.txt
shap
fairlearn
matplotlib
scipy
requests
pytest
httpx
tabulate
EOF
```

Install:

```bash
pip install -r requirements-dev.txt
```

---

# PHASE 3 — Convert notebook into training script

## 7. Create `src/train.py`

```bash
cat > src/train.py <<'EOF'
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


RANDOM_STATE = 42

DATA_PATH = Path("data/data.csv")
ARTIFACT_DIR = Path("artifacts")
REPORT_DIR = Path("reports")

FEATURES = [
    "sno",
    "age",
    "gender",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
]

TARGET = "target"


def prepare_data():
    df = pd.read_csv(DATA_PATH)

    # Preserve the encoding used by the supplied notebook,
    # but make it deterministic for inference.
    if df["gender"].dtype == object:
        gender_mapping = {
            "male": 0,
            "female": 1,
        }

        df["gender"] = (
            df["gender"]
            .astype(str)
            .str.lower()
            .map(gender_mapping)
        )

    cleaned_df = df.dropna().copy()

    cleaned_df[TARGET] = (
        cleaned_df[TARGET]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    return cleaned_df


def main():
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    df = prepare_data()

    X = df[FEATURES].copy()
    y = df[TARGET].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    search_space = {
        "C": np.logspace(-4, 4, 20),
        "solver": ["liblinear"],
    }

    search = RandomizedSearchCV(
        estimator=LogisticRegression(max_iter=1000),
        param_distributions=search_space,
        n_iter=20,
        cv=5,
        random_state=RANDOM_STATE,
        verbose=1,
        n_jobs=-1,
    )

    search.fit(X_train, y_train)

    model = search.best_estimator_
    predictions = model.predict(X_test)

    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(
            precision_score(
                y_test,
                predictions,
                pos_label="yes",
                zero_division=0,
            )
        ),
        "recall": float(
            recall_score(
                y_test,
                predictions,
                pos_label="yes",
                zero_division=0,
            )
        ),
        "f1": float(
            f1_score(
                y_test,
                predictions,
                pos_label="yes",
                zero_division=0,
            )
        ),
        "best_params": search.best_params_,
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "clean_rows": len(df),
        "confusion_matrix": confusion_matrix(
            y_test,
            predictions,
            labels=["no", "yes"],
        ).tolist(),
    }

    artifact = {
        "model": model,
        "features": FEATURES,
        "gender_mapping": {
            "male": 0,
            "female": 1,
        },
        "target": TARGET,
    }

    joblib.dump(
        artifact,
        ARTIFACT_DIR / "heart_disease_model.joblib",
    )

    train_output = X_train.copy()
    train_output[TARGET] = y_train.values

    test_output = X_test.copy()
    test_output[TARGET] = y_test.values

    train_output.to_csv(
        ARTIFACT_DIR / "train_split.csv",
        index=False,
    )

    test_output.to_csv(
        ARTIFACT_DIR / "test_split.csv",
        index=False,
    )

    df.to_csv(
        ARTIFACT_DIR / "cleaned_data.csv",
        index=False,
    )

    with open(REPORT_DIR / "model_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    print(json.dumps(metrics, indent=4))
    print("\nSaved model to artifacts/heart_disease_model.joblib")


if __name__ == "__main__":
    main()
EOF
```

Run:

```bash
python src/train.py
```

Inspect:

```bash
cat reports/model_metrics.json
ls -lh artifacts
```

Checkpoint: **do not proceed if this fails.**

---

# Important note about `sno`

The supplied notebook includes `sno` because it simply does:

```python
x = cleaned_df.drop("target", axis=1)
```

So we are preserving it for consistency with the provided model.

However, `sno` is an observation identifier rather than a genuine clinical feature. In a real production model I would investigate removing it because an index can create accidental leakage.

This is actually a useful point to mention during the screencast.

---

# PHASE 4 — Deliverable 2: SHAP explainability

## 8. Create `src/explain.py`

```bash
cat > src/explain.py <<'EOF'
import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap


ARTIFACT_PATH = Path("artifacts/heart_disease_model.joblib")
TRAIN_PATH = Path("artifacts/train_split.csv")
TEST_PATH = Path("artifacts/test_split.csv")
REPORT_DIR = Path("reports")


def main():
    REPORT_DIR.mkdir(exist_ok=True)

    artifact = joblib.load(ARTIFACT_PATH)
    model = artifact["model"]
    features = artifact["features"]

    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)

    X_train = train_df[features]
    X_test = test_df[features]

    explainer = shap.Explainer(model, X_train)
    shap_values = explainer(X_test)

    values = np.asarray(shap_values.values)

    if values.ndim == 3:
        mean_abs_shap = np.abs(values).mean(axis=(0, 2))
    else:
        mean_abs_shap = np.abs(values).mean(axis=0)

    importance = pd.DataFrame(
        {
            "feature": features,
            "mean_absolute_shap": mean_abs_shap,
        }
    ).sort_values("mean_absolute_shap", ascending=True)

    importance.to_csv(
        REPORT_DIR / "shap_feature_importance.csv",
        index=False,
    )

    least = importance.head(5)

    with open(REPORT_DIR / "shap_least_impact.json", "w") as f:
        json.dump(
            least.to_dict(orient="records"),
            f,
            indent=4,
        )

    plt.figure()
    shap.plots.beeswarm(
        shap_values,
        max_display=len(features),
        show=False,
    )
    plt.tight_layout()
    plt.savefig(
        REPORT_DIR / "shap_summary.png",
        dpi=160,
        bbox_inches="tight",
    )
    plt.close()

    print("\nFeatures with the least model impact:")
    print(least.to_string(index=False))

    print(
        "\nInterpretation: smaller mean absolute SHAP values mean "
        "that changing the feature generally changes the model output less."
    )


if __name__ == "__main__":
    main()
EOF
```

Run:

```bash
python src/explain.py
```

Show:

```bash
cat reports/shap_least_impact.json
```

Later, your screencast statement will use the **actual lowest features from this output**, not guesses.

---

# PHASE 5 — Deliverable 3: Fairlearn with age

## 9. Create `src/fairness.py`

We will explicitly treat **age as the sensitive attribute**. Because exact ages create many tiny groups, we will report both exact age and useful age cohorts.

```bash
cat > src/fairness.py <<'EOF'
import json
from functools import partial
from pathlib import Path

import joblib
import pandas as pd

from fairlearn.metrics import MetricFrame
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
)


ARTIFACT_PATH = Path("artifacts/heart_disease_model.joblib")
TEST_PATH = Path("artifacts/test_split.csv")
REPORT_DIR = Path("reports")


def main():
    REPORT_DIR.mkdir(exist_ok=True)

    artifact = joblib.load(ARTIFACT_PATH)
    model = artifact["model"]
    features = artifact["features"]

    test_df = pd.read_csv(TEST_PATH)

    X_test = test_df[features]
    y_test = test_df["target"]

    predictions = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score,
        "precision": partial(
            precision_score,
            pos_label="yes",
            zero_division=0,
        ),
        "recall": partial(
            recall_score,
            pos_label="yes",
            zero_division=0,
        ),
    }

    # Direct age-based Fairlearn audit
    exact_age_frame = MetricFrame(
        metrics=metrics,
        y_true=y_test,
        y_pred=predictions,
        sensitive_features=test_df["age"],
    )

    exact_age = exact_age_frame.by_group
    exact_age.to_csv(
        REPORT_DIR / "fairness_by_exact_age.csv"
    )

    # Cohorts make the fairness comparison easier to interpret.
    age_groups = pd.cut(
        test_df["age"],
        bins=[0, 49, 59, float("inf")],
        labels=["under_50", "50_to_59", "60_plus"],
    )

    cohort_frame = MetricFrame(
        metrics=metrics,
        y_true=y_test,
        y_pred=predictions,
        sensitive_features=age_groups,
    )

    by_group = cohort_frame.by_group
    by_group.to_csv(
        REPORT_DIR / "fairness_by_age_group.csv"
    )

    differences = cohort_frame.difference(
        method="between_groups"
    )

    ratios = cohort_frame.ratio(
        method="between_groups"
    )

    summary = {
        "overall": {
            k: float(v)
            for k, v in cohort_frame.overall.to_dict().items()
        },
        "difference_between_age_groups": {
            k: float(v)
            for k, v in differences.to_dict().items()
        },
        "ratio_between_age_groups": {
            k: float(v)
            for k, v in ratios.to_dict().items()
        },
    }

    with open(REPORT_DIR / "fairness_summary.json", "w") as f:
        json.dump(summary, f, indent=4)

    print("\nFairness metrics by age cohort:")
    print(by_group)

    print("\nFairness gaps:")
    print(json.dumps(summary, indent=4))


if __name__ == "__main__":
    main()
EOF
```

Run:

```bash
python src/fairness.py
```

Inspect:

```bash
cat reports/fairness_by_age_group.csv
cat reports/fairness_summary.json
```

For the screencast:

> Fairlearn does not itself declare a model “fair” or “unfair.” MetricFrame disaggregates performance across the sensitive groups so we can inspect whether meaningful gaps exist.

---

# PHASE 6 — Production FastAPI

## 10. Create `src/app.py`

```bash
cat > src/app.py <<'EOF'
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
EOF
```

GKE's logging agent collects application stdout/stderr, and valid single-line JSON is specifically supported as structured logging. ([Google Cloud Documentation][1])

---

# 11. Test API locally inside Cloud Shell

Run:

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8080
```

Open another Cloud Shell tab and test:

```bash
curl -X POST http://127.0.0.1:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sno": 87,
    "age": 46,
    "gender": 0,
    "cp": 1,
    "trestbps": 101,
    "chol": 197,
    "fbs": 1,
    "restecg": 1,
    "thalach": 156,
    "exang": 0,
    "oldpeak": 0,
    "slope": 2,
    "ca": 0,
    "thal": 3
  }'
```

You should get:

```json
{
  "request_id": "...",
  "prediction": "...",
  "heart_disease_probability": ...
}
```

Stop server:

```text
Ctrl + C
```

---

# PHASE 7 — Docker

## 12. Create Dockerfile

```bash
cat > Dockerfile <<'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY artifacts ./artifacts

ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=/app/artifacts/heart_disease_model.joblib

EXPOSE 8080

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]
EOF
```

Create `.dockerignore`:

```bash
cat > .dockerignore <<'EOF'
.git
.github
venv
__pycache__
.pytest_cache
reports
reference
tests
EOF
```

---

# 13. Test Docker

```bash
docker build -t heart-disease-api:local .
```

Run:

```bash
docker run --rm -d \
  --name heart-api-test \
  -p 8080:8080 \
  heart-disease-api:local
```

Check:

```bash
curl http://127.0.0.1:8080/healthz
```

Then:

```bash
docker stop heart-api-test
```

---

# PHASE 8 — Artifact Registry

## 14. Create repository

```bash
AR_REPO="oppe2-repo"

gcloud artifacts repositories create "$AR_REPO" \
  --repository-format=docker \
  --location="$REGION" \
  --description="OPPE2 Heart Disease API"
```

If it already exists, ignore the `ALREADY_EXISTS` error.

Authenticate Docker:

```bash
gcloud auth configure-docker \
  us-central1-docker.pkg.dev
```

Artifact Registry requires configuring Docker for the specific regional hostname such as `us-central1-docker.pkg.dev`. ([Google Cloud Documentation][3])

Set image:

```bash
IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${AR_REPO}/heart-disease-api"
```

Tag:

```bash
docker tag heart-disease-api:local \
  "${IMAGE_URI}:v1"
```

Push:

```bash
docker push "${IMAGE_URI}:v1"
```

Check:

```bash
gcloud artifacts docker images list \
  "${REGION}-docker.pkg.dev/${PROJECT_ID}/${AR_REPO}"
```

---

# PHASE 9 — GKE

We'll use a **GKE Standard cluster** because it gives you very clear pod/HPA behavior during the exam.

## 15. Create cluster

```bash
CLUSTER_NAME="oppe2-heart-cluster"

gcloud container clusters create "$CLUSTER_NAME" \
  --zone="$ZONE" \
  --machine-type="e2-standard-2" \
  --num-nodes=1 \
  --enable-ip-alias \
  --release-channel=regular \
  --logging=SYSTEM,WORKLOAD
```

Current GKE supports `SYSTEM` and `WORKLOAD` logging components when creating Standard clusters. ([Google Cloud Documentation][4])

Get credentials:

```bash
gcloud container clusters get-credentials \
  "$CLUSTER_NAME" \
  --zone="$ZONE" \
  --project="$PROJECT_ID"
```

Check:

```bash
kubectl get nodes
```

---

# 16. Kubernetes namespace

```bash
cat > k8s/namespace.yaml <<'EOF'
apiVersion: v1
kind: Namespace
metadata:
  name: heart-disease
EOF
```

---

# 17. Deployment manifest

```bash
cat > k8s/deployment.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment

metadata:
  name: heart-disease-api
  namespace: heart-disease

spec:
  replicas: 1

  selector:
    matchLabels:
      app: heart-disease-api

  template:
    metadata:
      labels:
        app: heart-disease-api

    spec:
      containers:
        - name: heart-disease-api
          image: IMAGE_PLACEHOLDER

          ports:
            - containerPort: 8080

          resources:
            requests:
              cpu: "200m"
              memory: "256Mi"

            limits:
              cpu: "750m"
              memory: "512Mi"

          readinessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10

          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
EOF
```

CPU requests matter because CPU-based HPA needs a resource request from which utilization can be calculated. ([Google Cloud Documentation][5])

---

# 18. LoadBalancer service

```bash
cat > k8s/service.yaml <<'EOF'
apiVersion: v1
kind: Service

metadata:
  name: heart-disease-api
  namespace: heart-disease

spec:
  type: LoadBalancer

  selector:
    app: heart-disease-api

  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
EOF
```

---

# 19. HPA — maximum exactly 3 pods

```bash
cat > k8s/hpa.yaml <<'EOF'
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler

metadata:
  name: heart-disease-api-hpa
  namespace: heart-disease

spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: heart-disease-api

  minReplicas: 1
  maxReplicas: 3

  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0

    scaleDown:
      stabilizationWindowSeconds: 60

  metrics:
    - type: Resource
      resource:
        name: cpu

        target:
          type: Utilization
          averageUtilization: 60
EOF
```

This directly meets the **maximum 3 pods** requirement. `maxReplicas` is the HPA upper bound. ([Google Cloud Documentation][6])

---

# 20. Deploy manually once

```bash
kubectl apply -f k8s/namespace.yaml

sed "s|IMAGE_PLACEHOLDER|${IMAGE_URI}:v1|g" \
  k8s/deployment.yaml \
  | kubectl apply -f -

kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

Watch:

```bash
kubectl get pods -n heart-disease
```

```bash
kubectl get hpa -n heart-disease
```

```bash
kubectl get service -n heart-disease
```

Wait for:

```text
EXTERNAL-IP
```

Set:

```bash
EXTERNAL_IP=$(kubectl get service heart-disease-api \
  -n heart-disease \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo "$EXTERNAL_IP"
```

Test:

```bash
curl "http://${EXTERNAL_IP}/healthz"
```

---

# PHASE 10 — GitHub Actions CI/CD

This is worth **40 marks together with deployment**, so we should make it robust.

## 21. Dedicated GitHub Actions service account

```bash
SA_NAME="github-actions-oppe2"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
```

Create:

```bash
gcloud iam service-accounts create "$SA_NAME" \
  --display-name="GitHub Actions OPPE2"
```

Grant Artifact Registry:

```bash
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/artifactregistry.writer"
```

For the exam, use Container Admin to avoid Kubernetes IAM blocking deployment:

```bash
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/container.admin"
```

---

# 22. Workload Identity Federation

Do not reuse a provider whose attribute condition is tied to your old weekly repo. We'll create a dedicated OPPE2 provider.

Get project number:

```bash
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" \
  --format='value(projectNumber)')

echo "$PROJECT_NUMBER"
```

Use your existing pool:

```bash
POOL_ID="github-actions-pool"
```

Check:

```bash
gcloud iam workload-identity-pools describe "$POOL_ID" \
  --project="$PROJECT_ID" \
  --location="global"
```

If that says it does not exist:

```bash
gcloud iam workload-identity-pools create "$POOL_ID" \
  --project="$PROJECT_ID" \
  --location="global" \
  --display-name="GitHub Actions Pool"
```

Create OPPE2 provider:

```bash
PROVIDER_ID="oppe2-provider"
GITHUB_REPO="srupat/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026"
```

```bash
gcloud iam workload-identity-pools providers create-oidc "$PROVIDER_ID" \
  --project="$PROJECT_ID" \
  --location="global" \
  --workload-identity-pool="$POOL_ID" \
  --display-name="OPPE2 GitHub Provider" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.ref=assertion.ref,attribute.actor=assertion.actor" \
  --attribute-condition="attribute.repository == '${GITHUB_REPO}'"
```

Grant impersonation:

```bash
gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
  --project="$PROJECT_ID" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_ID}/attribute.repository/${GITHUB_REPO}"
```

Get provider resource:

```bash
gcloud iam workload-identity-pools providers describe "$PROVIDER_ID" \
  --project="$PROJECT_ID" \
  --location="global" \
  --workload-identity-pool="$POOL_ID" \
  --format='value(name)'
```

Copy the result.

---

# 23. GitHub secrets

Repository:

```text
Settings
→ Secrets and variables
→ Actions
```

Create:

```text
GCP_WORKLOAD_IDENTITY_PROVIDER
```

Value will look like:

```text
projects/961685377398/locations/global/workloadIdentityPools/github-actions-pool/providers/oppe2-provider
```

Create:

```text
GCP_SERVICE_ACCOUNT
```

Value:

```text
github-actions-oppe2@mlops-499806.iam.gserviceaccount.com
```

---

# 24. Tests

Create:

```bash
cat > tests/test_model.py <<'EOF'
from pathlib import Path

import joblib
import pandas as pd


MODEL_PATH = Path("artifacts/heart_disease_model.joblib")


def test_model_exists():
    assert MODEL_PATH.exists()


def test_model_loads():
    artifact = joblib.load(MODEL_PATH)

    assert "model" in artifact
    assert "features" in artifact


def test_model_predicts():
    artifact = joblib.load(MODEL_PATH)

    model = artifact["model"]
    features = artifact["features"]

    test_df = pd.read_csv(
        "artifacts/test_split.csv"
    )

    prediction = model.predict(
        test_df[features].head(1)
    )

    assert prediction[0] in {"yes", "no"}
EOF
```

Run:

```bash
pytest tests -v
```

---

# 25. GitHub Actions workflow

```bash
cat > .github/workflows/cicd.yml <<'EOF'
name: OPPE2 CI CD

on:
  push:
    branches:
      - main

  workflow_dispatch:

permissions:
  contents: read
  id-token: write

env:
  PROJECT_ID: mlops-499806
  REGION: us-central1
  ZONE: us-central1-a
  CLUSTER_NAME: oppe2-heart-cluster
  AR_REPO: oppe2-repo
  NAMESPACE: heart-disease

jobs:
  build-test-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v3
        with:
          workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
          service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

      - name: Setup Google Cloud CLI
        uses: google-github-actions/setup-gcloud@v3

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      - name: Train model
        run: |
          python src/train.py

      - name: Run tests
        run: |
          pytest tests -v

      - name: Configure Artifact Registry Docker auth
        run: |
          gcloud auth configure-docker \
            ${REGION}-docker.pkg.dev \
            --quiet

      - name: Build and push Docker image
        run: |
          IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${AR_REPO}/heart-disease-api"

          docker build \
            -t "${IMAGE_URI}:${GITHUB_SHA}" \
            -t "${IMAGE_URI}:latest" \
            .

          docker push "${IMAGE_URI}:${GITHUB_SHA}"
          docker push "${IMAGE_URI}:latest"

      - name: Get GKE credentials
        uses: google-github-actions/get-gke-credentials@v3
        with:
          cluster_name: ${{ env.CLUSTER_NAME }}
          location: ${{ env.ZONE }}

      - name: Deploy to GKE
        run: |
          IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${AR_REPO}/heart-disease-api:${GITHUB_SHA}"

          kubectl apply -f k8s/namespace.yaml

          sed "s|IMAGE_PLACEHOLDER|${IMAGE_URI}|g" \
            k8s/deployment.yaml \
            | kubectl apply -f -

          kubectl apply -f k8s/service.yaml
          kubectl apply -f k8s/hpa.yaml

          kubectl rollout status \
            deployment/heart-disease-api \
            -n ${NAMESPACE} \
            --timeout=180s

          kubectl get pods -n ${NAMESPACE}
          kubectl get hpa -n ${NAMESPACE}
          kubectl get service -n ${NAMESPACE}
EOF
```

GitHub Actions authentication supports Workload Identity Federation rather than long-lived service-account keys, and the GKE credentials action prepares the kubeconfig used by subsequent `kubectl` commands. ([GitHub][7])

---

# PHASE 11 — Generate 100 random records

## 26. Create `src/generate_random_data.py`

```bash
cat > src/generate_random_data.py <<'EOF'
from pathlib import Path

import numpy as np
import pandas as pd


RANDOM_STATE = 42
N = 100

INPUT = Path("artifacts/cleaned_data.csv")
OUTPUT = Path("data/generated_100.csv")

CONTINUOUS = [
    "age",
    "trestbps",
    "chol",
    "thalach",
    "oldpeak",
]

CATEGORICAL = [
    "gender",
    "cp",
    "fbs",
    "restecg",
    "exang",
    "slope",
    "ca",
    "thal",
]


def main():
    rng = np.random.default_rng(RANDOM_STATE)

    train = pd.read_csv(INPUT)

    output = pd.DataFrame()

    output["sno"] = rng.integers(
        int(train["sno"].min()),
        int(train["sno"].max()) + 1,
        N,
    )

    for feature in CONTINUOUS:
        low = float(train[feature].min())
        high = float(train[feature].max())

        output[feature] = rng.uniform(
            low,
            high,
            N,
        )

    output["age"] = output["age"].round().astype(int)

    for feature in CATEGORICAL:
        values = train[feature].dropna().unique()

        output[feature] = rng.choice(
            values,
            size=N,
            replace=True,
        )

    feature_order = [
        "sno",
        "age",
        "gender",
        "cp",
        "trestbps",
        "chol",
        "fbs",
        "restecg",
        "thalach",
        "exang",
        "oldpeak",
        "slope",
        "ca",
        "thal",
    ]

    output = output[feature_order]

    for col in [
        "sno",
        "age",
        "gender",
        "cp",
        "fbs",
        "restecg",
        "exang",
        "slope",
        "ca",
        "thal",
    ]:
        output[col] = output[col].round().astype(int)

    OUTPUT.parent.mkdir(exist_ok=True)
    output.to_csv(OUTPUT, index=False)

    print(output.head())
    print(f"\nGenerated {len(output)} rows at {OUTPUT}")


if __name__ == "__main__":
    main()
EOF
```

Run:

```bash
python src/generate_random_data.py
```

Check:

```bash
wc -l data/generated_100.csv
head data/generated_100.csv
```

Expected:

```text
101
```

because header + 100 rows.

---

# PHASE 12 — Send all 100 through deployed API

## 27. Create `src/predict_100.py`

```bash
cat > src/predict_100.py <<'EOF'
import argparse
import time
from pathlib import Path

import pandas as pd
import requests


INPUT_PATH = Path("data/generated_100.csv")
OUTPUT_PATH = Path("reports/predictions_100.csv")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()

    df = pd.read_csv(INPUT_PATH)

    rows = []

    for index, row in df.iterrows():
        payload = {
            "sno": int(row["sno"]),
            "age": int(row["age"]),
            "gender": int(row["gender"]),
            "cp": int(row["cp"]),
            "trestbps": float(row["trestbps"]),
            "chol": float(row["chol"]),
            "fbs": int(row["fbs"]),
            "restecg": int(row["restecg"]),
            "thalach": float(row["thalach"]),
            "exang": int(row["exang"]),
            "oldpeak": float(row["oldpeak"]),
            "slope": int(row["slope"]),
            "ca": int(row["ca"]),
            "thal": int(row["thal"]),
        }

        started = time.perf_counter()

        response = requests.post(
            f"{args.url}/predict",
            json=payload,
            timeout=10,
        )

        latency_ms = (
            time.perf_counter() - started
        ) * 1000

        result = response.json()

        rows.append(
            {
                **payload,
                "status_code": response.status_code,
                "prediction": result.get("prediction"),
                "heart_disease_probability": result.get(
                    "heart_disease_probability"
                ),
                "request_id": result.get("request_id"),
                "latency_ms": latency_ms,
            }
        )

        print(
            f"{index + 1:03d}/100 "
            f"status={response.status_code} "
            f"prediction={result.get('prediction')} "
            f"latency={latency_ms:.1f}ms"
        )

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(f"\nSaved predictions to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
EOF
```

Run:

```bash
EXTERNAL_IP=$(kubectl get service heart-disease-api \
  -n heart-disease \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

python src/predict_100.py \
  --url "http://${EXTERNAL_IP}"
```

Check:

```bash
head reports/predictions_100.csv
```

---

# PHASE 13 — Cloud Logging

Because every `/predict` call writes one JSON log event, you should now have at least 100 prediction entries.

CLI check:

```bash
gcloud logging read \
'resource.type="k8s_container"
AND resource.labels.cluster_name="oppe2-heart-cluster"
AND resource.labels.namespace_name="heart-disease"
AND jsonPayload.event="prediction"' \
--limit=10 \
--format=json
```

For the screencast use:

```text
GCP Console
→ Logging
→ Logs Explorer
```

Filter:

```text
resource.type="k8s_container"
resource.labels.cluster_name="oppe2-heart-cluster"
resource.labels.namespace_name="heart-disease"
jsonPayload.event="prediction"
```

GKE application logs are available as `k8s_container` resources in Cloud Logging. ([Google Cloud Documentation][8])

You should be able to expand a log and show:

```text
timestamp
request_id
input_features
predicted_output
heart_disease_probability
```

That directly satisfies Deliverable 5.

---

# PHASE 14 — Drift detection

## 28. Create `src/drift.py`

```bash
cat > src/drift.py <<'EOF'
import json
from pathlib import Path

import pandas as pd
from scipy.stats import (
    chi2_contingency,
    ks_2samp,
)


TRAIN_PATH = Path("artifacts/cleaned_data.csv")
PRODUCTION_PATH = Path("data/generated_100.csv")
REPORT_PATH = Path("reports/drift_report.csv")

CONTINUOUS = [
    "sno",
    "age",
    "trestbps",
    "chol",
    "thalach",
    "oldpeak",
]

CATEGORICAL = [
    "gender",
    "cp",
    "fbs",
    "restecg",
    "exang",
    "slope",
    "ca",
    "thal",
]


def continuous_test(train, prod, feature):
    stat, p = ks_2samp(
        train[feature],
        prod[feature],
    )

    return {
        "feature": feature,
        "test": "Kolmogorov-Smirnov",
        "statistic": float(stat),
        "p_value": float(p),
        "drift_detected": bool(p < 0.05),
        "train_mean": float(train[feature].mean()),
        "incoming_mean": float(prod[feature].mean()),
    }


def categorical_test(train, prod, feature):
    categories = sorted(
        set(train[feature].dropna().unique())
        | set(prod[feature].dropna().unique())
    )

    train_counts = [
        int((train[feature] == category).sum())
        for category in categories
    ]

    prod_counts = [
        int((prod[feature] == category).sum())
        for category in categories
    ]

    table = [
        train_counts,
        prod_counts,
    ]

    stat, p, _, _ = chi2_contingency(table)

    return {
        "feature": feature,
        "test": "Chi-square",
        "statistic": float(stat),
        "p_value": float(p),
        "drift_detected": bool(p < 0.05),
        "train_mean": None,
        "incoming_mean": None,
    }


def main():
    train = pd.read_csv(TRAIN_PATH)
    prod = pd.read_csv(PRODUCTION_PATH)

    results = []

    for feature in CONTINUOUS:
        results.append(
            continuous_test(
                train,
                prod,
                feature,
            )
        )

    for feature in CATEGORICAL:
        results.append(
            categorical_test(
                train,
                prod,
                feature,
            )
        )

    results_df = pd.DataFrame(results)
    results_df.to_csv(REPORT_PATH, index=False)

    summary = {
        "total_features": len(results_df),
        "features_with_drift": results_df.loc[
            results_df["drift_detected"],
            "feature",
        ].tolist(),
        "num_drifted_features": int(
            results_df["drift_detected"].sum()
        ),
        "threshold": "p < 0.05",
    }

    with open(
        "reports/drift_summary.json",
        "w",
    ) as f:
        json.dump(summary, f, indent=4)

    print(results_df.to_string(index=False))

    print("\nSummary:")
    print(json.dumps(summary, indent=4))


if __name__ == "__main__":
    main()
EOF
```

Run:

```bash
python src/drift.py
```

Inspect:

```bash
cat reports/drift_report.csv
cat reports/drift_summary.json
```

Interpretation:

```text
p < 0.05
→ statistically significant evidence of distribution change

p >= 0.05
→ insufficient evidence to declare drift
```

Do **not** say that `p >= 0.05` proves there is no drift.

---

# PHASE 15 — Stress test >2,000 concurrent connections

I recommend doing this from a **Compute Engine load-generator VM**, not Cloud Shell. It remains fully on GCP and gives us control over file-descriptor limits.

## 29. Create load-generator VM

```bash
gcloud compute instances create oppe2-loadgen \
  --zone="$ZONE" \
  --machine-type=e2-standard-4 \
  --image-family=debian-12 \
  --image-project=debian-cloud
```

SSH:

```bash
gcloud compute ssh oppe2-loadgen \
  --zone="$ZONE"
```

Inside VM:

```bash
sudo apt-get update
sudo apt-get install -y wrk
```

Check:

```bash
wrk --version
```

Exit:

```bash
exit
```

---

# 30. Generate wrk script from the 100 rows

Create:

```bash
cat > scripts/create_wrk_payloads.py <<'EOF'
import json

import pandas as pd


df = pd.read_csv("data/generated_100.csv")

payloads = []

for _, row in df.iterrows():
    payload = {
        "sno": int(row["sno"]),
        "age": int(row["age"]),
        "gender": int(row["gender"]),
        "cp": int(row["cp"]),
        "trestbps": float(row["trestbps"]),
        "chol": float(row["chol"]),
        "fbs": int(row["fbs"]),
        "restecg": int(row["restecg"]),
        "thalach": float(row["thalach"]),
        "exang": int(row["exang"]),
        "oldpeak": float(row["oldpeak"]),
        "slope": int(row["slope"]),
        "ca": int(row["ca"]),
        "thal": int(row["thal"]),
    }

    payloads.append(json.dumps(payload))


with open("reports/wrk_payloads.lua", "w") as f:
    f.write('wrk.method = "POST"\\n')
    f.write('wrk.headers["Content-Type"] = "application/json"\\n')
    f.write("local payloads = {\\n")

    for payload in payloads:
        escaped = payload.replace(
            "\\\\",
            "\\\\\\\\",
        ).replace(
            '"',
            '\\"',
        )

        f.write(f'  "{escaped}",\\n')

    f.write("}\\n")
    f.write("local counter = 0\\n")
    f.write("""
request = function()
  counter = counter + 1
  local payload = payloads[((counter - 1) % #payloads) + 1]
  return wrk.format(nil, nil, nil, payload)
end
""")

print("Created reports/wrk_payloads.lua")
EOF
```

Run:

```bash
python scripts/create_wrk_payloads.py
```

---

# 31. Copy wrk script to load generator

```bash
gcloud compute scp \
  reports/wrk_payloads.lua \
  oppe2-loadgen:~/wrk_payloads.lua \
  --zone="$ZONE"
```

---

# 32. Run >2,000 connections

First watch autoscaling in Cloud Shell:

```bash
kubectl get hpa,pods \
  -n heart-disease \
  -w
```

Open another Cloud Shell tab.

Set external IP:

```bash
EXTERNAL_IP=$(kubectl get service heart-disease-api \
  -n heart-disease \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo "$EXTERNAL_IP"
```

Then:

```bash
gcloud compute ssh oppe2-loadgen \
  --zone="$ZONE" \
  --command="ulimit -n 10000 && wrk -t8 -c2200 -d60s --latency -s ~/wrk_payloads.lua http://${EXTERNAL_IP}/predict" \
  | tee reports/wrk_2200_connections.txt
```

This meets:

```text
2200 concurrent connections > 2000
```

Show:

```bash
cat reports/wrk_2200_connections.txt
```

You need to discuss:

```text
Requests/sec       → throughput

Latency average    → normal response time

Latency percentiles
                     → tail latency

Socket errors /
timeouts           → overload/resilience

HPA pod count      → scaling response
```

---

# 33. Observe autoscaler

During or immediately after load:

```bash
kubectl get hpa \
  -n heart-disease
```

```bash
kubectl get pods \
  -n heart-disease \
  -o wide
```

You want to demonstrate that the HPA is configured:

```text
MINPODS = 1
MAXPODS = 3
```

and ideally scales to:

```text
2 or 3 pods
```

depending on CPU pressure.

---

# PHASE 16 — Git commit + trigger CI/CD

Before pushing:

```bash
git status
```

Create `.gitignore`:

```bash
cat > .gitignore <<'EOF'
venv/
__pycache__/
.pytest_cache/
*.pyc
.DS_Store

# Temporary Kubernetes rendered files
deployment-rendered.yaml
EOF
```

Stage:

```bash
git add .
```

Review:

```bash
git status
```

Commit:

```bash
git commit -m "Complete OPPE2 heart disease production MLOps pipeline"
```

Push:

```bash
git push origin main
```

This should trigger:

```text
GitHub Actions
→ train
→ test
→ Docker build
→ Artifact Registry push
→ GKE deployment
```

Then show the successful workflow in your screencast.

---

# Final OPPE2 repo structure

You should end up around:

```text
22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026/
│
├── .github/
│   └── workflows/
│       └── cicd.yml
│
├── artifacts/
│   ├── heart_disease_model.joblib
│   ├── cleaned_data.csv
│   ├── train_split.csv
│   └── test_split.csv
│
├── data/
│   ├── data.csv
│   └── generated_100.csv
│
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── hpa.yaml
│
├── reference/
│   └── HeartDiseaseTrainingAndPrediction.ipynb
│
├── reports/
│   ├── model_metrics.json
│   ├── shap_feature_importance.csv
│   ├── shap_least_impact.json
│   ├── shap_summary.png
│   ├── fairness_by_exact_age.csv
│   ├── fairness_by_age_group.csv
│   ├── fairness_summary.json
│   ├── predictions_100.csv
│   ├── drift_report.csv
│   ├── drift_summary.json
│   ├── wrk_payloads.lua
│   └── wrk_2200_connections.txt
│
├── scripts/
│   └── create_wrk_payloads.py
│
├── src/
│   ├── app.py
│   ├── train.py
│   ├── explain.py
│   ├── fairness.py
│   ├── generate_random_data.py
│   ├── predict_100.py
│   └── drift.py
│
├── tests/
│   └── test_model.py
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── requirements-dev.txt
```

---

# What each deliverable maps to

| Marks                          | Evidence                                                                             |
| ------------------------------ | ------------------------------------------------------------------------------------ |
| Repository                     | Private GitHub repo + accepted collaborator                                          |
| SHAP – 10                      | `shap_summary.png`, `shap_feature_importance.csv`, explain lowest-impact features    |
| Fairlearn – 10                 | `fairness_by_age_group.csv`, `fairness_summary.json`                                 |
| GKE + Docker + CI/CD – 40      | Artifact Registry, GKE Deployment, LoadBalancer, HPA max 3, successful GitHub Action |
| 100 predictions + Logging – 20 | `generated_100.csv`, `predictions_100.csv`, 100 Cloud Logging entries                |
| wrk – 10                       | `-c2200`, latency/throughput/timeouts, pod scaling                                   |
| Drift – 10                     | `drift_report.csv`, training vs generated-data statistical comparison                |

---

# Screencast order

Do **not** show everything randomly. Record it in this order:

1. **Private GitHub repository + collaborator**
2. **Provided notebook → production scripts**
3. **Model metrics**
4. **SHAP plot + least-impact features**
5. **Fairlearn age-group output**
6. **Dockerfile and Artifact Registry image**
7. **GKE deployment**
8. **LoadBalancer API prediction**
9. **HPA showing maximum = 3**
10. **Successful GitHub Actions CI/CD**
11. **100 generated rows**
12. **100 prediction results**
13. **Cloud Logging individual prediction entry**
14. **wrk command with 2,200 concurrent connections**
15. **wrk throughput, latency and timeout results**
16. **HPA/pod scaling during load**
17. **drift report**
18. **Final architecture summary**

One more thing: **do not delete the GKE cluster or load generator until after your screencast and submission are safely complete.** Afterward, we should delete them because GKE and the VM continue incurring charges.

Start with **Phases 1–3 only** now. Once `python src/train.py` succeeds, send me the output from `reports/model_metrics.json`, and we'll validate the model before moving into SHAP/Fairlearn and deployment.

[1]: https://docs.cloud.google.com/kubernetes-engine/docs/concepts/about-logs?authuser=2&utm_source=chatgpt.com "About GKE logs  |  Google Kubernetes Engine (GKE)  |  Google Cloud Documentation"
[2]: https://docs.cloud.google.com/kubernetes-engine/docs/how-to/horizontal-pod-autoscaling?authuser=2&utm_source=chatgpt.com "Configuring horizontal Pod autoscaling  |  Google Kubernetes Engine (GKE)  |  Google Cloud Documentation"
[3]: https://docs.cloud.google.com/artifact-registry/docs/docker/authentication?hl=en&utm_source=chatgpt.com "Authenticate Docker to Artifact Registry  |  Google Cloud Documentation"
[4]: https://docs.cloud.google.com/sdk/gcloud/reference/container/clusters/create?utm_source=chatgpt.com "gcloud container clusters create  |  Google Cloud SDK  |  Google Cloud Documentation"
[5]: https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/bare-metal/docs/how-to/horizontalpodautoscale?utm_source=chatgpt.com "Configure horizontal pod autoscaling  |  Google Distributed Cloud software only for bare metal  |  Google Cloud Documentation"
[6]: https://docs.cloud.google.com/kubernetes-engine/docs/troubleshooting/horizontal-pod-autoscaling?utm_source=chatgpt.com "Troubleshoot horizontal Pod autoscaling  |  Google Kubernetes Engine (GKE)  |  Google Cloud Documentation"
[7]: https://github.com/google-github-actions/setup-gcloud?utm_source=chatgpt.com "GitHub - google-github-actions/setup-gcloud: A GitHub Action for installing and configuring the gcloud CLI. · GitHub"
[8]: https://docs.cloud.google.com/kubernetes-engine/docs/how-to/view-logs?authuser=2&utm_source=chatgpt.com "View GKE logs  |  Google Kubernetes Engine (GKE)  |  Google Cloud Documentation"

---

(venv) srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ python src/train.py
Fitting 5 folds for each of 20 candidates, totalling 100 fits
Traceback (most recent call last):
  File "/home/srujanpatwardhan/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026/src/train.py", line 193, in <module>
    main()
  File "/home/srujanpatwardhan/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026/src/train.py", line 107, in main
    search.fit(X_train, y_train)
  File "/home/srujanpatwardhan/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026/venv/lib/python3.12/site-packages/sklearn/base.py", line 1403, in wrapper
    return fit_method(estimator, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/srujanpatwardhan/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026/venv/lib/python3.12/site-packages/sklearn/model_selection/_search.py", line 1131, in fit
    self._run_search(evaluate_candidates, callback_ctx=root_callback_ctx)
  File "/home/srujanpatwardhan/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026/venv/lib/python3.12/site-packages/sklearn/model_selection/_search.py", line 2121, in _run_search
    evaluate_candidates(candidate_params, callback_ctx=search_ctx)
  File "/home/srujanpatwardhan/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026/venv/lib/python3.12/site-packages/sklearn/model_selection/_search.py", line 1107, in evaluate_candidates
    _warn_or_raise_about_fit_failures(out, self.error_score)
  File "/home/srujanpatwardhan/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026/venv/lib/python3.12/site-packages/sklearn/model_selection/_validation.py", line 478, in _warn_or_raise_about_fit_failures
    raise ValueError(all_fits_failed_message)
ValueError: 
All the 100 fits failed.
It is very likely that your model is misconfigured.
You can try to debug the error by setting error_score='raise'.

Below are more details about the failures:
--------------------------------------------------------------------------------
100 fits failed with the following error:
Traceback (most recent call last):
  File "/home/srujanpatwardhan/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026/venv/lib/python3.12/site-packages/sklearn/model_selection/_validation.py", line 851, in _fit_and_score
    estimator.fit(X_train, y_train, **fit_params)
  File "/home/srujanpatwardhan/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026/venv/lib/python3.12/site-packages/sklearn/base.py", line 1403, in wrapper
    return fit_method(estimator, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/srujanpatwardhan/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026/venv/lib/python3.12/site-packages/sklearn/linear_model/_logistic.py", line 1459, in fit
    X, y = validate_data(
           ^^^^^^^^^^^^^^
  File "/home/srujanpatwardhan/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026/venv/lib/python3.12/site-packages/sklearn/utils/validation.py", line 3055, in validate_data
    X, y = check_X_y(X, y, **check_params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/srujanpatwardhan/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026/venv/lib/python3.12/site-packages/sklearn/utils/validation.py", line 1327, in check_X_y
    X = check_array(
        ^^^^^^^^^^^^
  File "/home/srujanpatwardhan/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026/venv/lib/python3.12/site-packages/sklearn/utils/validation.py", line 1035, in check_array
    array = _asarray_with_order(array, order=order, dtype=dtype, xp=xp)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/srujanpatwardhan/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026/venv/lib/python3.12/site-packages/sklearn/utils/_array_api.py", line 976, in _asarray_with_order
    array = numpy.asarray(array, order=order, dtype=dtype)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/srujanpatwardhan/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026/venv/lib/python3.12/site-packages/pandas/core/generic.py", line 2027, in __array__
    arr = np.asarray(values, dtype=dtype)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ValueError: could not convert string to float: 'female'

(venv) srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ 

---

Yep — this is a straightforward preprocessing bug in the `train.py` I gave you.

The model is receiving the literal string:

```text
female
```

so `gender` was **not encoded to numeric** before Logistic Regression training.

The problem is this check from our script:

```python
if df["gender"].dtype == object:
```

With newer pandas versions, a text column may use a dedicated string dtype rather than `object`, so that condition can be false even though the values are `"male"` / `"female"`. Then the encoding block gets skipped entirely.

Let's fix this properly before moving ahead.

## 1. First confirm the actual dataset values

Run:

```bash
python - <<'PY'
import pandas as pd

df = pd.read_csv("data/data.csv")

print("Columns:")
print(df.columns.tolist())

print("\nGender dtype:")
print(df["gender"].dtype)

print("\nGender values:")
print(df["gender"].value_counts(dropna=False))

print("\nTarget values:")
print(df["target"].value_counts(dropna=False))

print("\nDtypes:")
print(df.dtypes)
PY
```

You will probably see something like:

```text
gender dtype:
str

gender values:
male
female
```

That explains why our `dtype == object` condition failed.

---

# 2. Fix `prepare_data()` properly

Open:

```bash
nano src/train.py
```

Find your entire existing:

```python
def prepare_data():
```

function and replace it with this:

```python
def prepare_data():
    df = pd.read_csv(DATA_PATH)

    # Normalize column names first.
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Normalize gender text irrespective of pandas string/object dtype.
    df["gender"] = (
        df["gender"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    gender_mapping = {
        "male": 0,
        "female": 1,
    }

    unknown_gender = set(df["gender"].dropna().unique()) - set(gender_mapping)

    if unknown_gender:
        raise ValueError(
            f"Unexpected gender values found: {sorted(unknown_gender)}"
        )

    df["gender"] = df["gender"].map(gender_mapping)

    # Convert all model features to numeric.
    for column in FEATURES:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # Normalize target labels.
    df[TARGET] = (
        df[TARGET]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Drop rows that contain missing/invalid values.
    cleaned_df = df.dropna(
        subset=FEATURES + [TARGET]
    ).copy()

    return cleaned_df
```

Save:

```text
Ctrl + O
Enter
Ctrl + X
```

---

# 3. Add a preprocessing sanity check

Before this line in `main()`:

```python
X = df[FEATURES].copy()
```

add:

```python
print("\nPrepared dataset:")
print(df.head())

print("\nFeature dtypes:")
print(df[FEATURES].dtypes)

print("\nGender values after encoding:")
print(df["gender"].value_counts())

print("\nTarget values:")
print(df[TARGET].value_counts())

assert df[FEATURES].select_dtypes(
    exclude=["number"]
).empty, "All model features must be numeric"
```

This is useful because we want the pipeline to **fail early during preprocessing**, rather than discover the problem after launching 100 cross-validation fits.

---

# 4. Run it again

```bash
python src/train.py
```

Before:

```text
Fitting 5 folds...
ValueError: could not convert string to float: 'female'
```

Now you should first see something like:

```text
Feature dtypes:
sno         int64
age         int64
gender      int64
...
```

and:

```text
Gender values after encoding:
0    ...
1    ...
```

Then:

```text
Fitting 5 folds for each of 20 candidates, totalling 100 fits
```

and finally your metrics JSON.

---

# 5. Check outputs

When it succeeds:

```bash
cat reports/model_metrics.json
```

Also:

```bash
ls -lh artifacts
```

We want:

```text
heart_disease_model.joblib
cleaned_data.csv
train_split.csv
test_split.csv
```

---

## 6. One important thing before we continue

Run this too:

```bash
python - <<'PY'
import pandas as pd

df = pd.read_csv("artifacts/cleaned_data.csv")

print("Shape:", df.shape)
print("\nGender:")
print(df["gender"].value_counts())

print("\nTarget:")
print(df["target"].value_counts())

print("\nNull count:")
print(df.isna().sum().sum())

print("\nNon-numeric features:")
features = [
    "sno", "age", "gender", "cp", "trestbps",
    "chol", "fbs", "restecg", "thalach",
    "exang", "oldpeak", "slope", "ca", "thal"
]
print(df[features].select_dtypes(exclude="number").columns.tolist())
PY
```

The final line should be:

```text
[]
```

That tells us **all 14 inputs are numeric**.

### Why this happened

Logistic Regression mathematically expects a numeric feature vector:

```text
X = [x1, x2, ..., x14]
```

It cannot directly process:

```text
gender = "female"
```

so categorical values first need an encoding such as:

```text
male   → 0
female → 1
```

The error occurred before any of the 100 CV fits could actually train, so nothing about the model itself is broken. The preprocessing condition was simply skipping the encoding.

Run the corrected `train.py` and send me the resulting `model_metrics.json`. **Don't move to SHAP yet** — I want to validate the resulting model and class encoding first, because that model artifact will become the basis of everything downstream: SHAP, Fairlearn, FastAPI, Docker, GKE, logging, and drift.

---

everything looks ok, should I continue with the next steps from above?

(venv) srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ python src/train.py
Fitting 5 folds for each of 20 candidates, totalling 100 fits
{
    "accuracy": 0.9830508474576272,
    "precision": 0.9696969696969697,
    "recall": 1.0,
    "f1": 0.9846153846153847,
    "best_params": {
        "solver": "liblinear",
        "C": 206.913808111479
    },
    "train_rows": 234,
    "test_rows": 59,
    "clean_rows": 293,
    "confusion_matrix": [
        [
            26,
            1
        ],
        [
            0,
            32
        ]
    ]
}

Saved model to artifacts/heart_disease_model.joblib
(venv) srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ cat reports/model_metrics.json
{
    "accuracy": 0.9830508474576272,
    "precision": 0.9696969696969697,
    "recall": 1.0,
    "f1": 0.9846153846153847,
    "best_params": {
        "solver": "liblinear",
        "C": 206.913808111479
    },
    "train_rows": 234,
    "test_rows": 59,
    "clean_rows": 293,
    "confusion_matrix": [
        [
            26,
            1
        ],
        [
            0,
            32
        ]
    ]
}(venv) srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ ls -lh artifacts
total 36K
-rw-rw-r-- 1 srujanpatwardhan srujanpatwardhan  14K Sep  6 08:57 cleaned_data.csv
-rw-rw-r-- 1 srujanpatwardhan srujanpatwardhan 1.7K Sep  6 08:57 heart_disease_model.joblib
-rw-rw-r-- 1 srujanpatwardhan srujanpatwardhan 2.9K Sep  6 08:57 test_split.csv
-rw-rw-r-- 1 srujanpatwardhan srujanpatwardhan  12K Sep  6 08:57 train_split.csv
(venv) srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ python - <<'PY'
import pandas as pd

df = pd.read_csv("artifacts/cleaned_data.csv")

print("Shape:", df.shape)
print("\nGender:")
print(df["gender"].value_counts())

print("\nTarget:")
print(df["target"].value_counts())

print("\nNull count:")
print(df.isna().sum().sum())

print("\nNon-numeric features:")
features = [
    "sno", "age", "gender", "cp", "trestbps",
    "chol", "fbs", "restecg", "thalach",
    "exang", "oldpeak", "slope", "ca", "thal"
]
print(df[features].select_dtypes(exclude="number").columns.tolist())
PY
Shape: (293, 15)

Gender:
gender
0    202
1     91
Name: count, dtype: int64

Target:
target
yes    160
no     133
Name: count, dtype: int64

Null count:
0

Non-numeric features:
[]
(venv) srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ 

---

Yes — this looks correct, and you can continue.

Your model matches the supplied notebook very closely:

```text
Accuracy:  98.31%
Precision: 96.97%
Recall:    100%
F1:        98.46%

Train rows: 234
Test rows:   59
Clean rows: 293
```

Your confusion matrix:

```text
             Predicted
             No   Yes
Actual No    26    1
Actual Yes    0   32
```

So on the held-out test set it missed only **1 out of 59 samples**, and importantly it identified all 32 positive heart-disease cases in this split.

The preprocessing checks are also exactly what we wanted:

```text
293 clean rows
0 nulls
gender encoded numerically
all 14 model inputs numeric
model artifact saved successfully
```

So the model artifact is now safe to use as the common basis for SHAP, Fairlearn, API deployment, Docker, GKE, logging and drift analysis.

## Continue with Phase 4 now: SHAP

Use the `src/explain.py` script from the previous instructions, then:

```bash
python src/explain.py
```

After it succeeds:

```bash
cat reports/shap_least_impact.json
cat reports/shap_feature_importance.csv
ls -lh reports/shap_summary.png
```

The most important output for Deliverable 2 is:

```text
reports/shap_least_impact.json
```

because the question specifically asks you to explain the features having the **least impact** on prediction.

Do not invent those features in the video — use whatever SHAP actually reports.

---

## Then Phase 5: Fairlearn

Run:

```bash
python src/fairness.py
```

Then:

```bash
cat reports/fairness_by_age_group.csv
echo ""
cat reports/fairness_summary.json
```

Remember that for this OPPE the marked deliverable specifically says:

```text
Sensitive attribute = age
```

So our fairness analysis is intentionally based on age, not gender.

---

## Then move to the API only after both work

Your next checkpoints should therefore be:

```text
1. train.py       ✅ DONE
2. explain.py     ← next
3. fairness.py
4. app.py / FastAPI
5. Docker
6. Artifact Registry
7. GKE + HPA max 3
8. GitHub Actions CI/CD
9. 100 random predictions
10. Cloud Logging
11. Drift
12. wrk > 2,000 connections
```

One note for the screencast later: mention that `sno` is retained because the provided baseline notebook treats all non-target columns as model features, although in a real clinical production system an observation index would normally be reviewed for removal because it is not a meaningful clinical predictor.

Go ahead with **SHAP and Fairlearn now**. If either script gives an error, send me the output before moving to the API/deployment stage.

---

is there any issue?

(venv) srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ AR_REPO="oppe2-repo"

gcloud artifacts repositories create "$AR_REPO" \
  --repository-format=docker \
  --location="$REGION" \
  --description="OPPE2 Heart Disease API"
Create request issued for: [oppe2-repo]
Waiting for operation [projects/mlops-499806/locations/us-central1/operations/0156a9da-b5ad-4103-91a0-f409c6f187aa] to complete...done.                                 
Created repository [oppe2-repo].
(venv) srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ gcloud auth configure-docker \
  us-central1-docker.pkg.dev
WARNING: Your config file at [/home/srujanpatwardhan/.docker/config.json] contains these credential helper entries:

{
  "credHelpers": {
    "gcr.io": "gcloud",
    "us.gcr.io": "gcloud",
    "eu.gcr.io": "gcloud",
    "asia.gcr.io": "gcloud",
    "staging-k8s.gcr.io": "gcloud",
    "marketplace.gcr.io": "gcloud",
    "africa-south1-docker.pkg.dev": "gcloud",
    "asia-docker.pkg.dev": "gcloud",
    "asia-east1-docker.pkg.dev": "gcloud",
    "asia-east2-docker.pkg.dev": "gcloud",
    "asia-northeast1-docker.pkg.dev": "gcloud",
    "asia-northeast2-docker.pkg.dev": "gcloud",
    "asia-northeast3-docker.pkg.dev": "gcloud",
    "asia-south1-docker.pkg.dev": "gcloud",
    "asia-south2-docker.pkg.dev": "gcloud",
    "asia-southeast1-docker.pkg.dev": "gcloud",
    "asia-southeast2-docker.pkg.dev": "gcloud",
    "asia-southeast3-docker.pkg.dev": "gcloud",
    "australia-southeast1-docker.pkg.dev": "gcloud",
    "australia-southeast2-docker.pkg.dev": "gcloud",
    "docker.africa-south1.rep.pkg.dev": "gcloud",
    "docker.asia-east1.rep.pkg.dev": "gcloud",
    "docker.asia-east2.rep.pkg.dev": "gcloud",
    "docker.asia-northeast1.rep.pkg.dev": "gcloud",
    "docker.asia-northeast2.rep.pkg.dev": "gcloud",
    "docker.asia-northeast3.rep.pkg.dev": "gcloud",
    "docker.asia-south1.rep.pkg.dev": "gcloud",
    "docker.asia-south2.rep.pkg.dev": "gcloud",
    "docker.asia-southeast1.rep.pkg.dev": "gcloud",
    "docker.asia-southeast2.rep.pkg.dev": "gcloud",
    "docker.australia-southeast1.rep.pkg.dev": "gcloud",
    "docker.australia-southeast2.rep.pkg.dev": "gcloud",
    "docker.europe-central2.rep.pkg.dev": "gcloud",
    "docker.europe-north1.rep.pkg.dev": "gcloud",
    "docker.europe-southwest1.rep.pkg.dev": "gcloud",
    "docker.europe-west1.rep.pkg.dev": "gcloud",
    "docker.europe-west10.rep.pkg.dev": "gcloud",
    "docker.europe-west12.rep.pkg.dev": "gcloud",
    "docker.europe-west2.rep.pkg.dev": "gcloud",
    "docker.europe-west3.rep.pkg.dev": "gcloud",
    "docker.europe-west4.rep.pkg.dev": "gcloud",
    "docker.europe-west6.rep.pkg.dev": "gcloud",
    "docker.europe-west8.rep.pkg.dev": "gcloud",
    "docker.europe-west9.rep.pkg.dev": "gcloud",
    "docker.me-central1.rep.pkg.dev": "gcloud",
    "docker.me-central2.rep.pkg.dev": "gcloud",
    "docker.me-west1.rep.pkg.dev": "gcloud",
    "docker.northamerica-northeast1.rep.pkg.dev": "gcloud",
    "docker.northamerica-northeast2.rep.pkg.dev": "gcloud",
    "docker.southamerica-east1.rep.pkg.dev": "gcloud",
    "docker.southamerica-west1.rep.pkg.dev": "gcloud",
    "docker.us-central1.rep.pkg.dev": "gcloud",
    "docker.us-central2.rep.pkg.dev": "gcloud",
    "docker.us-east1.rep.pkg.dev": "gcloud",
    "docker.us-east4.rep.pkg.dev": "gcloud",
    "docker.us-east5.rep.pkg.dev": "gcloud",
    "docker.us-east7.rep.pkg.dev": "gcloud",
    "docker.us-south1.rep.pkg.dev": "gcloud",
    "docker.us-west1.rep.pkg.dev": "gcloud",
    "docker.us-west2.rep.pkg.dev": "gcloud",
    "docker.us-west3.rep.pkg.dev": "gcloud",
    "docker.us-west4.rep.pkg.dev": "gcloud",
    "europe-central2-docker.pkg.dev": "gcloud",
    "europe-docker.pkg.dev": "gcloud",
    "europe-north1-docker.pkg.dev": "gcloud",
    "europe-north2-docker.pkg.dev": "gcloud",
    "europe-southwest1-docker.pkg.dev": "gcloud",
    "europe-west1-docker.pkg.dev": "gcloud",
    "europe-west10-docker.pkg.dev": "gcloud",
    "europe-west12-docker.pkg.dev": "gcloud",
    "europe-west2-docker.pkg.dev": "gcloud",
    "europe-west3-docker.pkg.dev": "gcloud",
    "europe-west4-docker.pkg.dev": "gcloud",
    "europe-west6-docker.pkg.dev": "gcloud",
    "europe-west8-docker.pkg.dev": "gcloud",
    "europe-west9-docker.pkg.dev": "gcloud",
    "me-central1-docker.pkg.dev": "gcloud",
    "me-central2-docker.pkg.dev": "gcloud",
    "me-west1-docker.pkg.dev": "gcloud",
    "northamerica-northeast1-docker.pkg.dev": "gcloud",
    "northamerica-northeast2-docker.pkg.dev": "gcloud",
    "northamerica-south1-docker.pkg.dev": "gcloud",
    "southamerica-east1-docker.pkg.dev": "gcloud",
    "southamerica-west1-docker.pkg.dev": "gcloud",
    "us-central1-docker.pkg.dev": "gcloud",
    "us-central2-docker.pkg.dev": "gcloud",
    "us-docker.pkg.dev": "gcloud",
    "us-east1-docker.pkg.dev": "gcloud",
    "us-east4-docker.pkg.dev": "gcloud",
    "us-east5-docker.pkg.dev": "gcloud",
    "us-east7-docker.pkg.dev": "gcloud",
    "us-south1-docker.pkg.dev": "gcloud",
    "us-west1-docker.pkg.dev": "gcloud",
    "us-west2-docker.pkg.dev": "gcloud",
    "us-west3-docker.pkg.dev": "gcloud",
    "us-west4-docker.pkg.dev": "gcloud",
    "us-west8-docker.pkg.dev": "gcloud"
  }
}
Adding credentials for: us-central1-docker.pkg.dev
gcloud credential helpers already registered correctly.
(venv) srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${AR_REPO}/heart-disease-api"
(venv) srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ docker tag heart-disease-api:local \
  "${IMAGE_URI}:v1"
(venv) srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ docker push "${IMAGE_URI}:v1"
The push refers to repository [us-central1-docker.pkg.dev/mlops-499806/oppe2-repo/heart-disease-api]
842edd81ebb2: Waiting 
44136fa355b3: Waiting 
3678bb828654: Waiting 
6310eb16bf42: Waiting 
db840d086b65: Waiting 
f9efa1b83d06: Waiting 
8f3d3ce43820: Waiting 
3f8adbedd8ef: Waiting 
68c83c930801: Waiting 
c73f3df33f7f: Waiting 
87fe5fa2f5c9: Waiting 
failed to do request: Head "https://us-central1-docker.pkg.dev/v2/mlops-499806/oppe2-repo/heart-disease-api/blobs/sha256:3678bb828654fcc3752f7a5eb63c5accfa00c97047252f25405285550d74a3fd": dial tcp 74.125.68.82:443: connect: connection refused
(venv) srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ 

---

No major issue with your setup. Everything succeeded until the actual network upload.

The important parts are all correct:

```text
Artifact Registry repository created      ✅
Region us-central1                         ✅
Docker credential helper configured        ✅
Image tagged with correct Artifact URI      ✅
Push started                               ✅
```

The failure:

```text
dial tcp 74.125.68.82:443: connect: connection refused
```

is a **network connectivity failure between Cloud Shell/Docker and Artifact Registry**, not an authentication or permissions error.

If credentials were wrong, you would normally see something like `401 Unauthorized`, `403 Forbidden`, or `Permission denied`. Here Docker couldn't even establish the HTTPS connection.

## 1. Just retry first

Your variables should still exist in the current shell:

```bash
echo "$PROJECT_ID"
echo "$REGION"
echo "$AR_REPO"
echo "$IMAGE_URI"
```

You should see approximately:

```text
mlops-499806
us-central1
oppe2-repo
us-central1-docker.pkg.dev/mlops-499806/oppe2-repo/heart-disease-api
```

Now simply retry:

```bash
docker push "${IMAGE_URI}:v1"
```

Docker will reuse layers it already has locally, so you do not need to rebuild.

---

## 2. If it fails again, test Artifact Registry connectivity

Run:

```bash
curl -I https://us-central1-docker.pkg.dev/v2/
```

A response such as:

```text
HTTP/2 401
```

is actually **fine** here. It means the registry is reachable; the bare `curl` request simply isn't authenticated.

What we don't want is:

```text
connection refused
```

or:

```text
could not resolve host
```

---

## 3. Verify the repository exists

```bash
gcloud artifacts repositories describe oppe2-repo \
  --location=us-central1
```

You should see details such as:

```text
format: DOCKER
name: projects/mlops-499806/locations/us-central1/repositories/oppe2-repo
```

So we know the destination is valid.

---

## 4. Re-register Docker authentication

If necessary:

```bash
gcloud auth configure-docker us-central1-docker.pkg.dev --quiet
```

Then:

```bash
docker push "${IMAGE_URI}:v1"
```

---

## 5. Verify your active GCP identity too

```bash
gcloud auth list
```

You should see your account marked:

```text
ACTIVE: *
```

Check project:

```bash
gcloud config get-value project
```

Expected:

```text
mlops-499806
```

---

## 6. If `connection refused` keeps happening

Because this is Cloud Shell, the quickest fix is often to restart the Cloud Shell session.

After reconnecting:

```bash
cd ~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026
source venv/bin/activate

PROJECT_ID="mlops-499806"
REGION="us-central1"
AR_REPO="oppe2-repo"
IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${AR_REPO}/heart-disease-api"
```

Confirm the local image still exists:

```bash
docker images | grep heart-disease
```

If you see:

```text
heart-disease-api   local
```

retag if necessary:

```bash
docker tag heart-disease-api:local "${IMAGE_URI}:v1"
```

Then:

```bash
gcloud auth configure-docker us-central1-docker.pkg.dev --quiet
docker push "${IMAGE_URI}:v1"
```

---

## 7. Fallback if Cloud Shell Docker networking keeps failing

We can let **Cloud Build** build and push the image remotely instead:

```bash
gcloud services enable cloudbuild.googleapis.com
```

Then from the repository root:

```bash
gcloud builds submit \
  --tag "${IMAGE_URI}:v1" \
  .
```

This does:

```text
source code
    ↓
Cloud Build
    ↓
Docker build
    ↓
Artifact Registry
```

So it avoids relying on the local Cloud Shell Docker push connection.

But **don't switch to this yet**. First retry:

```bash
docker push "${IMAGE_URI}:v1"
```

Your current setup looks correct; the error you hit is almost certainly transient connectivity rather than something wrong with the OPPE2 pipeline.

---

is everything ok?

(venv) srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ kubectl get hpa,pods \
  -n heart-disease \
  -w
error: you may only specify a single resource type
(venv) srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ kubectl get hpa,pods   -n heart-disease   -w
error: you may only specify a single resource type
(venv) srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ 

---

Yes — this error by itself is **not a problem with your deployment or HPA**. It is just the way your current `kubectl` invocation handles `-w`: it is rejecting multiple resource types in the same watch command.

Use separate commands instead.

For HPA:

```bash
kubectl get hpa -n heart-disease -w
```

For pods:

```bash
kubectl get pods -n heart-disease -w
```

If you want both on the same screen, use:

```bash
watch -n 2 'kubectl get hpa -n heart-disease; echo; kubectl get pods -n heart-disease -o wide'
```

That is actually better for your stress test/screencast. You should see something like:

```text
NAME                    REFERENCE                      TARGETS   MINPODS   MAXPODS   REPLICAS
heart-disease-api-hpa   Deployment/heart-disease-api  10%/60%  1         3         1
```

and below it:

```text
NAME                                 READY   STATUS    RESTARTS   AGE
heart-disease-api-xxxxxxxxxx-xxxxx   1/1     Running   0          ...
```

Also quickly verify everything:

```bash
kubectl get deployment -n heart-disease
kubectl get pods -n heart-disease
kubectl get service -n heart-disease
kubectl get hpa -n heart-disease
```

And check CPU metrics:

```bash
kubectl top pods -n heart-disease
```

If `kubectl top pods` works and your HPA shows something like:

```text
12%/60%
```

instead of:

```text
<unknown>/60%
```

then autoscaling metrics are working correctly.

For the upcoming `wrk` load test, keep this running in one Cloud Shell tab:

```bash
watch -n 2 'kubectl get hpa -n heart-disease; echo; kubectl get pods -n heart-disease -o wide'
```

Then run the 2200-connection stress test from the other terminal. That will let you visibly demonstrate the replicas increasing toward the configured **maximum of 3 pods**.

---

on a new tab of the shell, I am getting the following error

srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ curl -X POST http://127.0.0.1:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sno": 87,
    "age": 46,
    "gender": 0,
    "cp": 1,
    "trestbps": 101,
    "chol": 197,
    "fbs": 1,
    "restecg": 1,
    "thalach": 156,
    "exang": 0,
    "oldpeak": 0,
    "slope": 2,
    "ca": 0,
    "thal": 3
  }'
srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ EXTERNAL_IP=$(kubectl get service heart-disease-api \
  -n heart-disease \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo "$EXTERNAL_IP"
34.132.175.244
srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ gcloud compute ssh oppe2-loadgen \
  --zone="$ZONE" \
  --command="ulimit -n 10000 && wrk -t8 -c2200 -d60s --latency -s ~/wrk_payloads.lua http://${EXTERNAL_IP}/predict" \
  | tee reports/wrk_2200_connections.txt
ERROR: (gcloud.compute.ssh) could not parse resource []
srujanpatwardhan@cloudshell:~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026 (mlops-499806)$ 

--- 

The main issue is simply that **your new Cloud Shell tab does not have the shell variables from the previous tab**.

This part:

```bash
--zone="$ZONE"
```

is expanding to:

```bash
--zone=""
```

which is why `gcloud` says:

```text
could not parse resource []
```

Your `EXTERNAL_IP` is fine — you successfully got:

```text
34.132.175.244
```

So do this in the new tab:

```bash
cd ~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026

PROJECT_ID="mlops-499806"
REGION="us-central1"
ZONE="us-central1-a"
CLUSTER_NAME="oppe2-heart-cluster"

EXTERNAL_IP=$(kubectl get service heart-disease-api \
  -n heart-disease \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo "PROJECT_ID=$PROJECT_ID"
echo "REGION=$REGION"
echo "ZONE=$ZONE"
echo "EXTERNAL_IP=$EXTERNAL_IP"
```

You should get:

```text
PROJECT_ID=mlops-499806
REGION=us-central1
ZONE=us-central1-a
EXTERNAL_IP=34.132.175.244
```

Then verify the load generator VM exists:

```bash
gcloud compute instances list \
  --filter="name=oppe2-loadgen" \
  --format="table(name,zone,status)"
```

You want something like:

```text
NAME             ZONE           STATUS
oppe2-loadgen    us-central1-a  RUNNING
```

Then run the stress test:

```bash
gcloud compute ssh oppe2-loadgen \
  --zone="$ZONE" \
  --command="ulimit -n 10000 && wrk -t8 -c2200 -d60s --latency -s ~/wrk_payloads.lua http://${EXTERNAL_IP}/predict" \
  | tee reports/wrk_2200_connections.txt
```

### About your localhost `curl`

This:

```bash
curl -X POST http://127.0.0.1:8080/predict ...
```

is only for when you have this running locally in Cloud Shell:

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8080
```

Now that your API is deployed to GKE, test the deployed service instead:

```bash
curl -X POST "http://${EXTERNAL_IP}/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sno": 87,
    "age": 46,
    "gender": 0,
    "cp": 1,
    "trestbps": 101,
    "chol": 197,
    "fbs": 1,
    "restecg": 1,
    "thalach": 156,
    "exang": 0,
    "oldpeak": 0,
    "slope": 2,
    "ca": 0,
    "thal": 3
  }'
```

You should get JSON containing:

```json
{
  "request_id": "...",
  "prediction": "...",
  "heart_disease_probability": ...
}
```

### Make this easier for every new tab

Create one environment file now:

```bash
cat > oppe2.env <<'EOF'
export PROJECT_ID="mlops-499806"
export REGION="us-central1"
export ZONE="us-central1-a"
export CLUSTER_NAME="oppe2-heart-cluster"
export AR_REPO="oppe2-repo"
EOF
```

Then in **every new Cloud Shell tab**, just run:

```bash
cd ~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026
source oppe2.env
```

and refresh the service IP with:

```bash
export EXTERNAL_IP=$(kubectl get service heart-disease-api \
  -n heart-disease \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
```

So yes, your GKE deployment itself appears fine. The immediate error is just an **unset `$ZONE` variable in the new shell tab**.

--- 

how to show the shap image in the google cloud shell terminal?

---

Yes. The easiest way is **not to render it inside the text terminal itself**, but to use Cloud Shell’s browser preview.

From your repo root, run:

```bash
cd ~/22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026

ls -lh reports/shap_summary.png
```

Then serve the `reports` folder:

```bash
python3 -m http.server 8080 --directory reports
```

You should see:

```text
Serving HTTP on 0.0.0.0 port 8080 ...
```

Now in Cloud Shell, click:

**Web Preview → Preview on port 8080**

A page will open listing the report files. Click:

```text
shap_summary.png
```

That is probably the best approach for your screencast.

Alternatively, open the **Cloud Shell Editor**, navigate to:

```text
reports/
└── shap_summary.png
```

and click the image; the editor should preview it directly.

For the video, I recommend:

```text
1. Terminal: show `python src/explain.py`
2. Terminal: show `cat reports/shap_least_impact.json`
3. Browser preview: show `shap_summary.png`
```

That gives you both the numerical SHAP result and the visual explanation.
