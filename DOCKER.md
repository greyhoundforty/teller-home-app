# Docker Setup Guide

This guide explains how to run the Teller Home App using Docker.

## Prerequisites

- Docker installed and running
- Docker Compose installed
- `.env` file configured with your Teller credentials

## Environment Setup

Before running Docker, ensure you have a `.env` file in the project root:

```bash
cp .env.example .env
```

Fill in the required variables:

```env
TELLER_APP_ID=your_app_id
TELLER_APP_TOKEN=your_app_token
SECRET_KEY=your_secret_key
```

## Building the Image

The Teller Home App has optimizations for older Docker versions that may have buildx compatibility issues.

### Option 1: Using Mise (Recommended)

```bash
mise run docker-build
```

### Option 2: Using Docker CLI Directly

```bash
DOCKER_BUILDKIT=0 docker build -t teller-home-app:latest .
```

The `DOCKER_BUILDKIT=0` flag disables buildx, ensuring compatibility with Docker versions older than 0.17.

## Running with Docker Compose

### Start All Services

```bash
mise run docker-up
# or
DOCKER_BUILDKIT=0 docker-compose up -d
```

This will start:
- **PostgreSQL** database on port 5432
- **Flask app** on port 5001

### View Logs

```bash
mise run docker-logs
# or
docker-compose logs -f
```

### Stop Services

```bash
mise run docker-down
# or
docker-compose down
```

## Accessing the Application

Once running:

- **Web App**: http://localhost:5001
- **Database**: postgresql://teller:teller_dev_password@localhost:5432/teller_home

## Troubleshooting

### Build Error: "compose build requires buildx 0.17 or later"

This is a Docker Compose v5 compatibility issue. Use the provided `docker-build` mise task or run:

```bash
DOCKER_BUILDKIT=0 docker build -t teller-home-app:latest .
```

### Container Won't Start

Check the logs:

```bash
docker-compose logs app
docker-compose logs postgres
```

Common issues:
- PostgreSQL not ready: Wait 10-15 seconds for postgres to initialize
- Port 5001 already in use: Change port in docker-compose.yml
- Missing environment variables: Check `.env` file

### Database Connection Issues

```bash
# Connect to PostgreSQL directly
docker-compose exec postgres psql -U teller -d teller_home

# Or use the mise shortcut
mise run docker-shell-postgres
```

### Shell Access to App Container

```bash
mise run docker-shell-app
# or
docker-compose exec app /bin/bash
```

## Architecture

### Dockerfile

- **Base**: Python 3.12 slim image
- **Non-root user**: Runs as `appuser` for security
- **Health check**: TCP connection check on port 5001
- **Workers**: 2 Gunicorn workers (configurable)

### docker-compose.yml

- **postgres**: PostgreSQL 15 Alpine with persistent volume
- **app**: Flask app via Gunicorn, depends on postgres health check
- **Network**: Internal bridge network for service communication
- **Restart policy**: Services automatically restart on failure

## Performance Tuning

### Adjust Worker Count

In `docker-compose.yml`, modify the command:

```yaml
command: ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "4"]
```

Increase `--workers` for more concurrent requests (use 2 × CPU cores as a starting point).

### Database Optimization

Add environment variables to PostgreSQL service for production:

```yaml
postgres:
  environment:
    POSTGRES_INITDB_ARGS: "-c shared_buffers=256MB -c max_connections=200"
```

## Production Deployment

For production use:

1. Use a proper reverse proxy (nginx, traefik)
2. Configure SSL/TLS certificates
3. Use strong SECRET_KEY
4. Switch to PostgreSQL for production database (not SQLite)
5. Use multiple Gunicorn workers
6. Set up monitoring and logging
7. Use proper secrets management (not .env files)

## Useful Commands

```bash
# Rebuild without cache
DOCKER_BUILDKIT=0 docker build --no-cache -t teller-home-app:latest .

# Check image layers
docker history teller-home-app:latest

# Inspect image
docker inspect teller-home-app:latest

# Remove unused images
docker image prune

# Clean up stopped containers
docker container prune

# View resource usage
docker stats
```

## Notes

- Volume mounts for `src/` and `static/` allow live code updates (useful for development)
- PostgreSQL data persists in the `postgres_data` volume
- The app automatically waits for PostgreSQL to be healthy before starting
- All logs are written to stdout for easy monitoring
