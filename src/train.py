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
