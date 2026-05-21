.PHONY: run test lint format clean help

# Variables
APP_MODULE = app.main:app
PORT = 8000
HOST = 0.0.0.0

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

run: ## Run the FastAPI application in development mode
	uv run uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT) --reload

test: ## Run all tests using uv
	uv run pytest

test-v: ## Run all tests with verbose output
	uv run pytest -v

lint: ## Run linting checks
	uv run ruff check .

format: ## Format code using ruff
	uv run ruff format .

clean: ## Clean up temporary files and caches
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

install: ## Install dependencies using uv
	uv sync
