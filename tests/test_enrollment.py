#!/usr/bin/env python3
"""
Test script for Teller Connect enrollment flow.
This tests the enrollment endpoints without needing the full Teller Connect UI.
"""
import requests
import json
from datetime import datetime

API_BASE = "http://localhost:5001"

def test_enrollment_endpoints():
    """Test the Teller Connect enrollment endpoints."""
    
    print("=" * 60)
    print("Testing Teller Connect Enrollment Flow")
    print("=" * 60)
    print()
    
    # Test 1: Check initial enrollment status
    print("1️⃣  Checking initial enrollment status...")
    response = requests.get(f"{API_BASE}/api/teller-connect/status?user_id=test_user")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Enrollments: {data['count']}")
    print()
    
    # Test 2: Create a test enrollment
    print("2️⃣  Creating test enrollment...")
    enrollment_data = {
        "access_token": "test_token_" + datetime.now().strftime("%Y%m%d%H%M%S"),
        "enrollment_id": "enr_test_" + datetime.now().strftime("%Y%m%d%H%M%S"),
        "user_id": "test_user",
        "institution_name": "Test Bank"
    }
    
    response = requests.post(
        f"{API_BASE}/api/teller-connect/enroll",
        json=enrollment_data
    )
    print(f"   Status: {response.status_code}")
    result = response.json()
    
    if response.status_code in [200, 207]:  # 200 or 207 (Multi-Status)
        print(f"   ✅ Enrollment created: {result.get('enrollment_id')}")
        print(f"   Message: {result.get('message')}")
        
        if 'synced' in result:
            print(f"   Synced: {result['synced']}")
    else:
        print(f"   ❌ Error: {result.get('error')}")
    print()
    
    # Test 3: Check enrollment status again
    print("3️⃣  Checking enrollment status after creation...")
    response = requests.get(f"{API_BASE}/api/teller-connect/status?user_id=test_user")
    data = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Total enrollments: {data['count']}")
    
    if data['enrollments']:
        for i, enrollment in enumerate(data['enrollments'], 1):
            print(f"\n   Enrollment {i}:")
            print(f"     ID: {enrollment['enrollment_id']}")
            print(f"     Institution: {enrollment['institution_name']}")
            print(f"     Created: {enrollment['created_at']}")
            print(f"     Last Synced: {enrollment.get('last_synced', 'Never')}")
            print(f"     Active: {enrollment['is_active']}")
    print()
    
    # Test 4: Test duplicate enrollment (should update)
    print("4️⃣  Testing duplicate enrollment (should update)...")
    response = requests.post(
        f"{API_BASE}/api/teller-connect/enroll",
        json=enrollment_data
    )
    print(f"   Status: {response.status_code}")
    result = response.json()
    
    if response.status_code in [200, 207]:
        print(f"   ✅ Updated: {result.get('enrollment_id')}")
    else:
        print(f"   ❌ Error: {result.get('error')}")
    print()
    
    # Test 5: Disconnect enrollment
    if data['enrollments']:
        enrollment_id = data['enrollments'][0]['enrollment_id']
        print(f"5️⃣  Disconnecting enrollment: {enrollment_id}...")
        
        response = requests.post(
            f"{API_BASE}/api/teller-connect/disconnect/{enrollment_id}"
        )
        print(f"   Status: {response.status_code}")
        result = response.json()
        
        if response.status_code == 200:
            print(f"   ✅ {result.get('message')}")
        else:
            print(f"   ❌ Error: {result.get('error')}")
        print()
        
        # Check status after disconnect
        print("6️⃣  Checking status after disconnect...")
        response = requests.get(f"{API_BASE}/api/teller-connect/status?user_id=test_user")
        data = response.json()
        print(f"   Active enrollments: {data['count']}")
    
    print()
    print("=" * 60)
    print("✅ Enrollment endpoint tests complete!")
    print("=" * 60)


def test_api_with_enrollment():
    """Test API endpoints with enrollment data."""
    
    print("\n")
    print("=" * 60)
    print("Testing API Endpoints with Enrollment")
    print("=" * 60)
    print()
    
    # Test accounts endpoint
    print("🏦 Testing /api/accounts endpoint...")
    response = requests.get(f"{API_BASE}/api/accounts")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Found {data['count']} accounts")
        
        if data['accounts']:
            print(f"\n   Sample account:")
            account = data['accounts'][0]
            print(f"     Name: {account['name']}")
            print(f"     Type: {account['type']}")
            print(f"     Balance: ${account['current_balance']}")
    else:
        print(f"   ❌ Error: {response.status_code}")
    
    print()


def test_frontend_page():
    """Test if the Teller Connect frontend page is accessible."""
    
    print("\n")
    print("=" * 60)
    print("Testing Teller Connect Frontend")
    print("=" * 60)
    print()
    
    # Note: Flask needs to serve static files for this to work
    print("🌐 Teller Connect UI should be accessible at:")
    print(f"   📍 {API_BASE}/static/teller-connect.html")
    print()
    print("   Or open the file directly:")
    print("   📍 file:///<path-to-project>/static/teller-connect.html")
    print()


if __name__ == "__main__":
    try:
        # Test enrollment endpoints
        test_enrollment_endpoints()
        
        # Test API endpoints
        test_api_with_enrollment()
        
        # Show frontend info
        test_frontend_page()
        
        print("\n🎉 All tests completed successfully!")
        print("\nNext steps:")
        print("1. Open http://localhost:5001/static/teller-connect.html")
        print("2. Click 'Connect Bank Account'")
        print("3. Use Teller's sandbox mode for testing")
        print()
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API.")
        print("   Make sure the Flask app is running:")
        print("   $ mise run dev")
        print()
    except Exception as e:
        print(f"\n❌ Error: {e}")
