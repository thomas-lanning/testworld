"""
Example Usage of Testworld API Client

This script demonstrates various ways to use the Testworld client
to create companies and relationships programmatically.
"""

from testworld_client import TestworldClient


def example_basic_usage():
    """Basic example: Create companies manually and connect them."""
    client = TestworldClient()

    print("=== Example 1: Manual Company Creation ===\n")

    # Create companies with detailed information
    tesla = client.create_company(
        name="Tesla",
        who_they_are="Tesla is an electric vehicle and clean energy company that designs and manufactures electric cars, battery energy storage, and solar products.",
        goals="Accelerate the world's transition to sustainable energy through innovative electric vehicles and renewable energy solutions.",
        risk_appetite="aggressive",
        market_position="leader",
        leadership_style="visionary and innovative"
    )
    print(f"✓ Created company: {tesla['name']} (ID: {tesla['id']})")

    spacex = client.create_company(
        name="SpaceX",
        who_they_are="SpaceX is an aerospace manufacturer and space transportation company focused on reducing space transportation costs and enabling Mars colonization.",
        goals="Make humanity a multi-planetary species by developing reusable rockets and spacecraft.",
        risk_appetite="aggressive",
        market_position="leader",
        leadership_style="disruptive and ambitious"
    )
    print(f"✓ Created company: {spacex['name']} (ID: {spacex['id']})")

    # Create a relationship between them
    relationship = client.create_relationship(
        source_company_id=tesla['id'],
        target_company_id=spacex['id'],
        label="Sister Company",
        strength=0.9
    )
    print(f"\n✓ Created relationship: {relationship['label']} (strength: {relationship['strength']})")


def example_ai_generation():
    """Example using AI to generate company profiles from raw text."""
    client = TestworldClient()

    print("\n=== Example 2: AI-Powered Company Creation ===\n")

    # Create a company using AI to analyze raw data
    company_description = """
    Amazon is a multinational technology company focusing on e-commerce, cloud computing,
    digital streaming, and artificial intelligence. Founded by Jeff Bezos in 1994,
    Amazon started as an online bookstore and has grown into one of the world's most
    valuable companies. They prioritize customer obsession and long-term thinking.
    """

    amazon = client.create_company_from_ai(company_description)
    print(f"✓ AI-generated company: {amazon['name']}")
    print(f"  Who they are: {amazon['who_they_are'][:100]}...")
    print(f"  Goals: {amazon['goals'][:100]}...")
    print(f"  Risk appetite: {amazon['risk_appetite']}")


def example_batch_creation():
    """Example: Create multiple companies and relationships in batch."""
    client = TestworldClient()

    print("\n=== Example 3: Batch Creation ===\n")

    # Tech companies data
    tech_companies = [
        {
            "name": "Google",
            "description": "Google is a technology company specializing in Internet-related services and products, including search, advertising, cloud computing, and AI."
        },
        {
            "name": "Microsoft",
            "description": "Microsoft develops software, consumer electronics, and personal computers. Known for Windows, Office, Azure, and enterprise solutions."
        },
        {
            "name": "Meta",
            "description": "Meta (formerly Facebook) is a social media and technology company focused on building social platforms and the metaverse."
        }
    ]

    created_companies = []

    for company_data in tech_companies:
        try:
            company = client.create_company_from_ai(company_data["description"])
            created_companies.append(company)
            print(f"✓ Created: {company['name']}")
        except Exception as e:
            print(f"✗ Failed to create {company_data['name']}: {e}")

    # Create competitive relationships between all companies
    print("\n✓ Creating competitive relationships...")
    for i, company1 in enumerate(created_companies):
        for company2 in created_companies[i+1:]:
            try:
                client.create_relationship(
                    source_company_id=company1['id'],
                    target_company_id=company2['id'],
                    label="Competitor",
                    strength=0.7
                )
                print(f"  ↔ {company1['name']} <-> {company2['name']}")
            except Exception as e:
                print(f"  ✗ Failed to link {company1['name']} and {company2['name']}: {e}")


def example_querying():
    """Example: Query and display existing data."""
    client = TestworldClient()

    print("\n=== Example 4: Querying Data ===\n")

    # Get all companies
    companies = client.get_companies()
    print(f"Total companies: {len(companies)}")

    # Display each company
    for company in companies:
        print(f"\n📊 {company['name']}")
        print(f"   Position: {company['market_position']}")
        print(f"   Risk: {company['risk_appetite']}")

        # Get relationships for this company
        relationships = client.get_relationships(company['id'])
        if relationships:
            print(f"   Relationships: {len(relationships)}")
            for rel in relationships:
                print(f"     - {rel['label']} (strength: {rel['strength']})")


if __name__ == "__main__":
    print("Testworld API Client - Example Usage\n")
    print("Choose an example to run:")
    print("1. Basic manual company creation")
    print("2. AI-powered company generation")
    print("3. Batch creation with relationships")
    print("4. Query existing data")
    print("\nRunning Example 1 (you can modify the script to run others)...\n")

    # Run example 1 by default
    example_basic_usage()

    # Uncomment to run other examples:
    # example_ai_generation()
    # example_batch_creation()
    # example_querying()
