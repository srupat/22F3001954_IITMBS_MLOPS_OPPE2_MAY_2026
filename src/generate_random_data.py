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
