#!/usr/bin/env python3
"""
Scheduled Transaction Sync Service
Syncs transactions from Teller API for all active enrollments.
Run this script twice daily via cron or systemd timer.
"""
import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models import init_database, get_session, UserEnrollment
from src.teller_client import TellerClient
from src.sync_service import SyncService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduled_sync.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def sync_all_enrollments():
    """Sync transactions for all active enrollments."""
    logger.info("=" * 60)
    logger.info("Starting scheduled transaction sync")
    logger.info("=" * 60)
    
    # Initialize database
    init_database()
    session = get_session()
    
    try:
        # Get all active enrollments
        enrollments = session.query(UserEnrollment).filter_by(is_active=True).all()
        
        if not enrollments:
            logger.warning("No active enrollments found. Nothing to sync.")
            return
        
        logger.info(f"Found {len(enrollments)} active enrollment(s)")
        
        total_synced = {
            'accounts': 0,
            'balances': 0,
            'transactions': 0
        }
        
        successful_syncs = 0
        failed_syncs = 0
        
        # Sync each enrollment
        for enrollment in enrollments:
            try:
                logger.info(f"\nSyncing enrollment: {enrollment.enrollment_id}")
                logger.info(f"  Institution: {enrollment.institution_name or 'Unknown'}")
                logger.info(f"  User ID: {enrollment.user_id}")
                
                # Create client with enrollment's access token
                client = TellerClient(app_token=enrollment.access_token)
                sync_service = SyncService(client, session)
                
                # Perform sync
                result = sync_service.sync_all()
                
                # Update last_synced timestamp
                enrollment.last_synced = datetime.utcnow()
                session.commit()
                
                # Accumulate results
                total_synced['accounts'] += result['accounts']
                total_synced['balances'] += result['balances']
                total_synced['transactions'] += result['transactions']
                
                successful_syncs += 1
                
                logger.info(f"  ✓ Synced successfully:")
                logger.info(f"    - Accounts: {result['accounts']}")
                logger.info(f"    - Balances: {result['balances']}")
                logger.info(f"    - Transactions: {result['transactions']}")
                
            except Exception as e:
                failed_syncs += 1
                logger.error(f"  ✗ Failed to sync enrollment {enrollment.enrollment_id}: {str(e)}")
                session.rollback()
                continue
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("Sync Summary")
        logger.info("=" * 60)
        logger.info(f"Successful syncs: {successful_syncs}/{len(enrollments)}")
        logger.info(f"Failed syncs: {failed_syncs}/{len(enrollments)}")
        logger.info(f"\nTotal synced:")
        logger.info(f"  - Accounts: {total_synced['accounts']}")
        logger.info(f"  - Balances: {total_synced['balances']}")
        logger.info(f"  - Transactions: {total_synced['transactions']}")
        logger.info("=" * 60)
        
        return successful_syncs > 0
        
    except Exception as e:
        logger.error(f"Fatal error during sync: {str(e)}")
        return False
        
    finally:
        session.close()


if __name__ == "__main__":
    try:
        success = sync_all_enrollments()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

# Made with Bob
