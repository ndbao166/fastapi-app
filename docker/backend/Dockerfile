FROM python:3.12-slim-trixie

# Install make and other build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy uv from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy folder src to docker 
COPY app ./app
COPY config ./config
# Copy uv.lock to docker
COPY uv.lock .
# Copy pyproject.toml to docker
COPY pyproject.toml .
# Copy makefile to docker
COPY makefile .
# Create empty .env file
RUN touch .env

EXPOSE 8080

# Sync the project into a new environment, asserting the lockfile is up to date
RUN uv sync --locked

# Default command
CMD ["sh", "-c", "make lint && make run"]