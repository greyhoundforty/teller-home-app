"""
Test if the token needs any transformation.
"""
import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

app_id = os.getenv("TELLER_APP_ID")
app_token = os.getenv("TELLER_APP_TOKEN")
cert_path = "authentication/certificate.pem"
key_path = "authentication/private_key.pem"

print("="*60)
print("TOKEN TRANSFORMATION TEST")
print("="*60)
print(f"Original Token: {app_token}")
print(f"Token Length: {len(app_token)}")
print()

# Try different token formats
token_variants = [
    ("Original", app_token),
    ("Without quotes", app_token.strip('"').strip("'")),
    ("Stripped whitespace", app_token.strip()),
]

# Check if it looks base64 encoded and try to decode
if app_token and app_token.endswith('='):
    try:
        decoded = base64.b64decode(app_token).decode('utf-8')
        token_variants.append(("Base64 decoded", decoded))
    except:
        pass

for name, token in token_variants:
    print(f"\n{name}: {token[:30]}...")
    print("-" * 60)
    
    try:
        response = requests.get(
            "https://api.teller.io/accounts",
            cert=(cert_path, key_path),
            auth=(token, ""),
            timeout=10
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! This token format works!")
            data = response.json()
            print(f"Found {len(data)} accounts")
            break
        else:
            try:
                error = response.json()
                print(f"Error: {error.get('error', {}).get('message', 'Unknown')}")
            except:
                print(f"Response: {response.text[:100]}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)[:100]}")

print("\n" + "="*60)
print("\nLet me also check the certificate details...")
print("="*60)

# Read and display certificate info
try:
    with open(cert_path, 'r') as f:
        cert_content = f.read()
        # Check for subject/CN in certificate
        if 'app_' in cert_content:
            print("✓ Certificate contains app_ reference")
        
        # Try to get basic cert info
        from subprocess import run, PIPE
        result = run(['openssl', 'x509', '-in', cert_path, '-noout', '-subject', '-dates'], 
                    capture_output=True, text=True)
        if result.returncode == 0:
            print("\nCertificate Information:")
            print(result.stdout)
        else:
            print("\nCould not read certificate details (openssl not available)")
except Exception as e:
    print(f"Could not read certificate: {e}")
