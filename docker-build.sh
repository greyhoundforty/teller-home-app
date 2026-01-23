#!/bin/bash
# Helper script to build Docker image with proper settings

set -e

echo "🐳 Building Teller Home App Docker image..."

# Method 1: Try using docker build directly (most compatible)
if command -v docker &> /dev/null; then
    echo "Using docker build (most compatible)..."
    docker build -t teller-home-app:latest .
    echo "✅ Docker image built successfully"
    exit 0
fi

# If docker build is not available, try docker-compose with legacy builder
echo "⚠️  Attempting docker-compose build..."
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=1
docker-compose build --no-cache app

echo "✅ Build complete"
