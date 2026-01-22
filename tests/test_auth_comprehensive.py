"""
Comprehensive Teller API authentication test.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app_id = os.getenv("TELLER_APP_ID")
app_token = os.getenv("TELLER_APP_TOKEN")
cert_path = "authentication/certificate.pem"
key_path = "authentication/private_key.pem"

print("="*60)
print("TELLER API AUTHENTICATION TEST")
print("="*60)
print(f"App ID: {app_id}")
print(f"Token: {app_token[:20]}..." if app_token else "No token")
print(f"Cert exists: {os.path.exists(cert_path)}")
print(f"Key exists: {os.path.exists(key_path)}")
print()

tests = [
    {
        "name": "Test 1: Certificate only (no auth header)",
        "kwargs": {
            "cert": (cert_path, key_path)
        }
    },
    {
        "name": "Test 2: Certificate + Basic Auth (token as username)",
        "kwargs": {
            "cert": (cert_path, key_path),
            "auth": (app_token, "")
        }
    },
    {
        "name": "Test 3: Certificate + Basic Auth (app_id as username, token as password)",
        "kwargs": {
            "cert": (cert_path, key_path),
            "auth": (app_id, app_token)
        }
    },
    {
        "name": "Test 4: Certificate + Bearer token",
        "kwargs": {
            "cert": (cert_path, key_path),
            "headers": {"Authorization": f"Bearer {app_token}"}
        }
    },
    {
        "name": "Test 5: Certificate + Basic Auth (app_id as username, no password)",
        "kwargs": {
            "cert": (cert_path, key_path),
            "auth": (app_id, "")
        }
    },
    {
        "name": "Test 6: Certificate + Custom Header (API-Key)",
        "kwargs": {
            "cert": (cert_path, key_path),
            "headers": {"API-Key": app_token}
        }
    },
    {
        "name": "Test 7: Certificate + Custom Header (X-API-Key)",
        "kwargs": {
            "cert": (cert_path, key_path),
            "headers": {"X-API-Key": app_token}
        }
    },
]

for test in tests:
    print(f"\n{test['name']}")
    print("-" * 60)
    try:
        response = requests.get(
            "https://api.teller.io/accounts",
            **test['kwargs'],
            timeout=10
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS!")
            data = response.json()
            print(f"Found {len(data)} accounts")
            if data:
                for acc in data[:2]:  # Show first 2 accounts
                    print(f"  - {acc.get('name', 'Unknown')} ({acc.get('id')})")
            print("\n" + "="*60)
            print("🎉 WORKING AUTHENTICATION METHOD FOUND!")
            print("="*60)
            break
        else:
            try:
                error = response.json()
                print(f"Error: {error.get('error', {}).get('message', response.text[:100])}")
            except:
                print(f"Error: {response.text[:100]}")
    
    except requests.exceptions.SSLError as e:
        print(f"❌ SSL Error: {str(e)[:100]}")
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection Error: {str(e)[:100]}")
    except Exception as e:
        print(f"❌ Error: {str(e)[:100]}")

print("\n" + "="*60)
print("Test complete!")
print("="*60)
