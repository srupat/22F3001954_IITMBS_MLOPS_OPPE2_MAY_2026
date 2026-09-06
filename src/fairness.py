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
