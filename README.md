# 🚀 Vantage AI

Modular Full-stack Template: **FastAPI** + **Vue 3 (TS)** + **uv** + **Docker**.

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/Vue-3.0-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com/)

## 📖 Documentation

- [Architecture Guide](./docs/ARCHITECTURE.md) - Deep dive into project structure and patterns.
- [API Documentation](http://localhost:8000/docs) - Swagger UI (when backend is running).

## 🛠 Project Structure

```text
.
├── backend/               # FastAPI + uv
│   ├── app/
│   │   ├── api/          # Versioned routers (v1)
│   │   ├── services/     # Business logic layer
│   │   └── core/         # Global config & settings
├── frontend/              # Vue 3 + Vite + TypeScript
│   ├── src/
│   │   ├── modules/      # Feature-based architecture
│   │   └── services/     # Global API client
├── nginx.conf             # Reverse proxy & SPA config
└── docker-compose.yml     # Orchestration
```

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
docker-compose up --build
```

Visit [http://localhost](http://localhost).

### Manual Setup

Refer to the [Architecture Guide](./docs/ARCHITECTURE.md#development-workflow) for step-by-step local installation.

## 🔐 GitHub Actions Secrets (Cloud Run)

For CI/CD deployments, add these secrets in your GitHub repo:

Required:

- `GCP_WIF_PROVIDER`: Workload Identity Provider resource name
- `GCP_SERVICE_ACCOUNT`: Service account email used by GitHub Actions

Frontend build:

- `VITE_API_URL`: Backend URL + `/api/v1`

Steps:

1. Go to **Settings → Secrets and variables → Actions**.
2. Click **New repository secret**.
3. Add each secret name/value above.

If you want to set up Workload Identity Federation (recommended), ask the project owner to run the WIF setup steps and provide the `GCP_WIF_PROVIDER` value.

## ⚖️ License

MIT
