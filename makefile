
.PHONY: install
install:
	@echo "🚀 INSTALLING ENVIRONMENT..."
	uv sync

.PHONY: lint
lint:
	@echo "🔍 Checking uv.lock file integrity..."
	uv lock --check
	@echo "🔍 Running ruff linter..."
	uv run ruff check src
	@echo "🔍 Running pylint analysis..."
	uv run pylint src
	@echo "🔍 Running mypy type checking..."
	uv run mypy src
	uv pip freeze > requirements.txt
	@echo "🎉 ALL LINTING CHECKS PASSED SUCCESSFULLY!"

.PHONY: fix
fix:
	@echo "🚀 STARTING CODE FORMATTING AND FIXING..."
	uv run ruff format
	uv run ruff check --fix src

.PHONY: clean
clean:
	@echo "🚀 CLEANING PROJECT FILES..."
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	find . | grep -E '(\.mypy_cache|__pycache__|\.pyc|\.pyo$$)' | xargs rm -rf

.PHONY: run
run:
	@echo "🚀 STARTING APPLICATION..."
	@echo "🌐 Starting FastAPI server..."
	PYTHONPATH=./ && uv run src/main.py
