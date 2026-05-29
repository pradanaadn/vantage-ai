# Deployment (Cloud Run + GitHub Actions)

This guide documents how to set up Workload Identity Federation (WIF) and GitHub Actions secrets for Cloud Run deployments.

## Prerequisites

- Project ID: fourth-elixir-495806-e4
- GitHub repo: pradanaadn/vantage-ai
- gcloud authenticated with a project owner account

## 1) Enable required APIs

```bash
gcloud config set project fourth-elixir-495806-e4
gcloud services enable iamcredentials.googleapis.com iam.googleapis.com cloudresourcemanager.googleapis.com
```

## 2) Create a service account

```bash
gcloud iam service-accounts create gha-cloudrun \
  --display-name "GitHub Actions Cloud Run"
```

## 3) Grant roles to the service account

```bash
gcloud projects add-iam-policy-binding fourth-elixir-495806-e4 \
  --member "serviceAccount:gha-cloudrun@fourth-elixir-495806-e4.iam.gserviceaccount.com" \
  --role "roles/run.admin"

gcloud projects add-iam-policy-binding fourth-elixir-495806-e4 \
  --member "serviceAccount:gha-cloudrun@fourth-elixir-495806-e4.iam.gserviceaccount.com" \
  --role "roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding fourth-elixir-495806-e4 \
  --member "serviceAccount:gha-cloudrun@fourth-elixir-495806-e4.iam.gserviceaccount.com" \
  --role "roles/iam.serviceAccountUser"
```

## 4) Create Workload Identity Pool + Provider

```bash
gcloud iam workload-identity-pools create "github-pool" \
  --location="global" \
  --display-name="GitHub Actions Pool"

gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --display-name="GitHub Actions Provider" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --attribute-condition="attribute.repository=='pradanaadn/vantage-ai'"
```

## 5) Allow GitHub to impersonate the service account

```bash
PROJECT_NUMBER=$(gcloud projects describe fourth-elixir-495806-e4 --format='value(projectNumber)')

gcloud iam service-accounts add-iam-policy-binding \
  "gha-cloudrun@fourth-elixir-495806-e4.iam.gserviceaccount.com" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/github-pool/attribute.repository/pradanaadn/vantage-ai"
```

## 6) Get values for GitHub secrets

```bash
# GCP_WIF_PROVIDER
gcloud iam workload-identity-pools providers describe github-provider \
  --location=global \
  --workload-identity-pool=github-pool \
  --format="value(name)"

# GCP_SERVICE_ACCOUNT
# gha-cloudrun@fourth-elixir-495806-e4.iam.gserviceaccount.com
```

## 7) Add GitHub Actions secrets

Go to **Settings -> Secrets and variables -> Actions** and add:

- `GCP_WIF_PROVIDER`
- `GCP_SERVICE_ACCOUNT`
- `VITE_API_URL` (backend URL + `/api/v1`)

## 8) Cloud Run resource limits (free-tier friendly)

```bash
# Backend
gcloud run services update vantage-ai-backend \
  --region asia-southeast2 \
  --min-instances 0 \
  --max-instances 1 \
  --concurrency 5 \
  --cpu 1 \
  --memory 512Mi \
  --timeout 60

# Frontend
gcloud run services update vantage-ai-ui \
  --region asia-southeast2 \
  --min-instances 0 \
  --max-instances 1 \
  --concurrency 5 \
  --cpu 1 \
  --memory 256Mi \
  --timeout 60
```

## 9) Trigger deployments

Push to `main` to trigger the GitHub Actions workflows:

- `deploy-backend.yml`
- `deploy-frontend.yml`
