.PHONY: help install test lint format clean run-api run-examples docker-build docker-up docker-down

help:
	@echo "RiskSense Development Commands"
	@echo "=============================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install         Install dependencies"
	@echo "  make dev-install     Install dev dependencies (pytest, etc)"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test            Run test suite"
	@echo "  make test-verbose    Run tests with verbose output"
	@echo "  make test-coverage   Run tests with coverage report"
	@echo "  make lint            Run Python linting (flake8)"
	@echo "  make format          Format code (black)"
	@echo ""
	@echo "Development:"
	@echo "  make run-api         Run Flask API locally (port 5000)"
	@echo "  make run-cli         Run CLI tool (type 'risksense --help')"
	@echo "  make examples        Run example scripts"
	@echo "  make visualize       Generate fuzzy set visualizations"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build    Build Docker image"
	@echo "  make docker-up       Start containers (docker-compose)"
	@echo "  make docker-down     Stop containers"
	@echo "  make docker-logs     View container logs"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean           Remove __pycache__, .pyc, dist files"
	@echo "  make clean-docker    Remove Docker images & volumes"
	@echo ""

install:
	pip install --break-system-packages -r requirements.txt
	@echo "✓ Dependencies installed"

dev-install: install
	pip install --break-system-packages pytest pytest-cov matplotlib flask gunicorn
	@echo "✓ Dev dependencies installed"

test:
	python -m pytest tests/test_model.py -v

test-verbose:
	python -m pytest tests/test_model.py -vv -s

test-coverage:
	python -m pytest tests/test_model.py --cov=risksense --cov-report=html --cov-report=term
	@echo "✓ Coverage report: htmlcov/index.html"

lint:
	python -m flake8 risksense/ tests/ --max-line-length=88 --extend-ignore=E203,W503

format:
	python -m black risksense/ tests/ examples/ --line-length=88

run-api:
	python -c "from risksense.api import create_app; app = create_app(); app.run(host='0.0.0.0', port=5000, debug=True)"

run-cli:
	python -m risksense.cli --help

examples:
	python examples/01_individual_scoring.py
	python examples/02_batch_portfolio_analysis.py

visualize:
	python -c "from risksense.visualization import plot_membership_functions; \
	           plot_membership_functions('income', 'visuals/income_membership.png'); \
	           plot_membership_functions('dti', 'visuals/dti_membership.png'); \
	           plot_membership_functions('credit', 'visuals/credit_membership.png'); \
	           plot_membership_functions('stability', 'visuals/stability_membership.png'); \
	           print('✓ Visualizations saved to visuals/')"

docker-build:
	docker build -t risksense:latest .
	@echo "✓ Docker image built: risksense:latest"

docker-up:
	docker-compose up -d
	@echo "✓ Containers started"
	@echo "  API:      http://localhost:5000"
	@echo "  Prometheus: http://localhost:9090 (optional)"
	@echo "  Grafana:  http://localhost:3000 (optional)"

docker-down:
	docker-compose down
	@echo "✓ Containers stopped"

docker-logs:
	docker-compose logs -f risksense-api

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/
	@echo "✓ Cleaned up"

clean-docker:
	docker-compose down -v
	docker rmi risksense:latest
	@echo "✓ Docker cleaned up"

.DEFAULT_GOAL := help
