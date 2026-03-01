"""
Service for syncing data from Teller API to the local database.
"""
from datetime import datetime
from typing import List, Dict
from sqlalchemy.orm import Session
from .teller_client import TellerClient
from .models import Account, Balance, Transaction, get_session
import logging
import time

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
    
    def sync_accounts(self) -> List[str]:
        """
        Sync all accounts from Teller to the database.

        Returns:
            List of account IDs synced (used to scope subsequent balance/txn syncs)
        """
        logger.info("Syncing accounts from Teller...")

        try:
            accounts_data = self.teller_client.get_accounts()
            synced_ids = []

            for account_data in accounts_data:
                account = self.db_session.query(Account).filter_by(
                    id=account_data['id']
                ).first()

                if account:
                    account.name = account_data.get('name', 'Unknown')
                    account.type = account_data.get('type', 'unknown')
                    account.subtype = account_data.get('subtype')
                    account.institution_name = account_data.get('institution', {}).get('name')
                    account.currency = account_data.get('currency', 'USD')
                    account.status = account_data.get('status', 'open')
                    account.updated_at = datetime.utcnow()
                else:
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

                synced_ids.append(account_data['id'])

            self.db_session.commit()
            logger.info(f"Synced {len(synced_ids)} accounts: {synced_ids}")
            return synced_ids

        except Exception as e:
            logger.error(f"Error syncing accounts: {str(e)}")
            self.db_session.rollback()
            raise

    def sync_balances(self, account_ids: List[str]) -> int:
        """
        Sync balances for a specific set of account IDs.
        Scoped to the accounts belonging to the current enrollment token.

        Returns:
            Number of balances synced
        """
        logger.info(f"Syncing balances for {len(account_ids)} accounts...")

        try:
            accounts = self.db_session.query(Account).filter(
                Account.id.in_(account_ids)
            ).all()
            count = 0

            for account in accounts:
                time.sleep(1.0)
                try:
                    balance_data = self.teller_client.get_account_balances(account.id)

                    # Teller returns balance values as strings; guard against null
                    available_raw = balance_data.get('available')
                    ledger_raw = balance_data.get('ledger')

                    balance = Balance(
                        account_id=account.id,
                        available=float(available_raw) if available_raw is not None else 0.0,
                        ledger=float(ledger_raw) if ledger_raw is not None else 0.0,
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

    def sync_transactions(self, account_ids: List[str], days: int = 30) -> int:
        """
        Sync transactions for a specific set of account IDs.
        Scoped to the accounts belonging to the current enrollment token.

        Returns:
            Number of new transactions synced
        """
        logger.info(f"Syncing transactions for {len(account_ids)} accounts...")

        try:
            accounts = self.db_session.query(Account).filter(
                Account.id.in_(account_ids)
            ).all()
            count = 0

            for account in accounts:
                time.sleep(1.0)
                try:
                    transactions_data = self.teller_client.get_transactions(
                        account.id,
                        count=100
                    )

                    for txn_data in transactions_data:
                        existing_txn = self.db_session.query(Transaction).filter_by(
                            id=txn_data['id']
                        ).first()

                        if existing_txn:
                            continue

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
        Balance and transaction syncs are scoped to accounts returned by this enrollment's token.

        Returns:
            Dictionary with counts of synced items
        """
        logger.info("Starting full sync from Teller...")

        account_ids = self.sync_accounts()
        result = {
            'accounts': len(account_ids),
            'balances': self.sync_balances(account_ids),
            'transactions': self.sync_transactions(account_ids)
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
