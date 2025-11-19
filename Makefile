.PHONY: help install install-dev test test-verbose test-coverage clean lint format type-check run

help:
	@echo "AI Assistant Einstein - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install production dependencies"
	@echo "  make install-dev    Install development dependencies (includes testing)"
	@echo ""
	@echo "Testing:"
	@echo "  make test           Run all tests"
	@echo "  make test-verbose   Run tests with verbose output"
	@echo "  make test-coverage  Run tests with coverage report"
	@echo "  make test-unit      Run only unit tests"
	@echo "  make test-integration Run only integration tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint           Run flake8 linter"
	@echo "  make format         Format code with black"
	@echo "  make type-check     Run mypy type checker"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          Remove test artifacts and cache files"
	@echo ""
	@echo "Run:"
	@echo "  make run            Run the application"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

test:
	pytest

test-verbose:
	pytest -v

test-coverage:
	pytest --cov=. --cov-report=html --cov-report=term-missing

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

lint:
	flake8 main.py tests/ --max-line-length=100

format:
	black main.py tests/

type-check:
	mypy main.py --ignore-missing-imports

clean:
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf __pycache__/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

run:
	python main.py
