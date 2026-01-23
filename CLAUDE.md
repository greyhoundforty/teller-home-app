# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Teller Home App** is a Flask-based financial management application that connects to real bank accounts via the Teller API. It provides:
- Real-time balance tracking across multiple accounts
- Transaction history
- Bill payment scheduling with weekly forecasts
- Calendar visualization of payments and projected balances

**Tech Stack**: Python 3.12, Flask, SQLAlchemy, SQLite/PostgreSQL, Vanilla JS frontend

## Essential Commands

All commands use `mise` as the task runner. Run `mise task ls` to see all available tasks.

### Development Workflow
```bash
mise run dev              # Start Flask dev server with auto-reload (port 5001)
mise run test             # Run pytest test suite
mise run test-cov         # Run tests with coverage report (htmlcov/)
mise run lint             # Check code formatting (black, isort, flake8)
mise run format           # Auto-format code with black and isort
```

### Database Management
```bash
mise run db-init          # Initialize SQLite database schema
mise run db-seed          # Populate with mock data for testing
mise run db-reset         # Drop, recreate, and seed database

# PostgreSQL (Docker)
mise run postgres-up      # Start PostgreSQL container
mise run postgres-shell   # Open psql shell
mise run postgres-down    # Stop PostgreSQL container
```

### Docker Deployment
```bash
mise run docker-build     # Build image (with DOCKER_BUILDKIT=0 for compatibility)
mise run docker-up        # Start app + postgres services
mise run docker-logs      # View container logs
mise run docker-down      # Stop all services
```

### Database Switching
```bash
./switch-db.sh postgres   # Switch to PostgreSQL in .env
./switch-db.sh sqlite     # Switch to SQLite in .env
```

## Architecture

### Core Components

1. **app.py** - Main Flask application with API endpoints and static file serving
   - API routes: `/api/health`, `/api/accounts`, `/api/sync`, `/api/scheduled-payments`, `/api/weekly-forecast`
   - Static routes: Serves HTML/CSS/JS from `static/` directory
   - Teller Connect routes: `/api/teller-connect/enroll`, `/api/teller-connect/status`

2. **src/models.py** - SQLAlchemy ORM models
   - `Account` - Bank/credit accounts with optional custom display names
   - `Balance` - Time-series balance history
   - `Transaction` - Transaction records
   - `ScheduledPayment` - Bill payment schedules (recurring or one-time)
   - `UserEnrollment` - Teller access tokens per user enrollment

3. **src/teller_client.py** - Teller API client
   - Uses Basic Auth with `TELLER_APP_TOKEN` as username
   - Certificate-based authentication (`authentication/certificate.pem` + `private_key.pem`)
   - Methods: `get_accounts()`, `get_account()`, `get_balances()`, `get_transactions()`

4. **src/sync_service.py** - Data synchronization service
   - Syncs accounts, balances, and transactions from Teller to local database
   - Implements upsert logic (create or update records)
   - Per-enrollment syncing: Each user enrollment has isolated data

### Database Schema

**SQLite (development)**: `teller_home.db` - Single file database
**PostgreSQL (production)**: Configured via `docker-compose.yml` with persistent volume

Key relationships:
- `Account` has many `Balance` records (time-series)
- `Account` has many `Transaction` records
- `ScheduledPayment` optionally links to `Account` (for account-specific payments)
- `UserEnrollment` stores Teller access tokens with metadata

View: `account_summary` - Materialized view joining accounts with latest balance

### Frontend Structure

**Static files** in `static/`:
- `index.html` - Landing page with navigation
- `dashboard.html` - Account cards/list view with balances
- `calendar.html` - Monthly calendar with payment scheduling
- `teller-connect.html` - Bank account linking UI (Teller Connect modal)

**API Integration**: Vanilla JavaScript using fetch API, no framework dependencies

## Teller API Integration

### Authentication Modes

1. **Application Token** (`TELLER_APP_TOKEN`): For app-level operations
2. **User Enrollment Tokens**: Per-user access tokens obtained via Teller Connect OAuth-like flow
3. **Certificate Authentication**: `authentication/certificate.pem` + `private_key.pem` (required for production)

### Teller Connect Flow

1. User clicks "Connect Bank" → Opens Teller Connect modal (`TellerConnect.setup()` in frontend)
2. User selects bank and authenticates securely with Teller
3. Teller returns `access_token` and `enrollment_id`
4. Frontend POSTs to `/api/teller-connect/enroll` to save enrollment
5. Backend stores token in `UserEnrollment` table
6. Subsequent API calls use enrollment token to fetch user-specific data

