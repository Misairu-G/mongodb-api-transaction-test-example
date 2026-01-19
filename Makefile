.PHONY: help clean up stop clean rebuild test test-id-factory test-id-connector

.DEFAULT_GOAL := help

help:  ## Show this help message
	@echo "Available targets:"

	# Works by searching for 'target: ## description' pattern in this Makefile
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

up:  ## Start all services with docker compose
	docker compose up -d --build

upfront:  ## Start all services in the foreground
	docker compose up --build

stop:  ## Stop all services
	docker compose down

clean:  ## Stop services, remove volumes, images, and Python artifacts
	docker compose down -v --rmi 'local' --remove-orphans

	@echo "Removing Python artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +

rebuild: clean up  ## Clean and rebuild everything

test:  ## Run all tests
	pytest -v
