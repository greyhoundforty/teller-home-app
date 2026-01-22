"""
Test sync with mock data.
"""
from src.mock_teller_client import MockTellerClient
from src.models import init_database, get_session
from src.sync_service import SyncService

# Initialize database
print("Initializing database...")
init_database()

# Create mock client and session
print("\nCreating mock Teller client...")
client = MockTellerClient()
session = get_session()

try:
    # Run sync
    print("\nRunning sync with mock data...")
    sync_service = SyncService(client, session)
    result = sync_service.sync_all()
    
    print("\n" + "="*50)
    print("=== Sync Complete ===")
    print("="*50)
    print(f"Accounts synced: {result['accounts']}")
    print(f"Balances synced: {result['balances']}")
    print(f"Transactions synced: {result['transactions']}")
    print("\nDatabase populated with mock data successfully!")
    print("You can now start the Flask application to test the API.")

finally:
    session.close()
