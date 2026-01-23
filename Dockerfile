FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY src/ ./src/
COPY static/ ./static/
COPY authentication/ ./authentication/

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5001

# Health check (simple port check)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import socket; socket.create_connection(('localhost', 5001), timeout=2)" || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "--worker-class", "sync", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
