"""
Testworld API Client

A Python client for interacting with the Testworld application API.
Use this to programmatically create companies and relationships for network simulations.
"""

import requests
import os
from typing import Dict, List, Optional, Any
from datetime import datetime


class TestworldClient:
    """Client for interacting with Testworld Supabase backend."""

    def __init__(self, supabase_url: str = None, supabase_key: str = None):
        """
        Initialize the Testworld API client.

        Args:
            supabase_url: Supabase project URL (defaults to env var VITE_SUPABASE_URL)
            supabase_key: Supabase anon/public key (defaults to env var VITE_SUPABASE_PUBLISHABLE_KEY)
        """
        self.supabase_url = supabase_url or os.getenv("VITE_SUPABASE_URL", "http://127.0.0.1:54321")
        self.supabase_key = supabase_key or os.getenv(
            "VITE_SUPABASE_PUBLISHABLE_KEY",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"
        )

        self.headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

        self.base_url = f"{self.supabase_url}/rest/v1"
        self.functions_url = f"{self.supabase_url}/functions/v1"

    def create_company(
        self,
        name: str,
        who_they_are: str = None,
        goals: str = None,
        risk_appetite: str = "moderate",
        market_position: str = "niche player",
        leadership_style: str = "data-driven",
        raw_data_ref: str = None
    ) -> Dict[str, Any]:
        """
        Create a new company in the database.

        Args:
            name: Company name (required)
            who_they_are: 2-3 sentence description of the company
            goals: Primary business objectives
            risk_appetite: Risk approach (conservative, moderate, aggressive)
            market_position: Market position (leader, challenger, niche player, emerging)
            leadership_style: Management approach
            raw_data_ref: Reference to original data source

        Returns:
            Dict containing the created company data with ID
        """
        company_data = {
            "name": name,
            "who_they_are": who_they_are,
            "goals": goals,
            "risk_appetite": risk_appetite,
            "market_position": market_position,
            "leadership_style": leadership_style,
            "raw_data_ref": raw_data_ref
        }

        response = requests.post(
            f"{self.base_url}/companies",
            json=company_data,
            headers=self.headers
        )
        response.raise_for_status()

        result = response.json()
        return result[0] if isinstance(result, list) else result

    def generate_company_profile(self, company_data: str) -> Dict[str, Any]:
        """
        Use AI to generate a company profile from raw text data.

        Args:
            company_data: Raw text describing the company

        Returns:
            Dict containing the AI-generated company profile
        """
        response = requests.post(
            f"{self.functions_url}/generate-entity",
            json={"companyData": company_data},
            headers=self.headers
        )
        response.raise_for_status()

        return response.json()["profile"]

    def create_company_from_ai(self, company_data: str) -> Dict[str, Any]:
        """
        Generate a company profile using AI and save it to the database.

        Args:
            company_data: Raw text describing the company

        Returns:
            Dict containing the created company with ID
        """
        # Generate profile using AI
        profile = self.generate_company_profile(company_data)

        # Save to database
        return self.create_company(
            name=profile.get("name"),
            who_they_are=profile.get("who_they_are"),
            goals=profile.get("goals"),
            risk_appetite=profile.get("risk_appetite", "moderate"),
            market_position=profile.get("market_position", "niche player"),
            leadership_style=profile.get("leadership_style", "data-driven"),
            raw_data_ref=company_data[:500]
        )

    def get_companies(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve all companies from the database.

        Args:
            limit: Maximum number of companies to return (default 100)

        Returns:
            List of company dictionaries
        """
        response = requests.get(
            f"{self.base_url}/companies?limit={limit}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_company_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Find a company by name.

        Args:
            name: Company name to search for

        Returns:
            Company dict if found, None otherwise
        """
        response = requests.get(
            f"{self.base_url}/companies?name=eq.{name}",
            headers=self.headers
        )
        response.raise_for_status()

        results = response.json()
        return results[0] if results else None

    def create_relationship(
        self,
        source_company_id: str,
        target_company_id: str,
        label: str,
        strength: float = 0.5
    ) -> Dict[str, Any]:
        """
        Create a relationship between two companies.

        Args:
            source_company_id: UUID of the source company
            target_company_id: UUID of the target company
            label: Relationship label (e.g., "Supplier", "Partner", "Competitor")
            strength: Relationship strength from 0.0 to 1.0

        Returns:
            Dict containing the created relationship data
        """
        if not 0 <= strength <= 1:
            raise ValueError("Strength must be between 0.0 and 1.0")

        relationship_data = {
            "source_company_id": source_company_id,
            "target_company_id": target_company_id,
            "label": label,
            "strength": strength
        }

        response = requests.post(
            f"{self.base_url}/relationships",
            json=relationship_data,
            headers=self.headers
        )
        response.raise_for_status()

        result = response.json()
        return result[0] if isinstance(result, list) else result

    def get_relationships(self, company_id: str = None) -> List[Dict[str, Any]]:
        """
        Get relationships, optionally filtered by company.

        Args:
            company_id: Optional company UUID to filter relationships

        Returns:
            List of relationship dictionaries
        """
        url = f"{self.base_url}/relationships"
        if company_id:
            url += f"?or=(source_company_id.eq.{company_id},target_company_id.eq.{company_id})"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def delete_company(self, company_id: str) -> bool:
        """
        Delete a company by ID.

        Args:
            company_id: UUID of the company to delete

        Returns:
            True if successful
        """
        response = requests.delete(
            f"{self.base_url}/companies?id=eq.{company_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return True

    def delete_relationship(self, relationship_id: str) -> bool:
        """
        Delete a relationship by ID.

        Args:
            relationship_id: UUID of the relationship to delete

        Returns:
            True if successful
        """
        response = requests.delete(
            f"{self.base_url}/relationships?id=eq.{relationship_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return True


if __name__ == "__main__":
    # Example usage
    client = TestworldClient()

    print("Testworld API Client initialized!")
    print(f"Connected to: {client.supabase_url}")

    # Example: List existing companies
    companies = client.get_companies()
    print(f"\nFound {len(companies)} companies in database")
    for company in companies:
        print(f"  - {company['name']}")
