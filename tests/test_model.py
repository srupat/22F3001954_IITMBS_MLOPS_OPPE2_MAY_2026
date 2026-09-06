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
