"""
Teller API Client for connecting to Teller Connect and fetching financial data.
"""
import os
import time
import logging
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()


class TellerClient:
    """Client for interacting with the Teller API."""
    
    BASE_URL = "https://api.teller.io"
    
    def __init__(self, app_token: Optional[str] = None, cert_path: Optional[str] = None, key_path: Optional[str] = None):
        """
        Initialize the Teller client.
        
        Args:
            app_token: Teller API token. If not provided, will use TELLER_APP_TOKEN from env.
            cert_path: Path to certificate file. Defaults to authentication/certificate.pem
            key_path: Path to private key file. Defaults to authentication/private_key.pem
        """
        self.app_token = app_token or os.getenv("TELLER_APP_TOKEN")
        if not self.app_token:
            raise ValueError("TELLER_APP_TOKEN must be set in environment or passed to constructor")
        
        # Set up certificate paths — env vars take precedence, then constructor args, then defaults
        default_root = os.path.dirname(os.path.dirname(__file__))
        if cert_path is None:
            cert_path = os.getenv("TELLER_CERT_PATH") or os.path.join(default_root, "authentication", "certificate.pem")
        if key_path is None:
            key_path = os.getenv("TELLER_KEY_PATH") or os.path.join(default_root, "authentication", "private_key.pem")

        self.session = requests.Session()
        # Teller uses Basic Auth with access token as username, empty password
        self.session.auth = (self.app_token, "")
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "TellerHomeApp/1.0"
        })

        # Add mTLS certificate if available (required for development + production environments)
        if os.path.exists(cert_path) and os.path.exists(key_path):
            self.session.cert = (cert_path, key_path)
            print(f"Using certificate authentication from {cert_path}")
        else:
            print(f"Warning: Certificate files not found at {cert_path} and {key_path}. "
                  f"Set TELLER_CERT_PATH / TELLER_KEY_PATH env vars or place certs in authentication/")
    
    def _get(self, endpoint: str, params: Optional[Dict] = None, max_retries: int = 3) -> Dict:
        """
        Make a GET request to the Teller API with exponential backoff on 429.

        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters
            max_retries: Maximum number of retry attempts on rate limit

        Returns:
            JSON response as dictionary
        """
        url = f"{self.BASE_URL}{endpoint}"
        for attempt in range(max_retries):
            response = self.session.get(url, params=params)
            if response.status_code == 429:
                # Honour Retry-After if present, otherwise use exponential backoff
                retry_after = int(response.headers.get("Retry-After", 2 ** (attempt + 1)))
                logger.warning(
                    f"Rate limited on {endpoint}, waiting {retry_after}s "
                    f"(attempt {attempt + 1}/{max_retries})"
                )
                time.sleep(retry_after)
                continue
            response.raise_for_status()
            return response.json()
        # Final attempt after exhausting retries
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_accounts(self) -> List[Dict]:
        """
        Fetch all accounts linked to the application.
        
        Returns:
            List of account dictionaries
        """
        return self._get("/accounts")
    
    def get_account(self, account_id: str) -> Dict:
        """
        Fetch a specific account by ID.
        
        Args:
            account_id: The Teller account ID
            
        Returns:
            Account dictionary
        """
        return self._get(f"/accounts/{account_id}")
    
    def get_account_balances(self, account_id: str) -> Dict:
        """
        Fetch balance information for a specific account.
        
        Args:
            account_id: The Teller account ID
            
        Returns:
            Balance dictionary with available and ledger amounts
        """
        return self._get(f"/accounts/{account_id}/balances")
    
    def get_transactions(self, account_id: str, count: int = 100) -> List[Dict]:
        """
        Fetch transactions for a specific account.
        
        Args:
            account_id: The Teller account ID
            count: Number of transactions to fetch (default 100)
            
        Returns:
            List of transaction dictionaries
        """
        params = {"count": count}
        return self._get(f"/accounts/{account_id}/transactions", params=params)
    
    def get_account_details(self, account_id: str) -> Dict:
        """
        Fetch detailed information about an account.
        
        Args:
            account_id: The Teller account ID
            
        Returns:
            Account details dictionary
        """
        return self._get(f"/accounts/{account_id}/details")
    
    def test_connection(self) -> bool:
        """
        Test the connection to Teller API.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            self.get_accounts()
            return True
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False


def main():
    """Test the Teller client connection."""
    print("Testing Teller API connection...")
    
    try:
        client = TellerClient()
        
        # Test connection
        if client.test_connection():
            print("✓ Connection successful!")
        else:
            print("✗ Connection failed!")
            return
        
        # Fetch accounts
        print("\nFetching accounts...")
        accounts = client.get_accounts()
        print(f"Found {len(accounts)} account(s)")
        
        for account in accounts:
            print(f"\nAccount: {account.get('name', 'Unknown')}")
            print(f"  ID: {account.get('id')}")
            print(f"  Type: {account.get('type')}")
            print(f"  Subtype: {account.get('subtype')}")
            print(f"  Institution: {account.get('institution', {}).get('name', 'Unknown')}")
            
            # Get balance
            try:
                balances = client.get_account_balances(account['id'])
                print(f"  Available: ${balances.get('available', 0)}")
                print(f"  Ledger: ${balances.get('ledger', 0)}")
            except Exception as e:
                print(f"  Could not fetch balances: {str(e)}")
            
            # Get recent transactions
            try:
                transactions = client.get_transactions(account['id'], count=5)
                print(f"  Recent transactions: {len(transactions)}")
                for txn in transactions[:3]:
                    print(f"    - {txn.get('date')}: {txn.get('description')} (${txn.get('amount')})")
            except Exception as e:
                print(f"  Could not fetch transactions: {str(e)}")
    
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
