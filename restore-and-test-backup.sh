#!/bin/bash
# Restore SQLite backup and test locally
# Usage: ./restore-and-test-backup.sh teller_home.db.backup.before_xlsx_test

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <backup_file>"
    echo ""
    echo "Available backups:"
    ls -lh teller_home.db.backup* 2>/dev/null || echo "  No backups found"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "🔍 Testing SQLite backup: $BACKUP_FILE"
echo ""

# 1. Create safety backup of current SQLite file
if [ -f "teller_home.db" ]; then
    echo "💾 Backing up current teller_home.db..."
    cp teller_home.db "teller_home.db.backup.$(date +%Y%m%d_%H%M%S)"
fi

# 2. Restore the backup file
echo "📦 Restoring backup to teller_home.db..."
cp "$BACKUP_FILE" teller_home.db

# 3. Update schema to add missing columns (skip if already exist)
echo "🔧 Updating schema with missing columns (if needed)..."
sqlite3 teller_home.db <<'EOF' 2>/dev/null || true
-- Try to add missing columns (will fail silently if already exist)
ALTER TABLE accounts ADD COLUMN display_name TEXT;
EOF

sqlite3 teller_home.db <<'EOF' 2>/dev/null || true
ALTER TABLE scheduled_payments ADD COLUMN is_recurring BOOLEAN DEFAULT 1;
EOF

sqlite3 teller_home.db <<'EOF' 2>/dev/null || true
ALTER TABLE scheduled_payments ADD COLUMN frequency TEXT DEFAULT 'monthly';
EOF

sqlite3 teller_home.db <<'EOF' 2>/dev/null || true
ALTER TABLE scheduled_payments ADD COLUMN email TEXT;
EOF

echo "✅ Schema update complete"

echo ""
echo "✅ Backup restored and schema updated!"
echo ""
echo "📊 Database info:"
sqlite3 teller_home.db "SELECT COUNT(*) || ' accounts' FROM accounts; SELECT COUNT(*) || ' scheduled_payments' FROM scheduled_payments;"

echo ""
echo "🚀 Next steps:"
echo "  1. Switch to SQLite: ./switch-db.sh sqlite"
echo "  2. Start Flask app: mise run dev"
echo "  3. Visit: http://localhost:5001"
echo ""
echo "⚠️  To switch back to PostgreSQL later: ./switch-db.sh postgres"
