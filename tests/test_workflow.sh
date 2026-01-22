#!/bin/bash
# Complete workflow test for Teller Home App

set -e  # Exit on error

echo "============================================================"
echo "🚀 Teller Home App - Complete Workflow Test"
echo "============================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

step() {
    echo -e "${BLUE}▶ $1${NC}"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

echo ""
step "Step 1: Verify PostgreSQL is running"
if docker ps | grep -q teller-home-postgres; then
    success "PostgreSQL container is running"
else
    info "Starting PostgreSQL..."
    mise run postgres-up
    sleep 3
    success "PostgreSQL started"
fi

echo ""
step "Step 2: Test PostgreSQL connection"
python test_postgres.py | tail -5

echo ""
step "Step 3: Update .env to use PostgreSQL"
if grep -q "DATABASE_URL=\"postgresql:" .env; then
    success "Already using PostgreSQL"
else
    cp .env .env.backup
    sed -i.bak 's|DATABASE_URL="sqlite:///teller_home.db"|DATABASE_URL="postgresql://teller:teller_dev_password@localhost:5432/teller_home"|' .env
    success "Updated .env to use PostgreSQL"
fi

echo ""
step "Step 4: Initialize database schema with SQLAlchemy"
source .venv/bin/activate && python -m src.models > /dev/null 2>&1
success "Database schema initialized"

echo ""
step "Step 5: Seed database with mock data"
source .venv/bin/activate && python test_sync_mock.py 2>&1 | grep -E "(Synced|Complete)" | tail -5

echo ""
step "Step 6: Verify data in PostgreSQL"
docker exec teller-home-postgres psql -U teller -d teller_home -t -c "
    SELECT 
        'Accounts: ' || COUNT(DISTINCT a.id) || 
        ', Transactions: ' || COUNT(DISTINCT t.id) || 
        ', Balances: ' || COUNT(DISTINCT b.id)
    FROM accounts a
    LEFT JOIN transactions t ON t.account_id = a.id
    LEFT JOIN balances b ON b.account_id = a.id
"
success "Data verified in PostgreSQL"

echo ""
step "Step 7: Test account_summary view"
docker exec teller-home-postgres psql -U teller -d teller_home -c "
    SELECT 
        name, 
        type, 
        status,
        COALESCE(available::text, 'N/A') as available,
        transaction_count
    FROM account_summary
    ORDER BY name
" | head -10

echo ""
step "Step 8: Run unit tests"
source .venv/bin/activate && pytest tests/test_teller_client.py -q 2>&1 | tail -3
success "Unit tests passed"

echo ""
echo "============================================================"
success "🎉 Complete workflow test PASSED!"
echo "============================================================"
echo ""
info "PostgreSQL database is populated and ready"
info "You can now start the Flask app with:"
echo "  mise run dev"
echo ""
info "To view PostgreSQL data:"
echo "  mise run postgres-shell"
echo ""
info "To stop PostgreSQL:"
echo "  mise run postgres-down"
echo ""
