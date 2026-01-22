"""
Test script to verify API endpoints.
"""
import requests
import json

BASE_URL = "http://localhost:5001"

def print_response(title, response):
    """Pretty print API response."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))

try:
    # Test 1: Root endpoint
    print("\n🧪 Testing API Endpoints...")
    response = requests.get(f"{BASE_URL}/")
    print_response("1. Root Endpoint (/)", response)
    
    # Test 2: Health check
    response = requests.get(f"{BASE_URL}/api/health")
    print_response("2. Health Check (/api/health)", response)
    
    # Test 3: Get all accounts
    response = requests.get(f"{BASE_URL}/api/accounts")
    print_response("3. Get All Accounts (/api/accounts)", response)
    
    # Test 4: Get specific account (use first account ID from response)
    accounts = response.json()
    if accounts:
        account_id = accounts[0]['id']
        response = requests.get(f"{BASE_URL}/api/accounts/{account_id}")
        print_response(f"4. Get Specific Account (/api/accounts/{account_id})", response)
        
        # Test 5: Get transactions for account
        response = requests.get(f"{BASE_URL}/api/accounts/{account_id}/transactions?limit=5")
        print_response(f"5. Get Transactions (/api/accounts/{account_id}/transactions?limit=5)", response)
    
    # Test 6: Get scheduled payments
    response = requests.get(f"{BASE_URL}/api/scheduled-payments")
    print_response("6. Get Scheduled Payments (/api/scheduled-payments)", response)
    
    # Test 7: Create a scheduled payment
    new_payment = {
        "name": "Netflix Subscription",
        "amount": 15.99,
        "day_of_month": 15,
        "category": "Entertainment"
    }
    response = requests.post(f"{BASE_URL}/api/scheduled-payments", json=new_payment)
    print_response("7. Create Scheduled Payment (POST /api/scheduled-payments)", response)
    
    # Test 8: Get weekly forecast
    response = requests.get(f"{BASE_URL}/api/weekly-forecast")
    print_response("8. Get Weekly Forecast (/api/weekly-forecast)", response)
    
    print("\n✅ All tests completed successfully!")
    
except requests.exceptions.ConnectionError:
    print("\n❌ Error: Could not connect to the API")
    print("Make sure the Flask app is running on http://localhost:5001")
    print("Run: ./run_app.sh")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
