# File Structure

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
│   ├── wrk_2200_connections.txt
│   ├── hpa_final.txt
│   └── pods_final.txt
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
├── requirements-dev.txt
└── README.md
```

# How to Replicate the Repository

```bash
git clone <YOUR_PRIVATE_GITHUB_REPOSITORY_URL>
cd 22F3001954_IITMBS_MLOPS_OPPE2_MAY_2026
```

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

```bash
python src/train.py
python src/explain.py
python src/fairness.py
pytest tests -v
```

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8080
```

```bash
docker build -t heart-disease-api:local .
```

```bash
PROJECT_ID="mlops-499806"
REGION="us-central1"
ZONE="us-central1-a"
AR_REPO="oppe2-repo"
CLUSTER_NAME="oppe2-heart-cluster"
IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${AR_REPO}/heart-disease-api"
```

```bash
gcloud config set project "$PROJECT_ID"

gcloud services enable \
  container.googleapis.com \
  artifactregistry.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com \
  iamcredentials.googleapis.com \
  sts.googleapis.com
```

```bash
gcloud artifacts repositories create "$AR_REPO" \
  --repository-format=docker \
  --location="$REGION" \
  --description="OPPE2 Heart Disease API"
```

```bash
gcloud auth configure-docker "${REGION}-docker.pkg.dev"
docker tag heart-disease-api:local "${IMAGE_URI}:v1"
docker push "${IMAGE_URI}:v1"
```

```bash
gcloud container clusters create "$CLUSTER_NAME" \
  --zone="$ZONE" \
  --machine-type="e2-standard-2" \
  --num-nodes=1 \
  --enable-ip-alias \
  --release-channel=regular \
  --logging=SYSTEM,WORKLOAD
```

```bash
gcloud container clusters get-credentials "$CLUSTER_NAME" \
  --zone="$ZONE" \
  --project="$PROJECT_ID"
```

```bash
kubectl apply -f k8s/namespace.yaml

sed "s|IMAGE_PLACEHOLDER|${IMAGE_URI}:v1|g" \
  k8s/deployment.yaml \
  | kubectl apply -f -

kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

```bash
kubectl get deployment -n heart-disease
kubectl get pods -n heart-disease
kubectl get service -n heart-disease
kubectl get hpa -n heart-disease
```

```bash
EXTERNAL_IP=$(kubectl get service heart-disease-api \
  -n heart-disease \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo "$EXTERNAL_IP"
```

```bash
curl "http://${EXTERNAL_IP}/healthz"
```

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

```bash
python src/generate_random_data.py
```

```bash
python src/predict_100.py \
  --url "http://${EXTERNAL_IP}"
```

```bash
gcloud logging read \
'resource.type="k8s_container"
AND resource.labels.cluster_name="oppe2-heart-cluster"
AND resource.labels.namespace_name="heart-disease"
AND jsonPayload.event="prediction"' \
--limit=10 \
--format=json
```

```bash
python src/drift.py
```

```bash
python scripts/create_wrk_payloads.py
```

```bash
gcloud compute instances create oppe2-loadgen \
  --zone="$ZONE" \
  --machine-type=e2-standard-4 \
  --image-family=debian-12 \
  --image-project=debian-cloud
```

```bash
gcloud compute ssh oppe2-loadgen \
  --zone="$ZONE" \
  --command="sudo apt-get update && sudo apt-get install -y wrk"
```

```bash
gcloud compute scp \
  reports/wrk_payloads.lua \
  oppe2-loadgen:~/wrk_payloads.lua \
  --zone="$ZONE"
```

```bash
gcloud compute ssh oppe2-loadgen \
  --zone="$ZONE" \
  --command="ulimit -n 10000 && wrk -t8 -c2200 -d60s --latency -s ~/wrk_payloads.lua http://${EXTERNAL_IP}/predict" \
  | tee reports/wrk_2200_connections.txt
```

```bash
kubectl get hpa -n heart-disease | tee reports/hpa_final.txt
kubectl get pods -n heart-disease -o wide | tee reports/pods_final.txt
```

```bash
git add .
git commit -m "Complete OPPE2 heart disease production MLOps pipeline"
git push origin main
```
