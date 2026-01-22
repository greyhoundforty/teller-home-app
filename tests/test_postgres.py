"""
Test script to verify PostgreSQL connection and basic operations.
"""
import os
from sqlalchemy import create_engine, text
from src.models import Base, Account, Balance
from datetime import datetime

# Use PostgreSQL
db_url = "postgresql://teller:teller_dev_password@localhost:5432/teller_home"
os.environ['DATABASE_URL'] = db_url

print("="*60)
print("PostgreSQL Connection Test")
print("="*60)
print(f"Database URL: {db_url}")

try:
    # Create engine
    engine = create_engine(db_url)
    
    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"\n✅ Connected to PostgreSQL!")
        print(f"Version: {version[:50]}...")
        
        # Check tables
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result]
        print(f"\n✅ Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {table}")
        
        # Check if any data exists
        result = conn.execute(text("SELECT COUNT(*) FROM accounts"))
        account_count = result.fetchone()[0]
        print(f"\n📊 Data:")
        print(f"   Accounts: {account_count}")
        
        result = conn.execute(text("SELECT COUNT(*) FROM transactions"))
        txn_count = result.fetchone()[0]
        print(f"   Transactions: {txn_count}")
        
        result = conn.execute(text("SELECT COUNT(*) FROM balances"))
        balance_count = result.fetchone()[0]
        print(f"   Balances: {balance_count}")
        
        # Test the view
        result = conn.execute(text("SELECT COUNT(*) FROM account_summary"))
        view_count = result.fetchone()[0]
        print(f"\n✅ account_summary view: {view_count} rows")
        
        # Test trigger
        print(f"\n✅ Triggers configured:")
        result = conn.execute(text("""
            SELECT trigger_name, event_manipulation, event_object_table
            FROM information_schema.triggers
            WHERE trigger_schema = 'public'
        """))
        for trigger_name, event, table in result:
            print(f"   - {trigger_name} on {table} ({event})")
    
    print("\n" + "="*60)
    print("✅ PostgreSQL is fully configured and ready!")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print("\nMake sure PostgreSQL is running:")
    print("  mise run postgres-up")