**Environments**:
- `sandbox` - Test environment with fake bank credentials
- `production` - Real bank connections (requires valid Teller app credentials)

## Testing

### Test Suite Structure

- `test_teller_client.py` - Teller API client unit tests
- `test_sync_mock.py` - Sync service with mock data
- `test_api.py` - API endpoint integration tests (requires running server)
- `test_enrollment.py` - Teller Connect enrollment flow tests
- `test_postgres.py` - PostgreSQL connection tests

### Running Tests

```bash
# Full suite
mise run test

# With coverage
mise run test-cov
open htmlcov/index.html

# Single test file
source .venv/bin/activate && pytest tests/test_teller_client.py -v

# Single test function
source .venv/bin/activate && pytest tests/test_api.py::test_health_endpoint -v
```

## Environment Configuration

Required environment variables in `.env`:

```env
TELLER_APP_ID=app_xxx           # Teller application ID
TELLER_APP_TOKEN=test_xxx       # Teller API token
DATABASE_URL=sqlite:///...      # Database connection string
SECRET_KEY=xxx                  # Flask session secret
FLASK_ENV=development           # development or production
```

**Database URLs**:
- SQLite: `sqlite:///teller_home.db` (relative path)
- PostgreSQL: `postgresql://user:password@host:port/dbname`

## Docker Architecture

### Containers

1. **postgres** - PostgreSQL 15 Alpine
   - Port: 5432
   - User: `teller` / Password: `teller_dev_password`
   - Volume: `postgres_data` (persistent)
   - Health check: `pg_isready`

2. **app** - Flask application via Gunicorn
   - Port: 5001
   - Workers: 2 (configurable)
   - Depends on postgres health check
   - Volume mounts for live development: `src/`, `static/`, `authentication/`

### Build Compatibility

**Important**: This project disables Docker BuildKit (`DOCKER_BUILDKIT=0`) for compatibility with older Docker versions (<0.17). Always use `mise run docker-build` or set the environment variable manually.

## Common Development Patterns

### Adding a New API Endpoint

1. Add route in `app.py`:
   ```python
   @app.route('/api/my-endpoint')
   def my_endpoint():
       return jsonify({"data": "value"})
   ```

2. Update API documentation in `/api/info` endpoint

3. Add integration test in `tests/test_api.py`

### Adding a Database Model

1. Define model in `src/models.py` inheriting from `Base`
2. Add relationships to existing models if needed
3. Run `mise run db-reset` to recreate schema with new table
4. Update `src/sync_service.py` if syncing from Teller

### Syncing Data from Teller

The `SyncService` class handles all Teller API → Database synchronization:

```python
from src.teller_client import TellerClient
from src.sync_service import SyncService
from src.models import get_session

client = TellerClient()
session = get_session()
sync = SyncService(client, session)

sync.sync_accounts()      # Sync accounts
sync.sync_balances()      # Sync balances
sync.sync_transactions()  # Sync transactions
```

**Per-enrollment syncing**: Pass `enrollment_token` to `TellerClient` to sync specific user data.

## Troubleshooting

### "Port 5001 already in use"
```bash
lsof -ti :5001 | xargs kill -9
mise run dev
```

### "Database is locked"
SQLite file is locked by another process:
```bash
mise run backup-restart   # Backup and restart
# or
mise run db-reset         # Reset database
```

### PostgreSQL connection fails
```bash
mise run postgres-down
docker system prune -f
mise run postgres-up
# Wait 10-15 seconds for initialization
```

### Teller API 401 Unauthorized
- Check `TELLER_APP_TOKEN` in `.env`
- Verify certificate files exist: `authentication/certificate.pem` and `authentication/private_key.pem`
- Check token validity: `mise run auth-test`

### Docker build fails with "compose build requires buildx 0.17 or later"
Use `mise run docker-build` which sets `DOCKER_BUILDKIT=0`, or:
```bash
DOCKER_BUILDKIT=0 docker build -t teller-home-app:latest .
```

## Code Quality Standards

**Linting**: Black (formatter), isort (import sorting), flake8 (linter)
**Type Checking**: mypy (optional, run with `mise run typecheck`)

Before committing:
```bash
mise run format && mise run lint && mise run test
```

## Additional Documentation

- `README.md` - User-facing project overview
- `DOCKER.md` - Comprehensive Docker setup and troubleshooting
- `.agent-docs/QUICK_REFERENCE.md` - Quick command reference
- `.agent-docs/TELLER_CONNECT_GUIDE.md` - Teller Connect implementation guide
- `.agent-docs/DASHBOARD_CALENDAR_GUIDE.md` - API endpoints and frontend integration
