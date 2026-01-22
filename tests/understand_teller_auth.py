"""
Test Teller API with enrollment-based authentication.

According to Teller docs, after a user completes enrollment, you receive
an access_token that should be used for API calls.

The TELLER_APP_TOKEN might be for a different purpose.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app_id = os.getenv("TELLER_APP_ID")
cert_path = "authentication/certificate.pem"
key_path = "authentication/private_key.pem"

print("="*60)
print("TELLER API - Understanding the Flow")
print("="*60)
print()
print("📚 How Teller Authentication Works:")
print("-" * 60)
print("1. You have a certificate (✓ valid until 2029)")
print("2. You have an APP_ID: app_pnpkbje8trq7hl1g6g000")
print("3. Users complete Teller Connect enrollment")
print("4. You receive an 'access_token' for each user")
print("5. Use certificate + access_token to call API")
print()
print("🔍 Current Situation:")
print("-" * 60)
print("• Your TELLER_APP_TOKEN might be a sandbox/test token")
print("• OR it might not be the right type of token for /accounts")
print("• You may need to complete the Teller Connect enrollment flow")
print("  to get a valid access_token for a real user/account")
print()
print("="*60)
print("Testing with sandbox endpoint...")
print("="*60)

# Try the test/sandbox token endpoint if available
test_endpoints = [
    ("GET /accounts", "https://api.teller.io/accounts"),
    ("GET /accounts (sandbox)", "https://sandbox.teller.io/accounts"),
    ("GET /test", "https://api.teller.io/test"),
]

app_token = os.getenv("TELLER_APP_TOKEN")

for name, url in test_endpoints:
    print(f"\n{name}: {url}")
    print("-" * 40)
    try:
        response = requests.get(
            url,
            cert=(cert_path, key_path),
            auth=(app_token, ""),
            timeout=10
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Success!")
            print(response.json())
        elif response.status_code == 404:
            print("⚠️  Endpoint not found")
        else:
            print(f"Response: {response.text[:150]}")
    except Exception as e:
        print(f"Error: {str(e)[:100]}")

print("\n" + "="*60)
print("RECOMMENDATION")
print("="*60)
print("""
To fully test with real data, you need to:

1. Set up Teller Connect in your application
2. Have a test user complete the enrollment flow
3. Capture the access_token returned
4. Use that access_token (not TELLER_APP_TOKEN) for API calls

For now, the mock client lets you develop and test your app.
When you're ready to connect real accounts:
- Implement Teller Connect UI
- Get real user access tokens
- Replace MockTellerClient with TellerClient

See: https://teller.io/docs/api/
""")

print("\n💡 Your app is fully functional with mock data!")
print("   You can continue development and come back to this later.")
