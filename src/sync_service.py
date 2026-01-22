"""
Service for syncing data from Teller API to the local database.
"""
from datetime import datetime
from typing import List, Dict
from sqlalchemy.orm import Session
from .teller_client import TellerClient
from .models import Account, Balance, Transaction, get_session
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SyncService:
    """Service for synchronizing Teller data to the database."""
    
    def __init__(self, teller_client: TellerClient, db_session: Session):
        """
        Initialize the sync service.
        
        Args:
            teller_client: Teller API client instance
            db_session: SQLAlchemy database session
        """
        self.teller_client = teller_client
        self.db_session = db_session
    
    def sync_accounts(self) -> int:
        """
        Sync all accounts from Teller to the database.
        
        Returns:
            Number of accounts synced
        """
        logger.info("Syncing accounts from Teller...")
        
        try:
            accounts_data = self.teller_client.get_accounts()
            count = 0
            
            for account_data in accounts_data:
                account = self.db_session.query(Account).filter_by(
                    id=account_data['id']
                ).first()
                
                if account:
                    # Update existing account
                    account.name = account_data.get('name', 'Unknown')
                    account.type = account_data.get('type', 'unknown')
                    account.subtype = account_data.get('subtype')
                    account.institution_name = account_data.get('institution', {}).get('name')
                    account.currency = account_data.get('currency', 'USD')
                    account.status = account_data.get('status', 'open')
                    account.updated_at = datetime.utcnow()
                else:
                    # Create new account
                    account = Account(
                        id=account_data['id'],
                        name=account_data.get('name', 'Unknown'),
                        type=account_data.get('type', 'unknown'),
                        subtype=account_data.get('subtype'),
                        institution_name=account_data.get('institution', {}).get('name'),
                        currency=account_data.get('currency', 'USD'),
                        status=account_data.get('status', 'open')
                    )
                    self.db_session.add(account)
                
                count += 1
            
            self.db_session.commit()
            logger.info(f"Synced {count} accounts")
            return count
        
        except Exception as e:
            logger.error(f"Error syncing accounts: {str(e)}")
            self.db_session.rollback()
            raise
    
    def sync_balances(self) -> int:
        """
        Sync balances for all accounts.
        
        Returns:
            Number of balances synced
        """
        logger.info("Syncing balances from Teller...")
        
        try:
            accounts = self.db_session.query(Account).all()
            count = 0
            
            for account in accounts:
                try:
                    balance_data = self.teller_client.get_account_balances(account.id)
                    
                    balance = Balance(
                        account_id=account.id,
                        available=float(balance_data.get('available', 0)),
                        ledger=float(balance_data.get('ledger', 0)),
                        timestamp=datetime.utcnow()
                    )
                    
                    self.db_session.add(balance)
                    count += 1
                
                except Exception as e:
                    logger.warning(f"Could not sync balance for account {account.id}: {str(e)}")
            
            self.db_session.commit()
            logger.info(f"Synced {count} balances")
            return count
        
        except Exception as e:
            logger.error(f"Error syncing balances: {str(e)}")
            self.db_session.rollback()
            raise
    
    def sync_transactions(self, days: int = 30) -> int:
        """
        Sync transactions for all accounts.
        
        Args:
            days: Number of days of transactions to fetch
            
        Returns:
            Number of transactions synced
        """
        logger.info(f"Syncing transactions from Teller (last {days} days)...")
        
        try:
            accounts = self.db_session.query(Account).all()
            count = 0
            
            for account in accounts:
                try:
                    transactions_data = self.teller_client.get_transactions(
                        account.id,
                        count=500
                    )
                    
                    for txn_data in transactions_data:
                        # Check if transaction already exists
                        existing_txn = self.db_session.query(Transaction).filter_by(
                            id=txn_data['id']
                        ).first()
                        
                        if existing_txn:
                            continue
                        
                        # Parse date
                        date_str = txn_data.get('date')
                        txn_date = datetime.fromisoformat(date_str.replace('Z', '+00:00')) if date_str else datetime.utcnow()
                        
                        transaction = Transaction(
                            id=txn_data['id'],
                            account_id=account.id,
                            amount=float(txn_data.get('amount', 0)),
                            date=txn_date,
                            description=txn_data.get('description', 'Unknown'),
                            category=txn_data.get('category'),
                            type=txn_data.get('type'),
                            status=txn_data.get('status', 'posted')
                        )
                        
                        self.db_session.add(transaction)
                        count += 1
                
                except Exception as e:
                    logger.warning(f"Could not sync transactions for account {account.id}: {str(e)}")
            
            self.db_session.commit()
            logger.info(f"Synced {count} new transactions")
            return count
        
        except Exception as e:
            logger.error(f"Error syncing transactions: {str(e)}")
            self.db_session.rollback()
            raise
    
    def sync_all(self) -> Dict[str, int]:
        """
        Sync all data from Teller (accounts, balances, and transactions).
        
        Returns:
            Dictionary with counts of synced items
        """
        logger.info("Starting full sync from Teller...")
        
        result = {
            'accounts': self.sync_accounts(),
            'balances': self.sync_balances(),
            'transactions': self.sync_transactions()
        }
        
        logger.info(f"Full sync complete: {result}")
        return result


def run_sync():
    """Run a full sync operation."""
    from .models import init_database
    
    # Initialize database
    init_database()
    
    # Create client and session
    client = TellerClient()
    session = get_session()
    
    try:
        # Run sync
        sync_service = SyncService(client, session)
        result = sync_service.sync_all()
        
        print("\n=== Sync Complete ===")
        print(f"Accounts synced: {result['accounts']}")
        print(f"Balances synced: {result['balances']}")
        print(f"Transactions synced: {result['transactions']}")
    
    finally:
        session.close()


if __name__ == "__main__":
    run_sync()
