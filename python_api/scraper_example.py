"""
Web Scraper Example for Testworld

This script demonstrates how to scrape company data from various sources
and automatically populate the Testworld database.

NOTE: This is a basic example. For production use, you should:
1. Respect robots.txt and rate limits
2. Add error handling and retries
3. Use proper user agents
4. Consider legal/ethical implications of scraping
"""

import time
import requests
from typing import List, Dict
from testworld_client import TestworldClient


class CompanyScraper:
    """Base class for scraping company information."""

    def __init__(self, client: TestworldClient):
        self.client = client
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

    def scrape_company_from_wikipedia(self, company_name: str) -> Dict:
        """
        Scrape basic company info from Wikipedia.

        NOTE: This is a simplified example. Real implementation would need:
        - BeautifulSoup for HTML parsing
        - Proper error handling
        - Rate limiting
        """
        # Wikipedia API endpoint
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{company_name.replace(' ', '_')}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Extract relevant information
            return {
                "name": data.get("title", company_name),
                "description": data.get("extract", "No description available"),
                "url": data.get("content_urls", {}).get("desktop", {}).get("page", "")
            }
        except Exception as e:
            print(f"Error scraping {company_name}: {e}")
            return None

    def scrape_and_create(self, company_name: str, add_delay: bool = True):
        """Scrape company data and create in database."""
        print(f"Scraping: {company_name}...")

        # Add delay to be respectful to servers
        if add_delay:
            time.sleep(1)

        # Scrape data
        company_data = self.scrape_company_from_wikipedia(company_name)

        if not company_data:
            print(f"  ✗ Failed to scrape {company_name}")
            return None

        # Check if company already exists
        existing = self.client.get_company_by_name(company_data["name"])
        if existing:
            print(f"  ⚠ {company_data['name']} already exists (ID: {existing['id']})")
            return existing

        # Use AI to generate full profile
        try:
            company = self.client.create_company_from_ai(company_data["description"])
            print(f"  ✓ Created: {company['name']} (ID: {company['id']})")
            return company
        except Exception as e:
            print(f"  ✗ Error creating {company_name}: {e}")
            return None


def example_scrape_tech_companies():
    """Example: Scrape and populate tech companies."""
    client = TestworldClient()
    scraper = CompanyScraper(client)

    print("=== Tech Company Scraper ===\n")

    # List of companies to scrape
    tech_companies = [
        "Apple Inc.",
        "Microsoft",
        "Amazon (company)",
        "Google",
        "Meta Platforms",
        "Tesla, Inc.",
        "Netflix",
        "Nvidia"
    ]

    created_companies = []

    for company_name in tech_companies:
        company = scraper.scrape_and_create(company_name)
        if company:
            created_companies.append(company)

    print(f"\n✓ Successfully created {len(created_companies)} companies")

    # Create industry relationships
    if len(created_companies) >= 2:
        print("\n✓ Creating industry relationships...")
        for i in range(len(created_companies) - 1):
            try:
                client.create_relationship(
                    source_company_id=created_companies[i]['id'],
                    target_company_id=created_companies[i + 1]['id'],
                    label="Industry Peer",
                    strength=0.6
                )
                print(f"  ↔ {created_companies[i]['name']} <-> {created_companies[i+1]['name']}")
            except Exception as e:
                print(f"  ✗ Error creating relationship: {e}")


def example_custom_data_source():
    """Example: Use custom data source (CSV, JSON, API, etc.)."""
    client = TestworldClient()

    print("\n=== Custom Data Source Example ===\n")

    # Example: Manual data that could come from a CSV, JSON file, or API
    companies_data = [
        {
            "name": "Acme Corp",
            "description": "Acme Corp is a fictional company that manufactures widgets and innovative products for various industries.",
            "relationships": ["Beta Industries"]
        },
        {
            "name": "Beta Industries",
            "description": "Beta Industries is a manufacturing company specializing in industrial automation and robotics.",
            "relationships": ["Acme Corp", "Gamma Tech"]
        },
        {
            "name": "Gamma Tech",
            "description": "Gamma Tech develops cutting-edge software solutions for enterprise resource planning and supply chain management.",
            "relationships": ["Beta Industries"]
        }
    ]

    # Create all companies first
    company_map = {}  # name -> company object

    for data in companies_data:
        # Check if already exists
        existing = client.get_company_by_name(data["name"])
        if existing:
            print(f"⚠ {data['name']} already exists")
            company_map[data["name"]] = existing
            continue

        # Create using AI
        try:
            company = client.create_company_from_ai(data["description"])
            company_map[data["name"]] = company
            print(f"✓ Created: {company['name']}")
        except Exception as e:
            print(f"✗ Error creating {data['name']}: {e}")

    # Create relationships
    print("\n✓ Creating relationships...")
    for data in companies_data:
        if data["name"] not in company_map:
            continue

        source = company_map[data["name"]]

        for partner_name in data["relationships"]:
            if partner_name not in company_map:
                continue

            target = company_map[partner_name]

            try:
                client.create_relationship(
                    source_company_id=source['id'],
                    target_company_id=target['id'],
                    label="Business Partner",
                    strength=0.75
                )
                print(f"  ↔ {source['name']} <-> {target['name']}")
            except Exception as e:
                # Relationship might already exist
                if "duplicate key" not in str(e).lower():
                    print(f"  ✗ Error: {e}")


if __name__ == "__main__":
    print("Testworld Web Scraper Examples\n")
    print("Choose an example:")
    print("1. Scrape tech companies from Wikipedia")
    print("2. Import from custom data source")
    print("\nRunning Example 1...\n")

    # Run example 1 (Wikipedia scraping)
    example_scrape_tech_companies()

    # Uncomment to run example 2:
    # example_custom_data_source()
