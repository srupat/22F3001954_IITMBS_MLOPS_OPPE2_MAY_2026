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
