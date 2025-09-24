
.PHONY: install
install:
	@echo "================================================================================================"
	@echo "🚀 INSTALLING ENVIRONMENT..."
	@echo "📦 Syncing dependencies with uv..."
	uv sync
	@echo "✅ Environment successfully installed!"
	@echo "================================================================================================"

.PHONY: lint
lint:
	@echo "================================================================================================"
	@echo "🚀 STARTING LINTING PROCESS..."
	@echo "================================================================================================"
	@echo "🔍 Checking uv.lock file integrity..."
	uv lock --check
	@echo "✅ uv.lock file is up to date!"
	@echo "================================================================================================"
	@echo "🔍 Running ruff linter..."
	uv run ruff check src
	@echo "✅ Ruff linting completed successfully!"
	@echo "================================================================================================"
	@echo "🔍 Running pylint analysis..."
	uv run pylint src
	@echo "✅ Pylint analysis completed successfully!"
	@echo "================================================================================================"
	@echo "🔍 Running mypy type checking..."
	uv run mypy src
	@echo "✅ Mypy type checking completed successfully!"
	@echo "================================================================================================"
	@echo "📝 Generating requirements.txt..."
	uv pip freeze > requirements.txt
	@echo "✅ Requirements.txt generated successfully!"
	@echo "================================================================================================"
	@echo "🎉 ALL LINTING CHECKS PASSED SUCCESSFULLY!"
	@echo "================================================================================================"

.PHONY: fix
fix:
	@echo "================================================================================================"
	@echo "🚀 STARTING CODE FORMATTING AND FIXING..."
	@echo "================================================================================================"
	@echo "🛠️  Running ruff formatter..."
	uv run ruff format
	@echo "🛠️  Running ruff auto-fix..."
	uv run ruff check --fix src
	@echo "✅ Code formatting and fixing completed successfully!"
	@echo "================================================================================================"

.PHONY: clean
clean:
	@echo "================================================================================================"
	@echo "🚀 CLEANING PROJECT FILES..."
	@echo "🧹 Removing Python cache files..."
	find . -type f -name "*.py[co]" -delete
	@echo "🧹 Removing __pycache__ directories..."
	find . -type d -name "__pycache__" -delete
	@echo "🧹 Removing mypy cache and other artifacts..."
	find . | grep -E '(\.mypy_cache|__pycache__|\.pyc|\.pyo$$)' | xargs rm -rf
	@echo "🧹 Clearing terminal..."
	clear
	@echo "✅ Project cleanup completed successfully!"
	@echo "================================================================================================"

.PHONY: run
run:
	@echo "🚀 STARTING APPLICATION..."
	@echo "🌐 Starting FastAPI server..."
	PYTHONPATH=./ && uv run src/main.py

.PHONY: build_docker
build_docker:
	@echo "================================================================================================"
	@echo "🚀 BUILDING DOCKER IMAGE..."
	docker build -f docker/backend/Dockerfile -t fastapi-app:latest .
	@echo "✅ Docker image built successfully!"
	@echo "================================================================================================"

.PHONY: run_docker
run_docker:
	@echo "================================================================================================"
	@echo "🚀 STARTING DOCKER CONTAINER..."
	docker run -d -p 8000:8000 --env-file .env --name fastapi-app fastapi-app:latest
	@echo "================================================================================================"

.PHONY: clean_docker
clean_docker:
	@echo "================================================================================================"
	@echo "🚀 CLEANING DOCKER RESOURCES..."
	@echo "🛑 Stopping Docker container 'fastapi-app'..."
	@echo "🗑️  Removing Docker container 'fastapi-app'..."
	@echo "🗑️  Removing Docker image 'fastapi-app:latest'..."
	docker stop fastapi-app && docker rm fastapi-app && docker rmi fastapi-app:latest
	@echo "✅ Docker resources cleaned successfully!"
	@echo "🧹 All Docker artifacts removed!"
	@echo "================================================================================================"

.PHONY: full
full:
	@echo "================================================================================================"
	@echo "🚀 RUNNING FULL PIPELINE..."
	@echo "📋 Steps: lint → build_docker → run_docker"
	@echo "================================================================================================"
	make lint
	make build_docker
	make run_docker
	@echo "================================================================================================"
	@echo "🎉 FULL PIPELINE COMPLETED SUCCESSFULLY!"
	@echo "================================================================================================"