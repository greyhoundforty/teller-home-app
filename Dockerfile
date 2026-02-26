# ── Stage 1: dependency builder ───────────────────────────────────────────────
FROM python:3.12-slim AS builder

# Pull uv from the official distroless image (no extra bloat)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# uv tuning for Docker builds:
#   COMPILE_BYTECODE  – bake .pyc files at install time → faster cold start
#   LINK_MODE=copy    – copy files rather than hardlinks (required cross-layer)
#   PYTHON_DOWNLOADS  – never let uv fetch its own Python; use the base image's
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Create the virtualenv explicitly so its path is predictable
RUN uv venv /app/.venv

# Install deps into the venv.
# requirements-production.txt is the lean set (SQLite, no psycopg2/plotly/dev tools).
# Copying only the requirements file here maximises Docker layer cache reuse —
# the install layer is only invalidated when requirements change.
COPY requirements-production.txt .
RUN uv pip install --python /app/.venv -r requirements-production.txt


# ── Stage 2: final runtime image ──────────────────────────────────────────────
FROM python:3.12-slim AS final

WORKDIR /app

# Copy only the pre-built virtualenv — uv itself is NOT included in this stage
COPY --from=builder /app/.venv /app/.venv

# Prepend venv to PATH so all python/gunicorn invocations use it
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Application source
COPY app.py .
COPY src/ ./src/
COPY static/ ./static/
COPY init_db.sql .
COPY migrations/ ./migrations/

# Authentication certs are bind-mounted at runtime on Proxmox;
# create the directory so the mount point exists and has correct ownership.
RUN mkdir -p /app/authentication

# Non-root user for least-privilege execution
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# SQLite data directory — declare as a volume so the DB survives container restarts.
# Mount a host path or named volume here when running on Proxmox.
VOLUME ["/app/data"]

EXPOSE 5001

# Hit the real health endpoint so gunicorn must be fully up and the DB reachable
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD python -c \
        "import urllib.request; urllib.request.urlopen('http://localhost:5001/api/health', timeout=5)" \
        || exit 1

# 2 sync workers is fine for a single-user household app;
# increase if you add async workloads later
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5001", \
     "--workers", "2", \
     "--worker-class", "sync", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "app:app"]
