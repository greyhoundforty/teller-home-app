"""
Debug script to test Teller API authentication.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Get credentials
app_token = os.getenv("TELLER_APP_TOKEN")
cert_path = "authentication/certificate.pem"
key_path = "authentication/private_key.pem"

print(f"App Token: {app_token[:20]}..." if app_token else "No token found")
print(f"Certificate: {cert_path} (exists: {os.path.exists(cert_path)})")
print(f"Private Key: {key_path} (exists: {os.path.exists(key_path)})")
print()

# Test 1: Certificate auth only
print("Test 1: Certificate authentication only")
try:
    response = requests.get(
        "https://api.teller.io/accounts",
        cert=(cert_path, key_path)
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Success! Found {len(response.json())} accounts")
    else:
        print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Test 2: Certificate + Basic Auth
print("Test 2: Certificate + Basic Auth")
try:
    response = requests.get(
        "https://api.teller.io/accounts",
        auth=(app_token, ""),
        cert=(cert_path, key_path)
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Found {len(data)} accounts")
        for acc in data:
            print(f"  - {acc.get('name', 'Unknown')} ({acc.get('id')})")
    else:
        print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Test 3: Certificate + Bearer Token
print("Test 3: Certificate + Bearer Token")
try:
    response = requests.get(
        "https://api.teller.io/accounts",
        headers={"Authorization": f"Bearer {app_token}"},
        cert=(cert_path, key_path)
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Found {len(data)} accounts")
        for acc in data:
            print(f"  - {acc.get('name', 'Unknown')} ({acc.get('id')})")
    else:
        print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")
