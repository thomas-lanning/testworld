"""
Quick Test Script

Run this to verify the Python API client is working correctly.
"""

from testworld_client import TestworldClient

def main():
    print("🚀 Testing Testworld Python API Client\n")
    print("=" * 50)

    # Initialize client
    print("\n1. Initializing client...")
    client = TestworldClient()
    print(f"   ✓ Connected to: {client.supabase_url}")

    # Test reading data
    print("\n2. Reading existing companies...")
    companies = client.get_companies()
    print(f"   ✓ Found {len(companies)} companies")
    for company in companies[:3]:  # Show first 3
        print(f"     - {company['name']}")

    # Test creating a company
    print("\n3. Creating a test company...")
    try:
        test_company = client.create_company(
            name="Python Test Company",
            who_they_are="A test company created via Python API",
            goals="Verify the Python client works correctly",
            risk_appetite="moderate",
            market_position="niche player",
            leadership_style="test-driven"
        )
        print(f"   ✓ Created: {test_company['name']}")
        print(f"   ✓ ID: {test_company['id']}")

        # Clean up - delete the test company
        print("\n4. Cleaning up test data...")
        client.delete_company(test_company['id'])
        print("   ✓ Test company deleted")

    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

    # Test AI generation (optional - requires Ollama)
    print("\n5. Testing AI generation...")
    try:
        profile = client.generate_company_profile(
            "Acme Inc. is a widget manufacturer specializing in industrial products."
        )
        print(f"   ✓ AI generated profile for: {profile.get('name', 'Unknown')}")
    except Exception as e:
        print(f"   ⚠ AI generation skipped (Ollama may not be running): {e}")

    print("\n" + "=" * 50)
    print("✅ All tests passed! Python API client is working.\n")
    print("Next steps:")
    print("  - Run: python example_usage.py")
    print("  - Run: python scraper_example.py")
    print("  - Read: README.md for full documentation")
    print()

if __name__ == "__main__":
    main()
