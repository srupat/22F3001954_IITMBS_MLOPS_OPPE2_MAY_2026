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
