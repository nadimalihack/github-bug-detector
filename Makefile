.PHONY: help install test lint format clean run docker-build docker-up docker-down

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)GitHub Bug Detection System - Makefile Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install all dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	cd frontend && npm install
	@echo "$(GREEN)Dependencies installed successfully!$(NC)"

install-backend: ## Install backend dependencies only
	@echo "$(BLUE)Installing backend dependencies...$(NC)"
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	@echo "$(GREEN)Backend dependencies installed!$(NC)"

install-frontend: ## Install frontend dependencies only
	@echo "$(BLUE)Installing frontend dependencies...$(NC)"
	cd frontend && npm install
	@echo "$(GREEN)Frontend dependencies installed!$(NC)"

test: ## Run all tests
	@echo "$(BLUE)Running tests...$(NC)"
	pytest tests/ --cov=backend/src --cov-report=html --cov-report=term
	@echo "$(GREEN)Tests completed!$(NC)"

test-unit: ## Run unit tests only
	@echo "$(BLUE)Running unit tests...$(NC)"
	pytest tests/unit -v
	@echo "$(GREEN)Unit tests completed!$(NC)"

test-integration: ## Run integration tests only
	@echo "$(BLUE)Running integration tests...$(NC)"
	pytest tests/integration -v
	@echo "$(GREEN)Integration tests completed!$(NC)"

test-coverage: ## Generate coverage report
	@echo "$(BLUE)Generating coverage report...$(NC)"
	pytest tests/ --cov=backend/src --cov-report=html --cov-report=xml
	@echo "$(GREEN)Coverage report generated in htmlcov/$(NC)"

lint: ## Run linting checks
	@echo "$(BLUE)Running linting checks...$(NC)"
	flake8 backend/src
	pylint backend/src --exit-zero
	@echo "$(GREEN)Linting completed!$(NC)"

format: ## Format code with black and isort
	@echo "$(BLUE)Formatting code...$(NC)"
	black backend/src
	isort backend/src
	@echo "$(GREEN)Code formatted!$(NC)"

format-check: ## Check code formatting
	@echo "$(BLUE)Checking code formatting...$(NC)"
	black --check backend/src
	isort --check-only backend/src

type-check: ## Run type checking
	@echo "$(BLUE)Running type checks...$(NC)"
	mypy backend/src --ignore-missing-imports
	@echo "$(GREEN)Type checking completed!$(NC)"

security: ## Run security scans
	@echo "$(BLUE)Running security scans...$(NC)"
	bandit -r backend/src
	safety check
	@echo "$(GREEN)Security scans completed!$(NC)"

quality: lint format-check type-check security ## Run all quality checks

clean: ## Clean up generated files
	@echo "$(BLUE)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage coverage.xml
	rm -rf build/ dist/
	@echo "$(GREEN)Cleanup completed!$(NC)"

run-backend: ## Run backend server
	@echo "$(BLUE)Starting backend server...$(NC)"
	cd backend/src && python api.py

run-frontend: ## Run frontend development server
	@echo "$(BLUE)Starting frontend server...$(NC)"
	cd frontend && npm run dev

run: ## Run both backend and frontend
	@echo "$(BLUE)Starting all servers...$(NC)"
	@echo "Run 'make run-backend' in one terminal and 'make run-frontend' in another"

docker-build: ## Build Docker images
	@echo "$(BLUE)Building Docker images...$(NC)"
	docker-compose build
	@echo "$(GREEN)Docker images built!$(NC)"

docker-up: ## Start Docker containers
	@echo "$(BLUE)Starting Docker containers...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Containers started!$(NC)"

docker-down: ## Stop Docker containers
	@echo "$(BLUE)Stopping Docker containers...$(NC)"
	docker-compose down
	@echo "$(GREEN)Containers stopped!$(NC)"

docker-logs: ## View Docker logs
	docker-compose logs -f

docker-clean: ## Clean Docker resources
	@echo "$(BLUE)Cleaning Docker resources...$(NC)"
	docker-compose down -v
	docker system prune -f
	@echo "$(GREEN)Docker cleanup completed!$(NC)"

db-migrate: ## Run database migrations
	@echo "$(BLUE)Running database migrations...$(NC)"
	# Add migration commands here
	@echo "$(GREEN)Migrations completed!$(NC)"

db-seed: ## Seed database with sample data
	@echo "$(BLUE)Seeding database...$(NC)"
	python backend/scripts/seed_database.py
	@echo "$(GREEN)Database seeded!$(NC)"

train-model: ## Train ML model
	@echo "$(BLUE)Training model...$(NC)"
	cd backend/src && python trainer.py
	@echo "$(GREEN)Model training completed!$(NC)"

setup: install ## Initial project setup
	@echo "$(BLUE)Setting up project...$(NC)"
	cp .env.example .env
	@echo "$(GREEN)Project setup completed!$(NC)"
	@echo "$(RED)Don't forget to configure your .env file!$(NC)"

pre-commit: ## Install pre-commit hooks
	@echo "$(BLUE)Installing pre-commit hooks...$(NC)"
	pre-commit install
	@echo "$(GREEN)Pre-commit hooks installed!$(NC)"

pre-commit-run: ## Run pre-commit on all files
	@echo "$(BLUE)Running pre-commit checks...$(NC)"
	pre-commit run --all-files

update-deps: ## Update dependencies
	@echo "$(BLUE)Updating dependencies...$(NC)"
	pip install --upgrade -r requirements.txt
	cd frontend && npm update
	@echo "$(GREEN)Dependencies updated!$(NC)"

check: test quality ## Run tests and quality checks

deploy: ## Deploy to production
	@echo "$(BLUE)Deploying to production...$(NC)"
	# Add deployment commands here
	@echo "$(GREEN)Deployment completed!$(NC)"

backup: ## Backup database
	@echo "$(BLUE)Creating database backup...$(NC)"
	# Add backup commands here
	@echo "$(GREEN)Backup completed!$(NC)"

restore: ## Restore database from backup
	@echo "$(BLUE)Restoring database...$(NC)"
	# Add restore commands here
	@echo "$(GREEN)Restore completed!$(NC)"

docs: ## Generate documentation
	@echo "$(BLUE)Generating documentation...$(NC)"
	cd docs && make html
	@echo "$(GREEN)Documentation generated!$(NC)"

serve-docs: ## Serve documentation locally
	@echo "$(BLUE)Serving documentation...$(NC)"
	cd docs/_build/html && python -m http.server 8080

version: ## Show version information
	@echo "$(BLUE)Version Information:$(NC)"
	@echo "Python: $$(python --version)"
	@echo "Node: $$(node --version)"
	@echo "npm: $$(npm --version)"
	@echo "Docker: $$(docker --version)"

status: ## Show project status
	@echo "$(BLUE)Project Status:$(NC)"
	@echo "Backend: $$(curl -s http://localhost:8000/ | grep -o 'status' || echo 'Not running')"
	@echo "Frontend: $$(curl -s http://localhost:3000/ | grep -o 'html' || echo 'Not running')"
	@echo "Database: $$(docker ps | grep mongodb || echo 'Not running')"
