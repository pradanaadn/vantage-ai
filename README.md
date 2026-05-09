# Vantage AI

Modular Full-stack Project with Python (FastAPI) and Vue 3 (TypeScript).

## Project Structure

```text
.
├── backend/               # FastAPI Backend
│   ├── app/
│   │   ├── api/          # API Routers
│   │   ├── core/         # Config and Security
│   │   ├── db/           # Database setup
│   │   ├── models/       # SQLAlchemy Models
│   │   ├── schemas/      # Pydantic Schemas
│   │   └── services/     # Business Logic
│   └── pyproject.toml    # uv configuration
├── frontend/              # Vue TypeScript Frontend
│   ├── src/
│   │   ├── components/   # Shared UI components
│   │   ├── modules/      # Feature-based modules (store, services, views)
│   │   ├── services/     # Global services (API)
│   │   └── store/        # Global store
│   └── package.json
└── README.md
```

## Getting Started

### Backend

1. Navigate to `backend/`
2. Install dependencies: `uv sync`
3. Run the server: `uv run uvicorn app.main:app --reload`

### Frontend

1. Navigate to `frontend/`
2. Install dependencies: `npm install`
3. Run dev server: `npm run dev`
