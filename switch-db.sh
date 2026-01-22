#!/bin/bash
# Helper script to switch between SQLite and PostgreSQL

set -e

if [ "$1" == "postgres" ] || [ "$1" == "pg" ]; then
    echo "🔄 Switching to PostgreSQL..."
    
    # Check if PostgreSQL is running
    if ! docker ps | grep -q teller-home-postgres; then
        echo "📦 Starting PostgreSQL..."
        mise run postgres-up
        sleep 3
    fi
    
    # Update .env
    sed -i.bak 's|DATABASE_URL="sqlite:///teller_home.db"|DATABASE_URL="postgresql://teller:teller_dev_password@localhost:5432/teller_home"|' .env
    sed -i.bak 's|# DATABASE_URL="postgresql:|DATABASE_URL="postgresql:|' .env
    
    echo "✅ Switched to PostgreSQL"
    echo "📊 Database URL: postgresql://teller:teller_dev_password@localhost:5432/teller_home"
    echo ""
    echo "To populate with data:"
    echo "  source .venv/bin/activate && python test_sync_mock.py"
    
elif [ "$1" == "sqlite" ] || [ "$1" == "sq" ]; then
    echo "🔄 Switching to SQLite..."
    
    # Update .env
    sed -i.bak 's|DATABASE_URL="postgresql:|# DATABASE_URL="postgresql:|' .env
    sed -i.bak 's|# DATABASE_URL="sqlite:///teller_home.db"|DATABASE_URL="sqlite:///teller_home.db"|' .env
    
    echo "✅ Switched to SQLite"
    echo "📊 Database URL: sqlite:///teller_home.db"
    echo ""
    echo "To populate with data:"
    echo "  mise run db-seed"
    
else
    echo "Usage: $0 [postgres|pg|sqlite|sq]"
    echo ""
    echo "Examples:"
    echo "  $0 postgres    # Switch to PostgreSQL"
    echo "  $0 pg          # Switch to PostgreSQL (short)"
    echo "  $0 sqlite      # Switch to SQLite"
    echo "  $0 sq          # Switch to SQLite (short)"
    exit 1
fi
