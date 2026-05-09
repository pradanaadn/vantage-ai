# Vantage AI - Architecture & Development Guide

## 1. Project Overview
Vantage AI is a modular full-stack application built with **FastAPI** (Python) and **Vue 3** (TypeScript). It uses **uv** for Python package management and **Vite** for the frontend build pipeline.

## 2. Backend Architecture (FastAPI)
Located in `/backend`, the Python application follows a service-oriented modular pattern:

- `app/api/`: Entry points for requests. Versioned (`v1/`) and split by domain.
- `app/core/`: Global settings (Pydantic), security/auth, and shared constants.
- `app/services/`: Pure business logic and data access abstraction. 
- `app/schemas/`: Pydantic models for data validation and serialization.

*Note: The project is currently database-agnostic. Data access is handled through service classes, allowing for easy integration of SQL, NoSQL, or external APIs.*

## 3. Frontend Architecture (Vue 3 + TypeScript)
Located in `/frontend`, the Vue application uses a feature-based modular structure:

- `src/modules/<feature>/`: Self-contained feature folder containing:
    - `components/`: Feature-specific UI.
    - `services/`: API calls for this feature.
    - `store/`: Pinia state management.
    - `views/`: Page-level components.
- `src/components/`: Shared, generic UI components (Buttons, Inputs).
- `src/services/`: Global services (e.g., Axios instance).
- `src/router/`: Centralized routing logic.

## 4. Development Workflow

### Prerequisites
- Python 3.13+ & [uv](https://github.com/astral-sh/uv)
- Node.js 22+ & npm
- Docker & Docker Compose

### Local Development (Manual)
1. **Backend**: 
   ```bash
   cd backend && uv sync
   uv run uvicorn app.main:app --reload
   ```
2. **Frontend**:
   ```bash
   cd frontend && npm install
   npm run dev
   ```

### Docker Development
```bash
docker-compose up --build
```
- Web: http://localhost
- API Docs: http://localhost/api/v1/docs (via Nginx proxy)
