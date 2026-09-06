import json
from pathlib import Path

import pandas as pd


INPUT_PATH = Path("data/generated_100.csv")
OUTPUT_PATH = Path("reports/wrk_payloads.lua")


def main():
    df = pd.read_csv(INPUT_PATH)

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

    with OUTPUT_PATH.open("w") as f:
        f.write('wrk.method = "POST"\n')
        f.write('wrk.headers["Content-Type"] = "application/json"\n')
        f.write("\n")
        f.write("local payloads = {\n")

        # Lua long strings avoid complicated JSON quote escaping.
        for payload in payloads:
            f.write(f"  [=[{payload}]=],\n")

        f.write("}\n")
        f.write("\n")
        f.write("local counter = 0\n")
        f.write("\n")
        f.write("request = function()\n")
        f.write("  counter = counter + 1\n")
        f.write("  local index = ((counter - 1) % #payloads) + 1\n")
        f.write("  local payload = payloads[index]\n")
        f.write('  return wrk.format("POST", nil, nil, payload)\n')
        f.write("end\n")

    print(f"Created {OUTPUT_PATH}")
    print(f"Payload count: {len(payloads)}")


if __name__ == "__main__":
    main()
