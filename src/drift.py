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
