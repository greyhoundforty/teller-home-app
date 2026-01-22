"""
Mock Teller client for testing without actual API access.
"""
from datetime import datetime, timedelta
from typing import Dict, List
import random


class MockTellerClient:
    """Mock client for testing Teller integration without API access."""
    
    def __init__(self):
        """Initialize the mock client with sample data."""
        self.mock_accounts = [
            {
                "id": "acc_mock_checking_001",
                "name": "Primary Checking",
                "type": "depository",
                "subtype": "checking",
                "currency": "USD",
                "status": "open",
                "institution": {
                    "name": "Mock Bank"
                }
            },
            {
                "id": "acc_mock_savings_001",
                "name": "Savings Account",
                "type": "depository",
                "subtype": "savings",
                "currency": "USD",
                "status": "open",
                "institution": {
                    "name": "Mock Bank"
                }
            },
            {
                "id": "acc_mock_credit_001",
                "name": "Credit Card",
                "type": "credit",
                "subtype": "credit_card",
                "currency": "USD",
                "status": "open",
                "institution": {
                    "name": "Mock Credit Union"
                }
            }
        ]
        
        self.mock_balances = {
            "acc_mock_checking_001": {"available": "2543.50", "ledger": "2543.50"},
            "acc_mock_savings_001": {"available": "15230.75", "ledger": "15230.75"},
            "acc_mock_credit_001": {"available": "-1250.00", "ledger": "-1250.00"}
        }
    
    def get_accounts(self) -> List[Dict]:
        """Return mock accounts."""
        print("Using MOCK data - replace with real Teller client when credentials are working")
        return self.mock_accounts
    
    def get_account(self, account_id: str) -> Dict:
        """Return a specific mock account."""
        for account in self.mock_accounts:
            if account["id"] == account_id:
                return account
        raise ValueError(f"Account {account_id} not found")
    
    def get_account_balances(self, account_id: str) -> Dict:
        """Return mock balance."""
        if account_id in self.mock_balances:
            return self.mock_balances[account_id]
        return {"available": "0.00", "ledger": "0.00"}
    
    def get_transactions(self, account_id: str, count: int = 100) -> List[Dict]:
        """Generate mock transactions."""
        transactions = []
        base_date = datetime.now()
        
        transaction_templates = [
            ("Amazon.com", -45.99),
            ("Grocery Store", -123.45),
            ("Gas Station", -52.30),
            ("Coffee Shop", -5.75),
            ("Salary Deposit", 3500.00),
            ("Utility Bill", -125.00),
            ("Netflix", -15.99),
            ("Restaurant", -67.50),
            ("Online Shopping", -89.99),
            ("ATM Withdrawal", -100.00)
        ]
        
        for i in range(min(count, 50)):
            template = random.choice(transaction_templates)
            date = base_date - timedelta(days=i)
            
            transactions.append({
                "id": f"txn_mock_{account_id}_{i}",
                "account_id": account_id,
                "amount": str(template[1]),
                "date": date.isoformat(),
                "description": template[0],
                "category": "general",
                "type": "card_payment" if template[1] < 0 else "ach",
                "status": "posted"
            })
        
        return transactions
    
    def get_account_details(self, account_id: str) -> Dict:
        """Return mock account details."""
        account = self.get_account(account_id)
        return {
            **account,
            "last_four": "1234",
            "routing_number": "123456789"
        }
    
    def test_connection(self) -> bool:
        """Mock connection test always succeeds."""
        print("Using MOCK Teller client")
        return True


def main():
    """Test the mock client."""
    print("Testing Mock Teller Client...")
    
    client = MockTellerClient()
    
    print("\n✓ Connection successful (MOCK MODE)!")
    
    accounts = client.get_accounts()
    print(f"\nFound {len(accounts)} account(s)")
    
    for account in accounts:
        print(f"\nAccount: {account['name']}")
        print(f"  ID: {account['id']}")
        print(f"  Type: {account['type']}")
        print(f"  Subtype: {account['subtype']}")
        print(f"  Institution: {account['institution']['name']}")
        
        balances = client.get_account_balances(account['id'])
        print(f"  Available: ${balances['available']}")
        print(f"  Ledger: ${balances['ledger']}")
        
        transactions = client.get_transactions(account['id'], count=5)
        print(f"  Recent transactions: {len(transactions)}")
        for txn in transactions[:3]:
            print(f"    - {txn['date'][:10]}: {txn['description']} (${txn['amount']})")


if __name__ == "__main__":
    main()
